class Config:
    SECRET_KEY = "secret!"
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False

    CORS_ORIGINS = [
        "http://localhost:5173",
        "http://192.168.0.165:5173",
    ]

    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "admin123"

    USER_USERNAME = "user"
    USER_PASSWORD = "user123"

    ARDUINO_PORT = "COM5"