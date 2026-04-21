from flask import Flask
from flask_cors import CORS

from .config import Config
from .extensions import socketio
from .routes.authRoutes import auth_bp
from .routes.recordingsRoutes import recording_bp
from .socketEvents.motorEvents import register_motor_events
from .extensions import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    init_db(app)

    CORS(
        app,
        supports_credentials=True,
        origins=Config.CORS_ORIGINS
    )

    socketio.init_app(
        app,
        cors_allowed_origins=Config.CORS_ORIGINS,
    )

    app.register_blueprint(auth_bp)
    app.register_blueprint(recording_bp)
    register_motor_events(socketio)

    @app.get("/")
    def index():
        return {"message": "Backend running"}

    return app