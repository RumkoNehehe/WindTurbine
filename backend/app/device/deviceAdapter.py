import serial
import struct
import threading
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ============================================================
# DOMAIN MODEL
# ============================================================

class MotorMode(Enum):
    FORWARD = 85
    REVERSE = 170
    BRAKE = 165


@dataclass
class MotorCommand:
    pwm: int = 0
    mode: MotorMode = MotorMode.BRAKE


@dataclass
class DeviceCommand:
    motor1: MotorCommand = field(default_factory=MotorCommand)
    motor2: MotorCommand = field(default_factory=MotorCommand)
    relay_on: bool = False


@dataclass
class MotorState:
    pwm: int = 0
    mode: MotorMode = MotorMode.BRAKE
    rpm_raw: int = 0
    rpm_display: float = 0.0


@dataclass
class DeviceState:
    connected: bool = False
    last_update_ts: float = 0.0
    motor1: MotorState = field(default_factory=MotorState)
    motor2: MotorState = field(default_factory=MotorState)
    relay_on: bool = False
    voltage_raw: int = 0
    generator_raw: int = 0
    raw_frame_hex: str = ""


# ============================================================
# PROTOCOL CODEC
# ============================================================

class ArduinoProtocol:
    TX_HEADER = b"M1"
    RX_HEADER = b"N1"

    TX_FRAME_SIZE = 8   # "M1" + 6 bytes
    RX_FRAME_SIZE = 10  # "N1" + 8 bytes

    RPM_SCALE_LCD = 6.62

    @staticmethod
    def clamp_u8(value: int) -> int:
        return max(0, min(255, int(value)))

    @classmethod
    def encode_command(cls, command: DeviceCommand) -> bytes:
        relay_l = 122 if command.relay_on else 0
        relay_h = 0

        payload = bytes([
            cls.clamp_u8(command.motor1.pwm),
            command.motor1.mode.value,
            cls.clamp_u8(command.motor2.pwm),
            command.motor2.mode.value,
            relay_l,
            relay_h,
        ])
        return cls.TX_HEADER + payload

    @classmethod
    def decode_frame(cls, frame: bytes):
        if len(frame) != cls.RX_FRAME_SIZE:
            raise ValueError(f"Invalid RX frame length: {len(frame)}")

        if frame[:2] != cls.RX_HEADER:
            raise ValueError(f"Invalid RX frame header: {frame[:2]}")

        rpm1_raw = struct.unpack("<h", frame[2:4])[0]
        rpm2_raw = struct.unpack("<h", frame[4:6])[0]
        voltage_raw = struct.unpack("<H", frame[6:8])[0]
        generator_raw = struct.unpack("<H", frame[8:10])[0]

        return {
            "rpm1_raw": rpm1_raw,
            "rpm2_raw": rpm2_raw,
            "rpm1_display": abs(rpm1_raw) / cls.RPM_SCALE_LCD,
            "rpm2_display": abs(rpm2_raw) / cls.RPM_SCALE_LCD,
            "voltage_raw": voltage_raw,
            "generator_raw": generator_raw,
            "raw_frame_hex": " ".join(f"{b:02x}" for b in frame),
        }


# ============================================================
# SERIAL ADAPTER
# ============================================================

