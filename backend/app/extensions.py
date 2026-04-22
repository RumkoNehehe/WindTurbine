from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

from .config import Config

socketio = SocketIO(async_mode="threading")

db = SQLAlchemy()


def init_db(app):
    """
    Initialize the database with the Flask app
    """

    app.config["SQLALCHEMY_DATABASE_URI"] = (Config.DATABASE_CONNECTION_STRING)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)