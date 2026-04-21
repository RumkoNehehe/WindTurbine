from datetime import datetime, timezone
from simple_pid import PID
from ..config import Config
from backend.app.device.deviceAdapter import ArduinoSerialAdapter, MotorMode

from ..extensions import socketio
from ..config import Config
from .. import state

adapter = ArduinoSerialAdapter(port=Config.ARDUINO_PORT)

def clamp_pwm(value):
    return max(0, min(255, int(round(value))))

def build_pid(kp, ki, kd, target_rpm, starting_output=0.0):
    pid = PID(kp, ki, kd, setpoint=target_rpm)
    pid.sample_time = Config.PID_SAMPLE_TIME_IN_SECONDS  
    pid.output_limits = (0, 255)
    pid.set_auto_mode(True, last_output=starting_output)
    return pid

def parse_mode(mode_str: str) -> MotorMode:
    try:
        return MotorMode[mode_str]
    except KeyError:
        return MotorMode.BRAKE

def update_dashboard_state():
    current = adapter.get_state()

    state.state["isConnected"] = True
    state.state["lastUpdate"] = datetime.now(timezone.utc).isoformat()
    state.state["motors"] = [
        {
            "name": "Motor 1",
            "pwm": current.motor1.pwm,
            "rpm": int(round(current.motor1.rpm_display)),
            "mode": str(current.motor1.mode.name),
        },
        {
            "name": "Motor 2",
            "pwm": current.motor2.pwm,
            "rpm": int(round(current.motor2.rpm_display)),
            "mode": str(current.motor2.mode.name),
        },
    ]

def background_loop():
    while state.running:
        try:
            update_dashboard_state()
            socketio.emit("dashboard_update", state.state)
        except Exception as e:
            print(f"Background loop error: {e}")

        socketio.sleep(Config.BACKROUND_LOOP_SLEEP_IN_SECONDS)

def regulation_loop():
    print("Regulation loop started")

    while state.regulation_running:
        try:
            current = adapter.get_state()
            mode = parse_mode(state.regulation_config["mode"])
            target = state.regulation_config["target"]

            if target in ("motor1", "both") and state.pid_motor1 is not None:
                rpm1 = float(current.motor1.rpm_display)
                pwm1 = state.pid_motor1(rpm1)
                adapter.set_motor1(clamp_pwm(pwm1), mode)

            if target in ("motor2", "both") and state.pid_motor2 is not None:
                rpm2 = float(current.motor2.rpm_display)
                pwm2 = state.pid_motor2(rpm2)
                adapter.set_motor2(clamp_pwm(pwm2), mode)

        except Exception as e:
            print(f"Regulation loop error: {e}")

        socketio.sleep(Config.PID_SAMPLE_TIME_IN_SECONDS)

    print("Regulation loop stopped")

def connect_system():
    if not state.running:
        adapter.connect()
        adapter.start_communication()
        state.running = True
        state.background_thread = socketio.start_background_task(background_loop)

def disconnect_system():
    state.running = False
    state.regulation_running = False

    if state.pid_motor1 is not None:
        state.pid_motor1.reset()
    if state.pid_motor2 is not None:
        state.pid_motor2.reset()

    state.pid_motor1 = None
    state.pid_motor2 = None

    adapter.stop_system()
    adapter.disconnect()

def stop_system():
    state.regulation_running = False

    if state.pid_motor1 is not None:
        state.pid_motor1.reset()
    if state.pid_motor2 is not None:
        state.pid_motor2.reset()

    state.pid_motor1 = None
    state.pid_motor2 = None

    adapter.stop_system()

def set_motor_1(pwm: int, mode_str: str):
    adapter.set_motor1(pwm, parse_mode(mode_str))

def set_motor_2(pwm: int, mode_str: str):
    adapter.set_motor2(pwm, parse_mode(mode_str))

def start_regulation(data: dict):
    with state.regulation_lock:
        if state.regulation_running:
            print("Regulation already running")
            return

        target = data.get("target", "motor1")
        target_rpm = float(data.get("target_rpm", 0))
        kp = float(data.get("kp", 0))
        ki = float(data.get("ki", 0))
        kd = float(data.get("kd", 0))
        mode = data.get("mode", "FORWARD")

        state.regulation_config["target"] = target
        state.regulation_config["target_rpm"] = target_rpm
        state.regulation_config["kp"] = kp
        state.regulation_config["ki"] = ki
        state.regulation_config["kd"] = kd
        state.regulation_config["mode"] = mode

        current = adapter.get_state()

        state.pid_motor1 = None
        state.pid_motor2 = None

        if target == "motor1":
            state.pid_motor1 = build_pid(
                kp, ki, kd, target_rpm,
                starting_output=float(current.motor1.pwm),
            )

        elif target == "motor2":
            state.pid_motor2 = build_pid(
                kp, ki, kd, target_rpm,
                starting_output=float(current.motor2.pwm),
            )

        elif target == "both":
            state.pid_motor1 = build_pid(
                kp, ki, kd, target_rpm,
                starting_output=float(current.motor1.pwm),
            )
            state.pid_motor2 = build_pid(
                kp, ki, kd, target_rpm,
                starting_output=float(current.motor2.pwm),
            )

        state.regulation_running = True
        state.regulation_thread = socketio.start_background_task(regulation_loop)

        print("Started regulation:", state.regulation_config)

def stop_regulation():
    with state.regulation_lock:
        state.regulation_running = False

        if state.pid_motor1 is not None:
            state.pid_motor1.reset()
        if state.pid_motor2 is not None:
            state.pid_motor2.reset()

        state.pid_motor1 = None
        state.pid_motor2 = None

        print("Stopped regulation")