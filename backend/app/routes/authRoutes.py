from uuid import uuid4
from flask import Blueprint, request, session, jsonify

from ..config import Config
from .. import state

auth_bp = Blueprint("auth", __name__)

@auth_bp.post("/login")
def login():
    data = request.get_json() or {}
    username = data.get("username", "")
    password = data.get("password", "")

    with state.auth_lock:
        if username == Config.ADMIN_USERNAME and password == Config.ADMIN_PASSWORD:
            if state.admin_session_id is not None:
                return jsonify({
                    "success": False,
                    "message": "Admin is already logged in."
                }), 409

            current_session_id = str(uuid4())
            session["authenticated"] = True
            session["role"] = "admin"
            session["session_id"] = current_session_id
            state.admin_session_id = current_session_id

            return jsonify({
                "success": True,
                "role": "admin"
            })

        if username == Config.USER_USERNAME and password == Config.USER_PASSWORD:
            session["authenticated"] = True
            session["role"] = "user"
            session["session_id"] = str(uuid4())

            return jsonify({
                "success": True,
                "role": "user"
            })

    return jsonify({
        "success": False,
        "message": "Invalid credentials."
    }), 401

@auth_bp.post("/logout")
def logout():
    with state.auth_lock:
        if session.get("role") == "admin":
            current_session_id = session.get("session_id")
            if current_session_id == state.admin_session_id:
                state.admin_session_id = None

        session.clear()

    return jsonify({"success": True})

@auth_bp.get("/me")
def me():
    if not session.get("authenticated"):
        return jsonify({
            "authenticated": False
        })

    return jsonify({
        "authenticated": True,
        "role": session.get("role")
    })