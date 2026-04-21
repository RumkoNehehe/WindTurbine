from uuid import uuid4
from flask import Blueprint, request, session, jsonify
from werkzeug.security import check_password_hash

from .. import state
from ..extensions import db
from ..models.db_user import AppUser

auth_bp = Blueprint("auth", __name__)

@auth_bp.post("/login")
def login():
    data = request.get_json() or {}
    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return jsonify({
            "success": False,
            "message": "Username and password are required."
        }), 400

    try:
        user = db.session.execute(
            db.select(AppUser).where(AppUser.username == username)
        ).scalar_one_or_none()

        if user is None:
            return jsonify({
                "success": False,
                "message": "Invalid credentials."
            }), 401

        if not check_password_hash(user.password, password):
            return jsonify({
                "success": False,
                "message": "Invalid credentials."
            }), 401

        with state.auth_lock:
            if user.user_type == "admin":
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
                }), 200

            if user.user_type == "user":
                session["authenticated"] = True
                session["role"] = "user"
                session["session_id"] = str(uuid4())

                return jsonify({
                    "success": True,
                    "role": "user"
                }), 200

        return jsonify({
            "success": False,
            "message": "Invalid user type."
        }), 403

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Database error: {str(e)}"
        }), 500


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