from flask import Flask, render_template
from flask_socketio import SocketIO
from datetime import datetime, timezone
from simple_pid import PID
import time
import threading
from deviceAdapter import ArduinoSerialAdapter, MotorMode

# Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"

# SocketIO
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")
clients_count = 0
background_thread = None
thread_lock = threading.Lock()
running = False

state = {
    "isConnected": True,
    "lastUpdate": datetime.now().isoformat(),
    "motors": [],
    "logs": []
}

regulation_running = False
regulation_thread = None
regulation_lock = threading.Lock()

regulation_config = {
    "target": "motor1",
    "target_rpm": 0.0,
    "kp": 0.0,
    "ki": 0.0,
    "kd": 0.0,
    "mode": "FORWARD"
}

pid_motor1 = None
pid_motor2 = None

def clamp_pwm(value):
    return max(0, min(255, int(round(value))))

def build_pid(kp, ki, kd, target_rpm, starting_output=0.0):
        pid = PID(kp, ki,kd,setpoint=target_rpm)
        pid.sample_time = 0.1
        pid.output_limits = (0,255)
        pid.set_auto_mode(True, last_output=starting_output)
        return pid


adapter = ArduinoSerialAdapter(port="COM5")
# ---- Background task ----
def background_loop():
    global running

    while running:
        idk = adapter.get_state()

        state["isConnected"] = True
        state["lastUpdate"] = datetime.now(timezone.utc).isoformat()
        state["motors"] = [
            {
                "name": "Motor 1",
                "pwm": idk.motor1.pwm,
                "rpm": int(round(idk.motor1.rpm_display)),
                "mode": str(idk.motor1.mode.name)
            },
            {
                "name": "Motor 2",
                "pwm": idk.motor2.pwm,
                "rpm": int(round(idk.motor2.rpm_display)),
                "mode": str(idk.motor2.mode.name)
            }
        ]
        print("emiting update")
        socketio.emit("dashboard_update", state)
        socketio.sleep(0.5)

def regulation_loop():
    global regulation_running, pid_motor1, pid_motor2

    print("Regulation loop started")

    while regulation_running:
        try:
            current = adapter.get_state()

            mode_str = regulation_config["mode"]
            try:
                mode = MotorMode[mode_str]
            except KeyError:
                mode = MotorMode.BRAKE

            target = regulation_config["target"]

            if target in ("motor1", "both") and pid_motor1 is not None:
                rpm1 = float(current.motor1.rpm_display)
                pwm1 = pid_motor1(rpm1)
                adapter.set_motor1(clamp_pwm(pwm1), mode)

            if target in ("motor2", "both") and pid_motor2 is not None:
                rpm2 = float(current.motor2.rpm_display)
                pwm2 = pid_motor2(rpm2)
                adapter.set_motor2(clamp_pwm(pwm2), mode)

        except Exception as e:
            print(f"Regulation loop error: {e}")

        socketio.sleep(0.1)

    print("Regulation loop stopped")

# ---- Socket events ----
@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("connect")
def handle_connect():
    global clients_count, background_thread, running
    print("nehehe")

    with thread_lock:
        clients_count += 1
        print(f"Client connected, count={clients_count}")

        if not running:
            adapter.connect()
            adapter.start_communication()
            running = True
            background_thread = socketio.start_background_task(background_loop)


@socketio.on("disconnect")
def handle_disconnect():
    global clients_count, running, regulation_running, pid_motor1, pid_motor2

    with thread_lock:
        clients_count -= 1
        print(f"Client disconnected, count={clients_count}")

        if clients_count <= 0:
            clients_count = 0
            running = False
            regulation_running = False

            if pid_motor1 is not None:
                pid_motor1.reset()
            if pid_motor2 is not None:
                pid_motor2.reset()

            pid_motor1 = None
            pid_motor2 = None

            adapter.stop_system()
            adapter.disconnect()

@socketio.on("stop_system")
def handle_stop():
    global regulation_running, pid_motor1, pid_motor2

    print("Received request to stop system")

    regulation_running = False

    if pid_motor1 is not None:
        pid_motor1.reset()
    if pid_motor2 is not None:
        pid_motor2.reset()

    pid_motor1 = None
    pid_motor2 = None

    adapter.stop_system()

@socketio.on("set_motor_1")
def handle_set_motor1(data):
    print("received request to set motor 1")
    pwm = data.get("pwm", 0)
    mode_str = data.get("mode", "BRAKE")
    try:
        mode = MotorMode[mode_str]
    except KeyError:
        print("Invalid mode, fallback to BRAKE")
        mode = MotorMode.BRAKE

    print(f"pwm: {pwm} mode: {mode}")
    adapter.set_motor1(pwm, mode)

@socketio.on("set_motor_2")
def handle_set_motor2(data):
    print("received request to set motor 2")
    pwm = data.get("pwm", 0)
    mode_str = data.get("mode", "BRAKE")
    try:
        mode = MotorMode[mode_str]
    except KeyError:
        print("Invalid mode, fallback to BRAKE")
        mode = MotorMode.BRAKE

    print(f"pwm: {pwm} mode: {mode}")
    adapter.set_motor2(pwm, mode)

@socketio.on("start_regulation")
def handle_start_regulation(data):
    global regulation_running, regulation_thread, pid_motor1, pid_motor2

    with regulation_lock:
        if regulation_running:
            print("Regulation already running")
            return

        target = data.get("target", "motor1")
        target_rpm = float(data.get("target_rpm", 0))
        kp = float(data.get("kp", 0))
        ki = float(data.get("ki", 0))
        kd = float(data.get("kd", 0))
        mode = data.get("mode", "FORWARD")

        regulation_config["target"] = target
        regulation_config["target_rpm"] = target_rpm
        regulation_config["kp"] = kp
        regulation_config["ki"] = ki
        regulation_config["kd"] = kd
        regulation_config["mode"] = mode

        current = adapter.get_state()

        pid_motor1 = None
        pid_motor2 = None

        if target in ("motor1", "both"):
            pid_motor1 = build_pid(
                kp, ki, kd, target_rpm,
                starting_output=float(current.motor1.pwm)
            )

        if target in ("motor2", "both"):
            pid_motor2 = build_pid(
                kp, ki, kd, target_rpm,
                starting_output=float(current.motor2.pwm)
            )

        regulation_running = True
        regulation_thread = socketio.start_background_task(regulation_loop)

        print("Started regulation:", regulation_config)


@socketio.on("stop_regulation")
def handle_stop_regulation():
    global regulation_running, pid_motor1, pid_motor2

    with regulation_lock:
        regulation_running = False

        if pid_motor1 is not None:
            pid_motor1.reset()

        if pid_motor2 is not None:
            pid_motor2.reset()

        pid_motor1 = None
        pid_motor2 = None

        print("Stopped regulation")

# ---- Main ----
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8000, allow_unsafe_werkzeug=True)