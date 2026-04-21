class Config:
    SECRET_KEY = "secret!"
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False

    CORS_ORIGINS = [
        "http://localhost:5173",
        "http://192.168.0.165:5173",
    ]

    ARDUINO_PORT = "COM5"

    BACKROUND_LOOP_SLEEP_IN_SECONDS = 0.5
    PID_SAMPLE_TIME_IN_SECONDS = 0.1