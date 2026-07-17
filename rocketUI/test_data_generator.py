# generates fake packets to test the parser with
# run this first then run test_backend.py
#
# makes 3 files in records/:
#   test_single.txt  - one packet per sensor
#   test_flight.txt  - 100 packets like a real flight
#   test_bad.txt     - broken packets to make sure nothing crashes
 
import struct
import math
import os
 
os.makedirs("records", exist_ok=True)
 
# has to match datatypes.py
ADDR_TEMPERATURE  = 0x0001
ADDR_PRESSURE     = 0x0002
ADDR_ALTITUDE     = 0x0003
ADDR_ACCELERATION = 0x0004
ADDR_GYROSCOPE    = 0x0005
ADDR_MAGNETOMETER = 0x0006
ADDR_QUATERNION   = 0x0007
ADDR_GPS          = 0x0008
ADDR_GROUND_SPEED = 0x0009
ADDR_STRAIN       = 0x000A
 
PACKET_SIZE  = 128
PAYLOAD_SIZE = 124
 
 
def make_entry(address, values, value_type="uint32"):
    if value_type == "uint32":
        fmt_char = "I"
    elif value_type == "uint16":
        fmt_char = "H"
    elif value_type == "float32":
        fmt_char = "f"
 
    data = struct.pack("<" + fmt_char * len(values), *values)
    header = struct.pack("<HB", address, len(data))
    return header + data
 
 
def make_packet(entries, timestamp_ms):
    payload = b"".join(entries)
 
    if len(payload) > PAYLOAD_SIZE:
        raise ValueError(f"too much data: {len(payload)} bytes")
 
    payload = payload.ljust(PAYLOAD_SIZE, b"\x00")
    packet = payload + struct.pack("<I", timestamp_ms)
    return packet
 
 
# fake sensor data
# using abs() everywhere because uint32 cant be negative
 
def sim_temperature(t):
    temp = 20.0 + 15.0 * math.sin(math.pi * t)
    return [int(abs(temp * 100))]
 
def sim_pressure(t):
    return [int(abs(101325.0 - 5000.0 * math.sin(math.pi * t)))]
 
def sim_altitude(t):
    return [int(max(0.0, 3000.0 * math.sin(math.pi * t)) * 100)]
 
def sim_acceleration(t):
    vibe = 200 * math.sin(math.pi * t * 20)
    return [int(abs(100 + vibe)), int(abs(50 + vibe * 0.5)), int(abs(5000 * math.sin(math.pi * t) + 980))]
 
def sim_gyroscope(t):
    phase = math.pi * t
    return [int(abs(50 * math.sin(phase * 3))), int(abs(30 * math.sin(phase * 2 + 0.5))), int(abs(100 * math.sin(phase * 1.5)))]
 
def sim_magnetometer(t):
    phase = math.pi * t
    return [int(abs(2500 + 500 * math.cos(phase * 4))), int(abs(1200 + 300 * math.sin(phase * 4))), 4800]
 
def sim_quaternion(t):
    angle = math.pi * t * 0.5
    return [int(abs(math.cos(angle / 2) * 10000)), int(abs(math.sin(angle / 2) * 0.1 * 10000)),
            int(abs(math.sin(angle / 2) * 0.2 * 10000)), int(abs(math.sin(angle / 2) * 0.97 * 10000))]
 
def sim_gps(t):
    lat = int(abs((53.5232 + 0.001 * math.sin(math.pi * t)) * 1e7))
    lon = int(abs((113.5263 - 0.001 * t) * 1e7))
    return [lat, lon, int(sim_altitude(t)[0])]
 
def sim_ground_speed(t):
    return [int(max(0.0, 300.0 * math.sin(math.pi * t)) * 100)]
 
def sim_strain(t):
    return [int(5000 * abs(math.sin(math.pi * t * 2)))]
 
 
