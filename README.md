# 🌬️ Wind Turbine Control System

Web-based system for **remote control and monitoring of a wind turbine laboratory model**.
The application enables real-time interaction with hardware via a browser, including control of motors, data visualization, and experiment recording.

---

## 🚀 Features

* ⚡ Real-time control using WebSocket communication
* 📊 Live visualization of motor speed (RPM), PWM signals, and system state
* 🎯 PID regulation for automatic speed control
* 💾 Recording and storage of experiments (PostgreSQL)
* 👥 Role-based access (admin / user)
* 🌐 Remote access via secure network (Tailscale)
* 🔌 Direct communication with Arduino via serial interface

---

## 🏗️ Architecture

The system follows a **client–server architecture**:

* **Frontend** – Vue.js web application
* **Backend** – Flask + Flask-SocketIO
* **Database** – PostgreSQL
* **Hardware** – Arduino (motor control + sensors)
* **Gateway** – Raspberry Pi (runs backend + connects to hardware)

Communication:

* WebSocket → real-time control & monitoring
* REST API → authentication & database operations
* Serial (USB) → backend ↔ Arduino

---

## 🛠️ Technologies

* Python (Flask, Flask-SocketIO)
* Vue.js
* PostgreSQL
* Docker (optional)
* Tailscale (remote access)
* Arduino

---

## ⚙️ Installation

### 🔹 Option 1: Run locally (without Docker)

#### Backend

```bash
cd backend
pip install -r requirements.txt
python run.py
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

### 🔹 Option 2: Docker (recommended)

```bash
docker-compose up --build
```

---

## 🧩 Configuration

Before running, check:

* Serial port (e.g. `/dev/ttyACM0`)
* Database credentials (PostgreSQL)
* Backend port (default: `8000`)
* Frontend port (default: `5173`)

---

## 🔌 Hardware Connection

* Arduino connected via USB
* Serial communication using custom protocol:

  * `M1` → command (backend → device)
  * `N1` → response (device → backend)
* Data encoded in **little-endian format**

---

## 🔄 WebSocket API

### Client → Server

```json
set_motor_1
set_motor_2
start_regulation
stop_regulation
stop_system
```

Example:

```json
{
  "pwm": 120,
  "mode": "FORWARD"
}
```

---

### Server → Client

```json
device_state
```

Example:

```json
{
  "lastUpdate": "2026-04-22T11:07:50.708Z",
  "motors": [
    {
      "name": "Motor 1",
      "pwm": 128,
      "rpm": 311,
      "mode": "FORWARD"
    }
  ]
}
```

---

## 🌐 REST API

| Method | Endpoint      | Description         |
| ------ | ------------- | ------------------- |
| POST   | `/login`      | User authentication |
| POST   | `/logout`     | Logout              |
| GET    | `/me`         | Current user info   |
| GET    | `/recordings` | List saved data     |
| POST   | `/recordings` | Save measurement    |

---

## 🎯 PID Regulation

* Automatic control of motor speed
* Configurable parameters:

  * Kp, Ki, Kd
* Runs in backend loop with defined sampling time
* Can be enabled/disabled in real-time

---

## 💾 Data Storage

Measurements are stored as JSON:

```json
{
  "lastUpdate": "2026-04-22T11:07:50.708Z",
  "motors": [
    {
      "pwm": 128,
      "rpm": 311
    }
  ]
}
```

---

## 🔐 Security

* Role-based access:

  * **Admin** → control system
  * **User** → monitoring only
* Passwords stored as **hashed values**
* Authentication via **session cookies**
* Access restricted via **Tailscale private network**

---

## 🚀 Deployment

The system is designed to run on **Raspberry Pi**:

* Backend runs as service or Docker container
* Arduino connected via USB
* Remote access via Tailscale

⚠️ Note: Docker deployment requires sufficient storage (8GB SD card may not be enough)

---

## 🧪 Development Notes

* Monorepo structure (frontend + backend)
* Git used for version control
---

## 📄 License

This project was developed as part of a diploma thesis.

---
