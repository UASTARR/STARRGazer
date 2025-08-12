import sqlite3
import io
from flask import Flask, send_file, render_template, jsonify, abort
from flask_socketio import SocketIO, emit
import serial
import serial.tools.list_ports
import os
from backend import SerialReader
from datatypes import ids

app = Flask(__name__)

# Config
MBTILES_PATH = os.path.join(
    'assets', 'timmins.mbtiles')  # put your MBTiles here
SERIAL_BAUDRATE = 115200
SERIAL_RECONNECT_DELAY = 3.0

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')
serial_reader = None


@app.route('/')
def index():
    return render_template('index.html')


def get_tile(z, x, y):
    # MBTiles uses TMS scheme, Leaflet uses XYZ — flip y
    y_tms = (2**z - 1) - y
    conn = sqlite3.connect(MBTILES_PATH)
    cur = conn.cursor()
    cur.execute("SELECT tile_data FROM tiles WHERE zoom_level=? AND tile_column=? AND tile_row=?",
                (z, x, y_tms))
    row = cur.fetchone()
    conn.close()
    if row:
        return io.BytesIO(row[0])
    return None


@app.route("/tiles/<int:z>/<int:x>/<int:y>.png")
def tiles(z, x, y):
    tile = get_tile(z, x, y)
    if tile:
        return send_file(tile, mimetype="image/png")
    else:
        abort(404)


@app.route('/ports')
def ports():
    ports = [p.device for p in serial.tools.list_ports.comports()]
    print('Available serial ports:', ports)
    return jsonify(ports=ports)


@app.route('/ids')
def func_ids():
    return jsonify(id=ids)


@socketio.on('connect')
def handle_connect():
    print('Client connected')


@socketio.on('start_serial')
def handle_start_serial(data):
    # data expected: {'port': '/dev/ttyUSB0', 'baudrate': 115200}
    port = data.get('port')
    baud = int(data.get('baudrate', SERIAL_BAUDRATE))
    global serial_reader
    # stop existing
    if serial_reader is not None:
        if serial_reader.is_alive():
            serial_reader.stop()
    print(port, baud)
    serial_reader = SerialReader(port=port, baudrate=baud, socketio=socketio)
    serial_reader.start()
    emit('serial_started', {'port': port, 'baudrate': baud})


@socketio.on('stop_serial')
def handle_stop_serial():
    global serial_reader
    if serial_reader:
        serial_reader.stop()
    emit('serial_stopped')


if __name__ == '__main__':
    # ensure assets exist
    if not os.path.exists('assets'):
        os.makedirs('assets')
    print('Starting server on http://localhost:5000')
    # Use eventlet for websocket support
    socketio.run(app, host='0.0.0.0', port=5000)
