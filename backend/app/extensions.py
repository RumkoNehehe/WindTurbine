from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

socketio = SocketIO(async_mode="threading")

db = SQLAlchemy()


def init_db(app):
    """
    Initialize the database with the Flask app
    """

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "postgresql://app_user:app_password@localhost:5433/app_db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)