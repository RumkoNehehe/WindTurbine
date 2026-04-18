from flask import Flask, render_template
from flask_socketio import SocketIO
from datetime import datetime, timezone
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
        socketio.sleep(1)

# def dummy_background_loop():
#     dummyPwm = 60
#     dummyRpm = 10
#     while True:
#         idk =  adapter.get_state()
#         if(dummyRpm != 400):
#             dummyRpm+=20
#         state["isConnected"] = True
#         state["lastUpdate"] = datetime.now(timezone.utc).isoformat()
#         state["motors"] = [
#             {"name": "Motor 1"  , "pwm": dummyPwm, "rpm": int(round(dummyRpm)), "mode": str("Forward")},
#             {"name": "Motor 2"  , "pwm": dummyPwm, "rpm": int(round(dummyRpm-10)), "mode": str("Backward")}
#             ]

#         print("sending Socket")
#         socketio.emit("dashboard_update", state)

#         socketio.sleep(1)

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
    global clients_count, running

    with thread_lock:
        clients_count -= 1
        print(f"Client disconnected, count={clients_count}")

        if clients_count <= 0:
            clients_count = 0
            running = False
            adapter.stop_system()
            adapter.disconnect()

@socketio.on("stop_system")
def handle_stop():
    print("Received request to stop system")
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

# ---- Main ----
if __name__ == "__main__":
    # spustenie background tasku
    socketio.run(app, host="0.0.0.0", port=5000)