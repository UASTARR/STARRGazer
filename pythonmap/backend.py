import threading
import time
import os
import serial
from datatypes import ids
import pyubx2
from datetime import datetime

SERIAL_BAUDRATE = 9600
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

        date_str = datetime.now().strftime("%Y_%m_%d")
        base_filename = f"{date_str}.txt"
        self.savepath = os.path.join("records", base_filename)

        # Ensure uniqueness by adding _0, _1, etc.
        counter = 0
        while os.path.exists(self.savepath):
            self.savepath = os.path.join(
                "records", f"{date_str}_{counter}.txt")
            counter += 1

        print(f"Saving to: {self.savepath}")
        os.makedirs('records', exist_ok=True)

    def set_socketio(self, socketio):
        """Set the SocketIO instance to emit messages."""
        self._socketio = socketio

    def connect(self):
        if self.port is None:
            return False
        try:
            self._ser = serial.Serial(self.port, self.baudrate, timeout=1)
            self._save_thread = threading.Thread(
                target=self.save_data, daemon=True)
            self._save_thread.start()
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
                self._save_buffer.append(text)
                parsed = self.parse_line(text)
                print(parsed)
                # emit to clients
                self._socketio.emit('serial_data', parsed,
                                    namespace="/")
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

    def parse_line(self, line):
        # Data header (number of bytes), sensor_id (which sensor), timestamp, data.
        # header - 1 byte (how many bytes in the data)
        # sensor_id - 1 byte (which sensor sent the data)
        # timestamp - 4 bytes (unix timestamp)
        # data - variable length (depends on the sensor)
        # Example: b'\x0c\x01\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06'
        # All data is in raw binary format.
        if not line:
            return {}

        line = line.split(',')
        header = line[0]
        sensor_id = line[1]
        timestamp = line[2]
        data = line[3:]
        # print(f"Raw line: {line}")
        try:
            # Convert binary string fields to integers safely
            header = int(header) if header else 0
            sensor_id = int(sensor_id) if sensor_id else 0
            timestamp = float(timestamp) if timestamp else 0
            for i in range(len(data)):
                data[i] = float(data[i]) if data[i] else 0
            # print(
                # f"Parsed header: {header}, sensor_id: {sensor_id}, timestamp: {timestamp}, data: {data}")
        except Exception as e:
            print(f"Error parsing line: {e}")
            return {}

        if sensor_id not in ids.values():
            print(f"Unknown sensor ID: {sensor_id}")
            return {}

        if sensor_id == ids['temperature']:
            return {
                "timestamp": timestamp,
                "ids": sensor_id,
                "temperature": data[0],
                "pressure": data[1]
            }
        elif sensor_id == ids['acceleration']:
            return {
                "timestamp": timestamp,
                "ids": sensor_id,
                "accelerationx": data[0],
                "accelerationy": data[1],
                "accelerationz": data[2],

            }
        elif sensor_id == ids['gyroscope']:
            return {
                "timestamp": timestamp,
                "ids": sensor_id,
                "gyroscopex": data[0],
                "gyroscopey": data[1],
                "gyroscopez": data[2],
            }
        elif sensor_id == ids['magnetometer']:
            return {
                "timestamp": timestamp,
                "ids": sensor_id,
                "magnetometerx": data[0],
                "magnetometery": data[1],
                "magnetometerz": data[2],

            }
        elif sensor_id == ids['quaternion']:
            return {
                "timestamp": timestamp,
                "ids": sensor_id,
                "quaternionx": data[0],
                "quaterniony": data[1],
                "quaternionz": data[2],
                "quaternionw": data[3],
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
                else:
                    print(f"Unhandled NMEA message type: {parsed_data.msgID}")
                    return {}
            except Exception as e:
                print(f"Error parsing GPS data: {e}")
                return {}
        elif sensor_id == ids['strain']:
            try:
                return_thing = {
                    "timestamp": timestamp,
                    "ids": sensor_id,
                    "strain1": data[0],
                    "strain2": data[1],
                }
            except Exception as e:
                print(f"Error parsing strain data: {e}")
                return {}

            return return_thing
        else:
            print(f"Unhandled sensor ID: {sensor_id}")
            return {}

    def save_data(self):
        """Save the buffered data to a file or database."""
        try:
            while self._ser and self._ser.is_open:
                if self._save_buffer:
                    entry = self._save_buffer.pop(0)
                    with open(self.savepath, 'a') as f:
                        f.write(entry + '\n')
        except Exception as e:
            print(f"Failed to save serial data: {e}")
