# backend.py
# reads packets from the serial port and stores the latest sensor values
# runs in a background thread so it doesnt block the web server
#
# packet layout (128 bytes):
#   bytes 0-123  -> sensor entries back to back
#   bytes 124-127 -> uint32 timestamp (ms since startup)
#
# each sensor entry looks like:
#   [address: 2 bytes][length: 1 byte][data: N bytes]
#
# to use this in server.py:
#   telem = SerialBackend(port="COM3")
#   telem.start()
#   data = telem.get_latest()
 
import threading
import time
import os
import struct
import serial
from datatypes import SENSORS
from datetime import datetime
 
PACKET_SIZE = 128
PAYLOAD_SIZE = 124        # 128 - 4 bytes for the timestamp at the end
ENTRY_HEADER = 3          # 2 byte address + 1 byte length
 
BAUDRATE = 115200
RECONNECT_WAIT = 3.0      # seconds to wait before trying to reconnect
 
# how many bytes each value type takes up
BYTES_PER_TYPE = {
    "uint32":  4,
    "uint16":  2,
    "float32": 4,
}
 
# struct format character for each type
# < means little endian which is standard for most microcontrollers
STRUCT_CHAR = {
    "uint32":  "I",
    "uint16":  "H",
    "float32": "f",
}
 
 
class SerialBackend(threading.Thread):
    # reads from serial in the background and keeps _latest updated
    # server.py calls get_latest() whenever the browser asks for data
 
    def __init__(self, port=None, baudrate=BAUDRATE):
        super().__init__(daemon=True)
 
        self.port = port
        self.baudrate = baudrate
        self._ser = None
        self._stop = threading.Event()
        self._lock = threading.Lock()
        self._save_buffer = []
 
        # fill _latest with None for every field so get_latest()
        # always returns something even before any packets arrive
        self._latest = {"time": 0}
        for sensor in SENSORS.values():
            for field in sensor["fields"]:
                self._latest[field] = None
 
        # make a save file with todays date, add a number if it already exists
        date = datetime.now().strftime("%Y_%m_%d")
        self.savepath = os.path.join("records", f"{date}.txt")
        n = 0
        while os.path.exists(self.savepath):
            self.savepath = os.path.join("records", f"{date}_{n}.txt")
            n += 1
        os.makedirs("records", exist_ok=True)
        print(f"saving to {self.savepath}")
 
    def get_latest(self):
        # called by server.py to get the current sensor readings
        # the lock makes sure we dont read while the thread is writing
        with self._lock:
            return dict(self._latest)
 
    def stop(self):
        self._stop.set()
        if self._ser and self._ser.is_open:
            try:
                self._ser.close()
            except:
                pass
 
    def connect(self):
        # try to open the serial port, return True if it worked
        if self.port is None:
            print("no port set, running without hardware")
            return False
        try:
            self._ser = serial.Serial(self.port, self.baudrate, timeout=2)
            # start the save thread once connected
            threading.Thread(target=self._save_data, daemon=True).start()
            print(f"connected to {self.port}")
            return True
        except Exception as e:
            print(f"couldnt open {self.port}: {e}")
            self._ser = None
            return False
 
    def run(self):
        # main loop, keeps reading packets until stopped
        # if something goes wrong it tries to reconnect after a delay
        while not self._stop.is_set():
            if self._ser is None:
                if not self.connect():
                    time.sleep(RECONNECT_WAIT)
                    continue
 
            try:
                # read exactly 128 bytes, this blocks until they all arrive
                raw = self._ser.read(PACKET_SIZE)
 
                if len(raw) != PACKET_SIZE:
                    print(f"short packet: {len(raw)} bytes, skipping")
                    continue
 
                self._save_buffer.append(raw.hex())
 
                parsed = self._parse_packet(raw)
                if parsed:
                    self._update_latest(parsed)
 
            except Exception as e:
                print(f"read error: {e}, reconnecting in {RECONNECT_WAIT}s")
                try:
                    self._ser.close()
                except:
                    pass
                self._ser = None
                time.sleep(RECONNECT_WAIT)
 
    def _parse_packet(self, packet):
        # walk through the payload reading one sensor entry at a time
        # each entry is [address: 2][length: 1][data: N]
        # stop when we hit address 0x0000 (zero padding at end of payload)
        # last 4 bytes are always the timestamp
        result = {}
        offset = 0
 
        while offset + ENTRY_HEADER <= PAYLOAD_SIZE:
            address = struct.unpack_from("<H", packet, offset)[0]
 
            # 0x0000 means the rest is just padding, nothing left to read
            if address == 0x0000:
                break
 
            data_len = struct.unpack_from("<B", packet, offset + 2)[0]
            data_start = offset + ENTRY_HEADER
            data_end = data_start + data_len
 
            if data_end > PAYLOAD_SIZE:
                print(f"entry at {offset} claims {data_len} bytes but that goes past end of payload")
                break
 
            sensor = SENSORS.get(address)
            if sensor is None:
                print(f"unknown address 0x{address:04X}, skipping {data_len} bytes")
                offset = data_end
                continue
 
            decoded = self._unpack_values(packet[data_start:data_end], sensor, address)
            if decoded:
                result.update(decoded)
                print(f"0x{address:04X} ({sensor['name']}) -> {decoded}")
 
            offset = data_end
 
        # grab the timestamp from the last 4 bytes
        result["time"] = struct.unpack_from("<I", packet, PAYLOAD_SIZE)[0]
        return result
 
    def _unpack_values(self, data_bytes, sensor, address):
        # turn the raw bytes into a dict of field_name -> value
        fields = sensor["fields"]
        vtype = sensor["value_type"]
 
        nbytes = BYTES_PER_TYPE.get(vtype)
        char = STRUCT_CHAR.get(vtype)
 
        if nbytes is None:
            print(f"unknown value_type {vtype}")
            return {}
 
        expected = nbytes * len(fields)
        if len(data_bytes) != expected:
            print(f"size mismatch for 0x{address:04X}: expected {expected} bytes, got {len(data_bytes)}")
            return {}
 
        try:
            values = struct.unpack("<" + char * len(fields), data_bytes)
        except struct.error as e:
            print(f"unpack failed for 0x{address:04X}: {e}")
            return {}
 
        return dict(zip(fields, values))
 
    def _update_latest(self, parsed):
        # write new values into _latest
        # lock so the web server cant read half-written data
        with self._lock:
            self._latest.update(parsed)
 
    def _save_data(self):
        # runs in its own thread, writes packets to the record file
        while self._ser and self._ser.is_open:
            if self._save_buffer:
                entry = self._save_buffer.pop(0)
                try:
                    with open(self.savepath, "a") as f:
                        f.write(entry + "\n")
                except Exception as e:
                    print(f"save error: {e}")
            else:
                time.sleep(0.05)