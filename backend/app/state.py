from datetime import datetime
import threading

clients_count = 0
background_thread = None
thread_lock = threading.Lock()

running = False

admin_session_id = None
auth_lock = threading.Lock()

regulation_running = False
regulation_thread = None
regulation_lock = threading.Lock()

state = {
    "isConnected": True,
    "lastUpdate": datetime.now().isoformat(),
    "motors": [],
    "logs": []
}

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