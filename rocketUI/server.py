from flask import Flask, jsonify, render_template
from flask_cors import CORS
import time
import random

app = Flask(__name__)
CORS(app)  # allow your JS to fetch from localhost

last_altitude = 120.0

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/telemetry")
def telemetry():
    global last_altitude

    current_time = int(time.time())

    # produce a smooth altitude drift
    last_altitude += random.uniform(-0.5, 0.5)

    temperature = round(random.uniform(22, 26), 1)
    ground_speed = random.randint(3, 8)
    pressure = round(1013 + random.uniform(-2, 2), 1)

    roll = round(random.gauss(0, 1), 2)
    pitch = round(random.gauss(0, 1), 2)
    yaw = round(random.gauss(0, 1), 2)

    data = {
        "time": current_time,
        "temperature": temperature,
        "altitude": round(last_altitude, 1),
        "ground_speed": ground_speed,
        "pressure": pressure,
        "gyro": [roll, pitch, yaw],
        "gps": [53.535, -113.501]
    }
    
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
