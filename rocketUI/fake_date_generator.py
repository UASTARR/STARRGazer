import math
import random
import time

class FakeTelemetry:
    def __init__(self):
        self.time_s = 0
        
        # Starting reference values
        self.base_temp = 25
        self.base_alt = 120  # meters
        self.base_speed = 10 # m/s (36 km/h)
        self.base_pressure = 1013.25
        self.lat = 43.6532  # Example: Toronto
        self.lon = -79.3832

    def get_temperature(self):
        noise = (random.random() - 0.5) * 2
        trend = math.sin(self.time_s * 0.1) * 3
        return round(self.base_temp + noise + trend, 2)

    def get_altitude(self):
        drift = math.sin(self.time_s * 0.02) * 2
        noise = (random.random() - 0.5) * 0.5
        return round(self.base_alt + drift + noise, 2)

    def get_ground_speed(self):
        accel = math.sin(self.time_s * 0.05) * 2
        noise = (random.random() - 0.5) * 0.8
        return round(max(0, self.base_speed + accel + noise), 2)

    def get_pressure(self):
        weather_variation = math.sin(self.time_s * 0.005) * 1.5
        noise = (random.random() - 0.5) * 0.4
        return round(self.base_pressure + weather_variation + noise, 2)

    def get_gps(self):
        # Simulate small movement based on ground speed
        speed = self.get_ground_speed() / 100000  # convert to degree shift
        self.lat += speed * math.cos(self.time_s * 0.01)
        self.lon += speed * math.sin(self.time_s * 0.01)
        return round(self.lat, 6), round(self.lon, 6)

    def get_gyro(self):
        roll = round(math.sin(self.time_s * 0.4) * 45 + random.uniform(-3, 3), 2)
        pitch = round(math.sin(self.time_s * 0.3) * 30 + random.uniform(-2, 2), 2)
        yaw = round(math.sin(self.time_s * 0.2) * 60 + random.uniform(-4, 4), 2)
        return roll, pitch, yaw

    def generate_all(self):
        self.time_s += 1
        return {
            "time": self.time_s,
            "temperature": self.get_temperature(),
            "altitude": self.get_altitude(),
            "ground_speed": self.get_ground_speed(),
            "pressure": self.get_pressure(),
            "gps": self.get_gps(),
            "gyro": self.get_gyro()
        }


# Live test loop
if __name__ == "__main__":
    telem = FakeTelemetry()
    while True:
        data = telem.generate_all()
        print(data)
        time.sleep(0.1)
