from flask import session
from . import state

def is_authenticated():
    return session.get("authenticated", False)

def is_admin():
    return session.get("authenticated") and session.get("role") == "admin"

def current_session_id():
    return session.get("session_id")

def release_admin_if_current_session():
    if session.get("role") == "admin":
        current_id = session.get("session_id")
        with state.auth_lock:
            if current_id == state.admin_session_id:
                state.admin_session_id = None