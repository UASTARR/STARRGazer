import math
import random
import threading
import time
from flask import Flask, jsonify, render_template
from flask_cors import CORS

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
    
    def get_acceleration(self):
        ax = round(random.uniform(-2, 2), 2)
        ay = round(random.uniform(-2, 2), 2)
        az = round(9.8 + random.uniform(-0.5, 0.5), 2)
        return ax, ay, az
 
    def get_magnetometer(self):
        mx = round(25.0 + math.sin(self.time_s * 0.1) * 2 + random.uniform(-0.5, 0.5), 2)
        my = round(12.0 + math.cos(self.time_s * 0.1) * 2 + random.uniform(-0.5, 0.5), 2)
        mz = round(-48.0 + random.uniform(-1, 1), 2)
        return mx, my, mz
 
    def get_quaternion(self):
        angle = self.time_s * 0.05
        qw = round(math.cos(angle / 2), 4)
        qx = round(math.sin(angle / 2) * 0.1, 4)
        qy = round(math.sin(angle / 2) * 0.2, 4)
        qz = round(math.sin(angle / 2) * 0.97, 4)
        return qw, qx, qy, qz
 
    def get_strain(self):
        return round(abs(math.sin(self.time_s * 0.3)) * 500 + random.uniform(-10, 10), 2)
 
    def generate_all(self):
        self.time_s += 1
        lat, lon = self.get_gps()
        roll, pitch, yaw = self.get_gyro()
        ax, ay, az = self.get_acceleration()
        mx, my, mz = self.get_magnetometer()
        qw, qx, qy, qz = self.get_quaternion()
 
        # field names match what backend.get_latest() returns
        # so swapping fake data for real data doesnt break anything
        return {
            "time":          self.time_s,
            "temperature":   self.get_temperature(),
            "pressure":      self.get_pressure(),
            "altitude":      self.get_altitude(),
            "ground_speed":  self.get_ground_speed(),
            "lat":           lat,
            "lon":           lon,
            "gyroscopex":    roll,
            "gyroscopey":    pitch,
            "gyroscopez":    yaw,
            "accelerationx": ax,
            "accelerationy": ay,
            "accelerationz": az,
            "magnetometerx": mx,
            "magnetometery": my,
            "magnetometerz": mz,
            "quaternionw":   qw,
            "quaternionx":   qx,
            "quaterniony":   qy,
            "quaternionz":   qz,
            "strain":        self.get_strain(),
        }
 
 
# Live test loop
if __name__ == "__main__":
    telem = FakeTelemetry()
 
    web_telem = FakeTelemetry()
    web_app = Flask(__name__)
    CORS(web_app)
 
    @web_app.route("/")
    def home():
        return render_template("home.html")
 
    @web_app.route("/telemetry")
    def telemetry():
        return jsonify(web_telem.generate_all())
 
    flask_thread = threading.Thread(
        target=lambda: web_app.run(port=5000, debug=False, use_reloader=False),
        daemon=True
    )
    flask_thread.start()
    print("dashboard at http://127.0.0.1:5000")
    print("ctrl+c to stop\n")
    
    while True:
        data = telem.generate_all()
        print(data)
        time.sleep(0.1)