# test_single.txt - one sensor per packet
print("making test_single.txt...")
single = [
    make_packet([make_entry(ADDR_TEMPERATURE,  [2087])],                          timestamp_ms=1000),
    make_packet([make_entry(ADDR_PRESSURE,     [101325])],                        timestamp_ms=1100),
    make_packet([make_entry(ADDR_ALTITUDE,     [300000])],                        timestamp_ms=1200),
    make_packet([make_entry(ADDR_ACCELERATION, [100, 50, 1080])],                 timestamp_ms=1300),
    make_packet([make_entry(ADDR_GYROSCOPE,    [30, 10, 200])],                   timestamp_ms=1400),
    make_packet([make_entry(ADDR_MAGNETOMETER, [2500, 1200, 4800])],              timestamp_ms=1500),
    make_packet([make_entry(ADDR_QUATERNION,   [10000, 0, 0, 0])],                timestamp_ms=1600),
    make_packet([make_entry(ADDR_GPS,          [535232000, 1135263000, 300000])], timestamp_ms=1700),
    make_packet([make_entry(ADDR_GROUND_SPEED, [15000])],                         timestamp_ms=1800),
    make_packet([make_entry(ADDR_STRAIN,       [2500])],                          timestamp_ms=1900),
]
with open("records/test_single.txt", "w") as f:
    for p in single:
        f.write(p.hex() + "\n")
print(f"wrote {len(single)} packets")
 
 
# test_flight.txt - 100 packets, sensors update at different rates like a real flight
print("making test_flight.txt...")
flight = []
for i in range(100):
    t = i / 100.0
    entries = []
 
    if i % 5 == 0:
        entries.append(make_entry(ADDR_TEMPERATURE,  sim_temperature(t)))
        entries.append(make_entry(ADDR_PRESSURE,     sim_pressure(t)))
    if i % 3 == 0:
        entries.append(make_entry(ADDR_ALTITUDE,     sim_altitude(t)))
 
    entries.append(make_entry(ADDR_ACCELERATION, sim_acceleration(t)))
    entries.append(make_entry(ADDR_GYROSCOPE,    sim_gyroscope(t)))
 
    if i % 2 == 0:
        entries.append(make_entry(ADDR_MAGNETOMETER, sim_magnetometer(t)))
    if i % 2 == 1:
        entries.append(make_entry(ADDR_QUATERNION,   sim_quaternion(t)))
    if i % 10 == 0:
        entries.append(make_entry(ADDR_GPS,          sim_gps(t)))
        entries.append(make_entry(ADDR_GROUND_SPEED, sim_ground_speed(t)))
    if i % 4 == 0:
        entries.append(make_entry(ADDR_STRAIN,       sim_strain(t)))
 
    flight.append(make_packet(entries, i * 100))
 
with open("records/test_flight.txt", "w") as f:
    for p in flight:
        f.write(p.hex() + "\n")
print(f"wrote {len(flight)} packets")
 
 
# test_bad.txt - broken packets, parser shouldnt crash on any of these
print("making test_bad.txt...")
bad = []
 
# all zeros
bad.append(bytes(128))
 
# unknown address
payload = struct.pack("<HB", 0xFFFF, 4) + struct.pack("<I", 99999)
bad.append(payload.ljust(PAYLOAD_SIZE, b"\x00") + struct.pack("<I", 5000))
 
# length too big
payload = struct.pack("<HB", ADDR_TEMPERATURE, 120) + bytes(10)
bad.append(payload.ljust(PAYLOAD_SIZE, b"\x00") + struct.pack("<I", 6000))
 
# right address wrong size
payload = struct.pack("<HB", ADDR_TEMPERATURE, 7) + bytes(7)
bad.append(payload.ljust(PAYLOAD_SIZE, b"\x00") + struct.pack("<I", 7000))
 
# valid + unknown + valid mixed together
entries = [
    make_entry(ADDR_TEMPERATURE, [2500]),
    struct.pack("<HBI", 0xBEEF, 4, 0),
    make_entry(ADDR_ACCELERATION, [100, 50, 1080]),
]
bad.append(make_packet(entries, 8000))
 
with open("records/test_bad.txt", "w") as f:
    for p in bad:
        f.write(p.hex() + "\n")
print(f"wrote {len(bad)} packets")
 
print("\ndone, run test_backend.py next")