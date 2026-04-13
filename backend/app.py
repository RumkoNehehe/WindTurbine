from flask import Flask, render_template
from flask_socketio import SocketIO
import time
import threading
from deviceAdapter import ArduinoSerialAdapter, MotorMode

# Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"

# SocketIO
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# ---- Dummy state (zatiaľ bez adaptera) ----
state = {
    "value": 0
}

adapter = ArduinoSerialAdapter(port="COM5")

# ---- Background task ----
def background_loop():
    while True:
        idk =  adapter.get_state().motor1.rpm_display
        state["value"] = idk

        socketio.emit("device_state", state)

        time.sleep(1)

# ---- Routes ----
@app.route("/")
def index():
    return render_template("index.html")

# ---- Socket events ----
@socketio.on("connect")
def handle_connect():
    print("Client connected")
    adapter.connect()
    adapter.start_communication()

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

# ---- Main ----
if __name__ == "__main__":
    # spustenie background tasku
    socketio.start_background_task(background_loop)

    socketio.run(app, host="0.0.0.0", port=5000)