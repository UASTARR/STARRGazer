template = {
    "timestamp": float,
    "lat": float,
    "lon": float,
    "alt": float,
    "gpsfix": float,
    "nsats": float,
    "quaternion": list[float],  # [w, x, y, z]
    "acceleration": list[float],  # [x, y, z]
    "gyroscope": list[float],  # [x, y, z]
    "magnetometer": list[float],  # [x, y, z]
    "strain": float,
    "temperature": float,
}

ids = {
    "temperature": 0,       # Temperature sensor
    "acceleration": 1,      # Gyro x, gryo y, gyro z
    "gyroscope": 2,         # Accelerometer x, y, z
    "magnetometer": 3,      # Magnetometer x, y, z
    "quaternion": 4,        # quat w, x, y, z
    "gps": 5,               # lat, lon, alt, hspeed, vspeed, heading
    "strain": 6,            # Strain sensor
    "motherboard": 7,
}
