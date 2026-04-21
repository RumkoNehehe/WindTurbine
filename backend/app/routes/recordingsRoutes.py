from flask import Blueprint, request, session, jsonify

from ..extensions import db
from ..models.db_recording import Recording

recording_bp = Blueprint("recording", __name__)

@recording_bp.get("/recording/<int:recording_id>")
def get_recording_by_id(recording_id):
    try:
        recording = db.session.execute(
            db.select(Recording).where(Recording.id == recording_id)
        ).scalar_one_or_none()

        if recording is None:
            return jsonify({
                "message": "Recording not found"
            }), 404
        
        return jsonify({
            "id": recording.id,
            "name": recording.name,
            "message": "Recording found successfully",
            "data": recording.data,
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": f"Database error: {str(e)}"
        }), 500
    

@recording_bp.get("/recording")
def get_recording_list():
    try:
        recordings = db.session.execute(
            db.select(Recording.id, Recording.name)
        ).all()

        data = [
            {
                "id": r.id,
                "name": r.name
            }
            for r in recordings
        ]

        return jsonify({
            "message": "Recordings fetched successfully",
            "data": data,
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": f"Database error: {str(e)}"
        }), 500
    
@recording_bp.post("/recording")
def create_recording():
    request_data = request.get_json() or {}

    if not session.get("authenticated"):
        return jsonify({
            "success": False,
            "message": "Unauthorized"
        }), 401

    name = request_data.get("name")
    data = request_data.get("data")

    if not name or data is None:
        return jsonify({
            "success": False,
            "message": "Missing name or data"
        }), 400

    if not isinstance(data, list):
        return jsonify({
            "success": False,
            "message": "Recording data must be a JSON array"
        }), 400

    try:
        record = Recording(
            name=name,
            data=data
        )

        db.session.add(record)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Recording created successfully",
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": f"Database error: {str(e)}"
        }), 500