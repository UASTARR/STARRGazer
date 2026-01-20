from flask import Flask, jsonify, render_template, send_from_directory
from fake_date_generator import FakeTelemetry  # your Python script
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # allow your JS to fetch from localhost
telem = FakeTelemetry()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/telemetry")
def telemetry():
    data = telem.generate_all()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
