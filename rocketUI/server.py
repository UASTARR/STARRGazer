from flask import Flask, jsonify, render_template, send_from_directory, send_file
from fake_date_generator import FakeTelemetry  # your Python script
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # allow your JS to fetch from localhost
telem = FakeTelemetry()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/wireless_arming")
def wireless_arming():
    return render_template("wireless_arming.html")

@app.route('/manifest.json')
def serve_manifest():
    return send_file('manifest.json', mimetype='application/manifest+json')

@app.route('/sw.js')
def serve_sw():
    return send_file('sw.js', mimetype='application/javascript')

@app.route("/telemetry")
def telemetry():
    data = telem.generate_all()
    return jsonify(data)

if __name__ == "__main__":
    app.run('0.0.0.0', debug=True)
