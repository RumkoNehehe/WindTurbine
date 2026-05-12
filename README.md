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

The recommended deployment method is **Docker Compose on Raspberry Pi**.

This setup runs the complete system on the Raspberry Pi:

* Frontend served as a production build
* Backend running in a Docker container
* PostgreSQL database running in a Docker container
* Arduino connected directly to Raspberry Pi via USB
* Remote access provided through Tailscale

The Raspberry Pi acts as the gateway between the web application, database, Arduino hardware, and remote user connected through Tailscale.

Recommended setup:

```text
Remote browser
    ↓
Tailscale network
    ↓
Raspberry Pi
    ↓
Docker Compose
    ├── Frontend container
    ├── Backend container
    └── PostgreSQL container
    ↓
Arduino connected via USB
```

The application should be accessed through the Raspberry Pi **Tailscale IP address**.

Example:

```text
http://100.78.68.88:5173
```

---

### 🔹 1. Prepare Raspberry Pi

Flash Raspberry Pi OS to the SD card.

Before first boot, enable SSH:

* In Raspberry Pi Imager advanced settings, or
* By placing an empty file named `ssh` in the boot partition

Connect to the Raspberry Pi:

```bash
ssh myuser@rpi.local
```

If the Raspberry Pi was reflashed and SSH reports that the host identification has changed, remove the old host key:

```bash
ssh-keygen -R rpi.local
```

Then connect again:

```bash
ssh myuser@rpi.local
```

---

### 🔹 2. Update System

```bash
sudo apt update
sudo apt upgrade -y
```

Optionally reboot after the upgrade:

```bash
sudo reboot
```

Reconnect via SSH after reboot.

---

### 🔹 3. Clone Repository

Install Git if it is not already installed:

```bash
sudo apt install -y git
```

Clone the repository:

```bash
git clone https://github.com/RumkoNehehe/WindTurbine/
```

Enter the project directory:

```bash
cd WindTurbine
```

---

### 🔹 4. Install Docker

Install Docker using the official installation script:

```bash
curl -fsSL https://get.docker.com | sh
```

Add the current user to the Docker group:

```bash
sudo usermod -aG docker $USER
newgrp docker
```

Enable Docker to start automatically after reboot:

```bash
sudo systemctl enable docker
sudo systemctl start docker
```

Check that Docker is installed and running:

```bash
docker --version
docker ps
```

---

### 🔹 5. Install Docker Compose Plugin

Install the Docker Compose plugin:

```bash
sudo apt install -y docker-compose-plugin
```

Check the installation:

```bash
docker compose version
```

Use the modern Docker Compose command:

```bash
docker compose
```

instead of the older:

```bash
docker-compose
```

---

### 🔹 6. Install and Configure Tailscale

Install Tailscale:

```bash
curl -fsSL https://tailscale.com/install.sh | sh
```

Start Tailscale and authenticate Raspberry Pi into the Tailscale network:

```bash
sudo tailscale up --ssh
```

The command prints a login URL. Open it in a browser and log in to the correct Tailscale account/network.

Check the Tailscale connection:

```bash
tailscale status
```

Get the Raspberry Pi Tailscale IP address:

```bash
tailscale ip -4
```

Example:

```text
100.78.68.88
```

Enable Tailscale to start automatically after reboot:

```bash
sudo systemctl enable tailscaled
sudo systemctl start tailscaled
```

Check that Tailscale is enabled:

```bash
systemctl is-enabled tailscaled
```

Expected output:

```text
enabled
```

---

### 🔹 7. Check Application Configuration

Before starting the containers, check frontend and backend configuration files.

The frontend must point to the backend using the Raspberry Pi **Tailscale IP address**.

Example frontend config:

```js
export const config = {
  backendBaseUrl: "http://100.78.68.88:8000",
};
```

Do not use `localhost` in frontend configuration when accessing the application remotely.

Incorrect:

```js
export const config = {
  backendBaseUrl: "http://localhost:8000",
};
```

When the frontend is opened from another computer, `localhost` refers to that computer, not the Raspberry Pi.

Use `http://`, not `https://`, unless HTTPS/TLS has been configured with a reverse proxy or certificates.

Correct:

```text
http://100.78.68.88:8000
```

Usually incorrect for this setup:

```text
https://100.78.68.88:8000
```

