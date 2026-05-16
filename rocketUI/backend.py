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
import struct
import serial
from datatypes import SENSORS
 
PACKET_SIZE  = 128
PAYLOAD_SIZE = 124
ENTRY_HEADER = 3
 
BAUDRATE       = 115200
RECONNECT_WAIT = 3.0
 
BYTES_PER_TYPE = {
    "uint32":  4,
    "uint16":  2,
    "float32": 4,
}
 
STRUCT_CHAR = {
    "uint32":  "I",
    "uint16":  "H",
    "float32": "f",
}
 
 
class SerialBackend(threading.Thread):
 
    def __init__(self, port=None, baudrate=BAUDRATE):
        super().__init__(daemon=True)
 
        self.port     = port
        self.baudrate = baudrate
        self._ser     = None
        self._stop    = threading.Event()
        self._lock    = threading.Lock()
 
        # fill with None so get_latest() always returns something
        self._latest = {"time": 0}
        for sensor in SENSORS.values():
            for field in sensor["fields"]:
                self._latest[field] = None
 
    def get_latest(self):
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
        if self.port is None:
            print("no port set, running without hardware")
            return False
        try:
            self._ser = serial.Serial(self.port, self.baudrate, timeout=2)
            print(f"connected to {self.port}")
            return True
        except:
            print(f"couldnt open {self.port}")
            self._ser = None
            return False
 
    def run(self):
        while not self._stop.is_set():
            if self._ser is None:
                if not self.connect():
                    time.sleep(RECONNECT_WAIT)
                    continue
 
            try:
                raw = self._ser.read(PACKET_SIZE)
 
                if len(raw) != PACKET_SIZE:
                    print(f"short packet: {len(raw)} bytes, skipping")
                    continue
 
                parsed = self._parse_packet(raw)
                if parsed:
                    self._update_latest(parsed)
 
            except:
                print(f"read error, reconnecting in {RECONNECT_WAIT}s")
                try:
                    self._ser.close()
                except:
                    pass
                self._ser = None
                time.sleep(RECONNECT_WAIT)
 
    def _parse_packet(self, packet):
        result = {}
        offset = 0
 
        while offset + ENTRY_HEADER <= PAYLOAD_SIZE:
            address = struct.unpack_from("<H", packet, offset)[0]
 
            if address == 0x0000:
                break
 
            data_len   = struct.unpack_from("<B", packet, offset + 2)[0]
            data_start = offset + ENTRY_HEADER
            data_end   = data_start + data_len
 
            if data_end > PAYLOAD_SIZE:
                print(f"entry at {offset} goes past end of payload")
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
 
        result["time"] = struct.unpack_from("<I", packet, PAYLOAD_SIZE)[0]
        return result
 
    def _unpack_values(self, data_bytes, sensor, address):
        fields = sensor["fields"]
        vtype  = sensor["value_type"]
        nbytes = BYTES_PER_TYPE.get(vtype)
        char   = STRUCT_CHAR.get(vtype)
 
        if nbytes is None:
            print(f"unknown value_type {vtype}")
            return {}
 
        expected = nbytes * len(fields)
        if len(data_bytes) != expected:
            print(f"size mismatch for 0x{address:04X}: expected {expected} bytes, got {len(data_bytes)}")
            return {}
 
        try:
            values = struct.unpack("<" + char * len(fields), data_bytes)
        except:
            print(f"unpack failed for 0x{address:04X}")
            return {}
 
        return dict(zip(fields, values))
 
    def _update_latest(self, parsed):
        with self._lock:
            self._latest.update(parsed)