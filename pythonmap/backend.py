import threading
import time
import os
import serial
from datatypes import template, ids
import pyubx2

SERIAL_BAUDRATE = 115200
SERIAL_RECONNECT_DELAY = 3.0


class SerialReader(threading.Thread):
    def __init__(self, port=None, baudrate=SERIAL_BAUDRATE, socketio=None):
        super().__init__(daemon=True)
        self.port = port
        self.baudrate = baudrate
        self._stop = threading.Event()
        self._ser = None
        self._socketio = socketio
        self._save_buffer = []

    def set_socketio(self, socketio):
        """Set the SocketIO instance to emit messages."""
        self._socketio = socketio

    def connect(self):
        if self.port is None:
            return False
        try:
            self._save_thread = threading.Thread(
                target=self.save_data, daemon=True)
            self._save_thread.start()
            self._ser = serial.Serial(self.port, self.baudrate, timeout=1)
            print(f"Connected to serial port {self.port} @ {self.baudrate}")
            return True
        except Exception as e:
            print(f"Failed to open serial port {self.port}: {e}")
            self._ser = None
            return False

    def run(self):
        while not self._stop.is_set():
            if self._ser is None:
                if not self.connect():
                    time.sleep(SERIAL_RECONNECT_DELAY)
                    continue
            try:
                line = self._ser.readline()
                if not line:
                    continue
                try:
                    text = line.decode('utf-8', errors='replace').strip()
                except Exception:
                    text = repr(line)
                parsed = self.parse_line(text)
                # emit to clients
                self._socketio.emit('serial_data', parsed,
                                    namespace="/", broadcast=True)
                self._save_buffer.append(parsed)
            except Exception as e:
                print('Serial read error:', e)
                # on error, close and try reconnect
                try:
                    self._ser.close()
                except Exception:
                    pass
                self._ser = None
                time.sleep(SERIAL_RECONNECT_DELAY)

    def stop(self):
        self._stop.set()
        if self._ser and self._ser.is_open:
            try:
                self._ser.close()
                if hasattr(self, '_save_thread'):
                    self._save_thread.join(timeout=1)
            except Exception:
                pass

    def parse_line(self, line: str):
        # Data header (number of bytes), sensor_id (which sensor), timestamp, data.
        # header - 1 byte (how many bytes in the data)
        # sensor_id - 1 byte (which sensor sent the data)
        # timestamp - 4 bytes (unix timestamp)
        # data - variable length (depends on the sensor)
        # Example: b'\x0c\x01\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06'
        # All data is in raw binary format.
        if not line:
            return {}

        header = line[0:1]
        sensor_id = line[1:2]
        timestamp = line[2:6]
        data = line[6:header[0] + 6]
        try:
            sensor_id = int.from_bytes(sensor_id, 'big')
            timestamp = int.from_bytes(timestamp, 'big')
            data = data.decode('utf-8', errors='replace')
        except Exception as e:
            print(f"Error parsing line: {e}")
            return {}

        if sensor_id not in ids:
            print(f"Unknown sensor ID: {sensor_id}")
            return {}

        if sensor_id == ids['temperature']:
            return {
                "timestamp": timestamp,
                "ids": sensor_id,
                "temperature": float(data)
            }
        elif sensor_id == ids['acceleration']:
            values = list(map(float, data.split(',')))
            return {
                "timestamp": timestamp,
                "ids": sensor_id,
                "acceleration": values
            }
        elif sensor_id == ids['gyroscope']:
            values = list(map(float, data.split(',')))
            return {
                "timestamp": timestamp,
                "ids": sensor_id,
                "gyroscope": values
            }
        elif sensor_id == ids['magnetometer']:
            values = list(map(float, data.split(',')))
            return {
                "timestamp": timestamp,
                "ids": sensor_id,
                "magnetometer": values
            }
        elif sensor_id == ids['quaternion']:
            values = list(map(float, data.split(',')))
            return {
                "timestamp": timestamp,
                "ids": sensor_id,
                "quaternion": values
            }
        elif sensor_id == ids['gps']:
            try:
                parsed_data = pyubx2.UBXMessage.parse(
                    data, msgmode=pyubx2.NMEA)
                if parsed_data.msgID == "GGA":
                    return {
                        "timestamp": timestamp,
                        "ids": sensor_id,
                        "lat": parsed_data.lat,
                        "lon": parsed_data.lon,
                        "alt": parsed_data.alt,
                        "gpsfix": parsed_data.gpsfix,
                        "nsats": parsed_data.numSV,
                    }
                elif parsed_data.msgID == "GNS":
                    return {
                        "timestamp": timestamp,
                        "ids": sensor_id,
                        "lat": parsed_data.lat,
                        "lon": parsed_data.lon,
                        "alt": parsed_data.alt,
                        "gpsfix": parsed_data.fixType,
                        "nsats": parsed_data.numSV,
                    }
                elif parsed_data.msgID == "VTG":
                    return {
                        "timestamp": timestamp,
                        "ids": sensor_id,
                        "hspeed": parsed_data.spdOverGrndKmph,
                        "heading": parsed_data.cogTrue,
                    }
                elif parsed_data.msgID == "RMC":
                    return {
                        "timestamp": timestamp,
                        "ids": sensor_id,
                        "lat": parsed_data.lat,
                        "lon": parsed_data.lon,
                        "hspeed": parsed_data.spdOverGrndKmph,
                        "heading": parsed_data.cogTrue,
                    }
                else:
                    print(f"Unhandled NMEA message type: {parsed_data.msgID}")
                    return {}
            except Exception as e:
                print(f"Error parsing GPS data: {e}")
                return {}
        elif sensor_id == ids['strain']:
            return {
                "timestamp": timestamp,
                "ids": sensor_id,
                "strain": float(data)
            }
        else:
            print(f"Unhandled sensor ID: {sensor_id}")
            return {}

    def save_data(self):
        """Save the buffered data to a file or database."""
        path = os.path.join('records', f'serial_data_{time.time()}.txt')
        os.makedirs('records', exist_ok=True)
        try:
            while self._ser and self._ser.is_open:
                if self._save_buffer:
                    entry = self._save_buffer.pop(0)
                    with open(path, 'a') as f:
                        entry_str = ', '.join(
                            f'{k}={v}' for k, v in entry.items())
                        f.write(entry_str + '\n')
        except Exception as e:
            print(f"Failed to save serial data: {e}")