The backend should also allow requests from the frontend origin.

Example frontend origin:

```text
http://100.78.68.88:5173
```

For Flask, this can be configured with CORS:

```python
from flask_cors import CORS

CORS(app, origins=[
    "http://100.78.68.88:5173",
    "http://localhost:5173",
])
```

### 🔹 8. Docker Compose Configuration

The Docker Compose file should contain database, backend, and frontend services under the `services` section.

Example `docker-compose.yaml`:

```yaml
services:
  db:
    image: postgres:16-alpine
    container_name: app_db
    restart: unless-stopped
    environment:
      POSTGRES_DB: app_db
      POSTGRES_USER: app_user
      POSTGRES_PASSWORD: app_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database/init.sql:/docker-entrypoint-initdb.d/init.sql:ro

  backend:
    build:
      context: ./backend
    container_name: app_backend
    restart: unless-stopped
    depends_on:
      - db
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    devices:
      - "/dev/ttyACM0:/dev/ttyACM0"

  frontend:
    build:
      context: ./frontend
    container_name: app_frontend
    restart: unless-stopped
    depends_on:
      - backend
    ports:
      - "5173:80"

volumes:
  postgres_data:
```

### 🔹 9. Check Arduino Serial Port

Connect Arduino to Raspberry Pi using USB.

Check that the device is visible:

```bash
ls /dev/ttyACM*
```

Expected example:

```text
/dev/ttyACM0
```

The same device path must be mapped in `docker-compose.yaml`:

```yaml
devices:
  - "/dev/ttyACM0:/dev/ttyACM0"
```

If Arduino appears under a different port, update the Compose file accordingly.

---

### 🔹 10. Start Application

From the project root directory, build and start the containers:

```bash
docker compose up -d --build
```

Check running containers:

```bash
docker ps
```

Expected containers:

```text
app_frontend
app_backend
app_db
```

Expected port mappings:

```text
frontend: 5173 → 80
backend:  8000 → 8000
database: internal only, or 5433 → 5432 if explicitly exposed
```

---

### 🔹 11. Access Application

Open the frontend from a device connected to the same Tailscale network:

```text
http://TAILSCALE_IP:5173
```

Example:

```text
http://100.78.68.88:5173
```

The backend API is available at:

```text
http://TAILSCALE_IP:8000
```

Example:

```text
http://100.78.68.88:8000
```

---

### 🔹 12. CORS and Frontend URL Issues

If the frontend loads but API requests fail, check whether the frontend is still calling:

```text
http://localhost:8000
```

Search the frontend source:

```bash
grep -R "localhost:8000" -n ./frontend
```

Search inside the running frontend container:

```bash
docker exec -it app_frontend sh
grep -R "localhost:8000" -n /usr/share/nginx/html 2>/dev/null
grep -R "100.78.68.88:8000" -n /usr/share/nginx/html 2>/dev/null
```

If the old URL is still present, rebuild the frontend without cache:

```bash
docker compose down
docker compose build --no-cache frontend
docker compose up -d
```

Then hard refresh the browser:

```text
Ctrl + Shift + R
```

Or open browser DevTools, enable **Disable cache**, and reload the page.

The backend CORS configuration should allow the frontend origin:

```text
http://100.78.68.88:5173
```
---

### 🔹 Deployment Notes

* Docker Compose is the recommended deployment method
* Raspberry Pi should have sufficient storage available
* 8 GB SD card may not be enough for Docker images, database data, and system updates
* External SSD is recommended for better reliability
* Raspberry Pi and client computer must both be connected to the same Tailscale network
* Use Raspberry Pi Tailscale IP address in frontend configuration
* Do not use `localhost` in frontend configuration for remote access
* Use Docker service names such as `db` for communication between containers
* PostgreSQL does not need to expose a host port unless remote database access is required
* Use `http://` unless HTTPS has been explicitly configured
* Use `docker compose`, not the older `docker-compose`, on modern Docker installations
* Use the Nginx frontend Dockerfile for deployment instead of the Vite development server
* After changing frontend configuration, rebuild the frontend image because frontend configuration is usually included in the built JavaScript files

---

## 🧪 Development Notes

* Monorepo structure (frontend + backend)
* Git used for version control

---

## 📄 License

This project was developed as part of a diploma thesis.

---