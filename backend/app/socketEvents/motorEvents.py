from flask import session
from flask_socketio import emit

from .. import state
from ..auth import is_admin
from ..device.device import (
    connect_system,
    disconnect_system,
    stop_system,
    set_motor_1,
    set_motor_2,
    start_regulation,
    stop_regulation,
)

def register_motor_events(socketio):
    @socketio.on("connect")
    def handle_connect():
        with state.thread_lock:
            state.clients_count += 1
            print(f"Client connected, count={state.clients_count}")

            if not state.running:
                connect_system()

    @socketio.on("disconnect")
    def handle_disconnect():
        with state.thread_lock:
            state.clients_count -= 1
            print(f"Client disconnected, count={state.clients_count}")

            if session.get("role") == "admin":
                current_session_id = session.get("session_id")
                with state.auth_lock:
                    if current_session_id == state.admin_session_id:
                        state.admin_session_id = None
                        print("Admin session released on disconnect")

            if state.clients_count <= 0:
                state.clients_count = 0
                disconnect_system()

    @socketio.on("stop_system")
    def handle_stop():
        if not is_admin():
            print("Unauthorized stop_system")
            emit("error", {"message": "Unauthorized"})
            return

        stop_system()

    @socketio.on("set_motor_1")
    def handle_set_motor1(data):
        if not is_admin():
            print("Unauthorized set_motor_1")
            emit("error", {"message": "Unauthorized"})
            return

        pwm = data.get("pwm", 0)
        mode = data.get("mode", "BRAKE")
        set_motor_1(pwm, mode)

    @socketio.on("set_motor_2")
    def handle_set_motor2(data):
        if not is_admin():
            print("Unauthorized set_motor_2")
            emit("error", {"message": "Unauthorized"})
            return

        pwm = data.get("pwm", 0)
        mode = data.get("mode", "BRAKE")
        set_motor_2(pwm, mode)

    @socketio.on("start_regulation")
    def handle_start_regulation(data):
        if not is_admin():
            print("Unauthorized start_regulation")
            emit("error", {"message": "Unauthorized"})
            return

        start_regulation(data)

    @socketio.on("stop_regulation")
    def handle_stop_regulation():
        if not is_admin():
            print("Unauthorized stop_regulation")
            emit("error", {"message": "Unauthorized"})
            return

        stop_regulation()