class ArduinoSerialAdapter:
    def __init__(
        self,
        port: str,
        baudrate: int = 115200,
        timeout: float = 0.02,
        heartbeat_interval_s: float = 0.05,
    ):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.heartbeat_interval_s = heartbeat_interval_s

        self._serial: Optional[serial.Serial] = None
        self._rx_buffer = bytearray()

        self._command = DeviceCommand()
        self._state = DeviceState()

        self._command_lock = threading.Lock()
        self._state_lock = threading.Lock()
        self._serial_lock = threading.Lock()

        self._worker_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._running = False

    # --------------------------------------------------------
    # Lifecycle
    # --------------------------------------------------------

    def connect(self) -> None:
        if self._serial and self._serial.is_open:
            return

        self._serial = serial.Serial(
            self.port,
            baudrate=self.baudrate,
            timeout=self.timeout
        )

        with self._state_lock:
            self._state.connected = True
            self._state.last_update_ts = time.time()

    def disconnect(self) -> None:
        self.stop_communication()

        if self._serial and self._serial.is_open:
            try:
                self._serial.close()
            finally:
                self._serial = None

        with self._state_lock:
            self._state.connected = False

    def start_communication(self) -> None:
        if self._running:
            return

        if not self._serial or not self._serial.is_open:
            raise RuntimeError("Serial port is not connected.")

        self._stop_event.clear()
        self._worker_thread = threading.Thread(
            target=self._worker_loop,
            name="ArduinoSerialAdapterWorker",
            daemon=True,
        )
        self._worker_thread.start()
        self._running = True

    def stop_communication(self) -> None:
        if not self._running:
            return

        self._stop_event.set()

        if self._worker_thread and self._worker_thread.is_alive():
            self._worker_thread.join(timeout=2.0)

        self._worker_thread = None
        self._running = False

        self.set_command(
            motor1_pwm=0,
            motor1_mode=MotorMode.BRAKE,
            motor2_pwm=0,
            motor2_mode=MotorMode.BRAKE,
            relay_on=False,
        )

        try:
            if self._serial and self._serial.is_open:
                self._send_current_command_once()
        except Exception:
            pass

    # --------------------------------------------------------
    # Public API for backend
    # --------------------------------------------------------

    def is_connected(self) -> bool:
        return bool(self._serial and self._serial.is_open)

    def is_running(self) -> bool:
        return self._running

    def set_motor1(self, pwm: int, mode: MotorMode) -> None:
        with self._command_lock:
            self._command.motor1.pwm = ArduinoProtocol.clamp_u8(pwm)
            self._command.motor1.mode = mode

        with self._state_lock:
            self._state.motor1.pwm = ArduinoProtocol.clamp_u8(pwm)
            self._state.motor1.mode = mode

    def set_motor2(self, pwm: int, mode: MotorMode) -> None:
        with self._command_lock:
            self._command.motor2.pwm = ArduinoProtocol.clamp_u8(pwm)
            self._command.motor2.mode = mode

        with self._state_lock:
            self._state.motor2.pwm = ArduinoProtocol.clamp_u8(pwm)
            self._state.motor2.mode = mode

    def set_relay(self, on: bool) -> None:
        with self._command_lock:
            self._command.relay_on = bool(on)

        with self._state_lock:
            self._state.relay_on = bool(on)

    def set_command(
        self,
        motor1_pwm: int,
        motor1_mode: MotorMode,
        motor2_pwm: int,
        motor2_mode: MotorMode,
        relay_on: bool,
    ) -> None:
        with self._command_lock:
            self._command.motor1.pwm = ArduinoProtocol.clamp_u8(motor1_pwm)
            self._command.motor1.mode = motor1_mode
            self._command.motor2.pwm = ArduinoProtocol.clamp_u8(motor2_pwm)
            self._command.motor2.mode = motor2_mode
            self._command.relay_on = bool(relay_on)

        with self._state_lock:
            self._state.motor1.pwm = ArduinoProtocol.clamp_u8(motor1_pwm)
            self._state.motor1.mode = motor1_mode
            self._state.motor2.pwm = ArduinoProtocol.clamp_u8(motor2_pwm)
            self._state.motor2.mode = motor2_mode
            self._state.relay_on = bool(relay_on)

    def stop_system(self) -> None:
        self.set_command(
            motor1_pwm=0,
            motor1_mode=MotorMode.BRAKE,
            motor2_pwm=0,
            motor2_mode=MotorMode.BRAKE,
            relay_on=False,
        )
        self._send_current_command_once()

    def get_state(self) -> DeviceState:
        with self._state_lock:
            return DeviceState(
                connected=self._state.connected,
                last_update_ts=self._state.last_update_ts,
                motor1=MotorState(
                    pwm=self._state.motor1.pwm,
                    mode=self._state.motor1.mode,
                    rpm_raw=self._state.motor1.rpm_raw,
                    rpm_display=self._state.motor1.rpm_display,
                ),
                motor2=MotorState(
                    pwm=self._state.motor2.pwm,
                    mode=self._state.motor2.mode,
                    rpm_raw=self._state.motor2.rpm_raw,
                    rpm_display=self._state.motor2.rpm_display,
                ),
                relay_on=self._state.relay_on,
                voltage_raw=self._state.voltage_raw,
                generator_raw=self._state.generator_raw,
                raw_frame_hex=self._state.raw_frame_hex,
            )

    # --------------------------------------------------------
    # Internal worker
    # --------------------------------------------------------

    def _worker_loop(self) -> None:
        last_send = 0.0

        while not self._stop_event.is_set():
            now = time.time()

            try:
                if now - last_send >= self.heartbeat_interval_s:
                    self._send_current_command_once()
                    last_send = now

                self._poll_rx_once()

            except Exception as exc:
                with self._state_lock:
                    self._state.connected = False
                print(f"[ArduinoSerialAdapter] worker error: {exc}")
                time.sleep(0.1)

            time.sleep(0.001)

    def _send_current_command_once(self) -> None:
        if not self._serial or not self._serial.is_open:
            return

        with self._command_lock:
            frame = ArduinoProtocol.encode_command(self._command)

        with self._serial_lock:
            self._serial.write(frame)

    def _poll_rx_once(self) -> None:
        if not self._serial or not self._serial.is_open:
            return

        with self._serial_lock:
            waiting = self._serial.in_waiting
            if waiting > 0:
                self._rx_buffer.extend(self._serial.read(waiting))

        frame = self._extract_frame_from_buffer()
        if frame is None:
            return

        decoded = ArduinoProtocol.decode_frame(frame)

        with self._state_lock:
            self._state.connected = True
            self._state.last_update_ts = time.time()
            self._state.motor1.rpm_raw = decoded["rpm1_raw"]
            self._state.motor1.rpm_display = decoded["rpm1_display"]
            self._state.motor2.rpm_raw = decoded["rpm2_raw"]
            self._state.motor2.rpm_display = decoded["rpm2_display"]
            self._state.voltage_raw = decoded["voltage_raw"]
            self._state.generator_raw = decoded["generator_raw"]
            self._state.raw_frame_hex = decoded["raw_frame_hex"]

    def _extract_frame_from_buffer(self) -> Optional[bytes]:
        while len(self._rx_buffer) >= ArduinoProtocol.RX_FRAME_SIZE:
            idx = self._rx_buffer.find(ArduinoProtocol.RX_HEADER)

            if idx < 0:
                self._rx_buffer = self._rx_buffer[-1:]
                return None

            if idx > 0:
                del self._rx_buffer[:idx]

            if len(self._rx_buffer) < ArduinoProtocol.RX_FRAME_SIZE:
                return None

            frame = bytes(self._rx_buffer[:ArduinoProtocol.RX_FRAME_SIZE])
            del self._rx_buffer[:ArduinoProtocol.RX_FRAME_SIZE]
            return frame

        return None