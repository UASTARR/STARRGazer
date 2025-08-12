import sqlite3
import io
from flask import Flask, send_file, render_template, jsonify, abort, request
from flask_socketio import SocketIO, emit
import serial
import serial.tools.list_ports
import os
from backend import SerialReader
from datatypes import ids

app = Flask(__name__)

# Config
MBTILES_PATH = os.path.join('assets', 'timmins.mbtiles')
SERIAL_BAUDRATE = 115200
SERIAL_RECONNECT_DELAY = 3.0

socketio = SocketIO(app, cors_allowed_origins='*')
serial_reader = None

connected_clients = set()
client_roles = {}  # { sid: "admin" or "user" }


@app.route('/')
def index():
    return render_template('index.html')


def get_tile(z, x, y):
    y_tms = (2**z - 1) - y
    conn = sqlite3.connect(MBTILES_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT tile_data FROM tiles WHERE zoom_level=? AND tile_column=? AND tile_row=?",
        (z, x, y_tms)
    )
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
    sid = request.sid
    client_ip = request.remote_addr
    connected_clients.add(sid)

    # Determine if client is admin
    if client_ip in ("127.0.0.1", "::1"):  # IPv4 and IPv6 localhost
        client_roles[sid] = "admin"
    else:
        client_roles[sid] = "user"

    print(f"Client connected: {sid} from {client_ip} as {client_roles[sid]}")
    emit('connected', {'sid': sid, 'role': client_roles[sid]})


@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    connected_clients.discard(sid)
    client_roles.pop(sid, None)
    print(f"Client disconnected: {sid}")


@socketio.on('start_serial')
def handle_start_serial(data):
    global serial_reader
    sid = request.sid

    # Only admin can start
    if client_roles.get(sid) != "admin":
        emit(
            'error', {'message': 'Permission denied: Only admin can start serial'})
        return

    port = data.get('port')
    baud = int(data.get('baudrate', SERIAL_BAUDRATE))

    if serial_reader is not None and serial_reader.is_alive():
        print(
            f"Serial already running on {serial_reader.port}, adding client {sid}")
        connected_clients.add(sid)
        emit('serial_started', {
            'port': serial_reader.port,
            'baudrate': serial_reader.baudrate
        })
        return

    print(f"Starting new serial reader on {port} at {baud}")
    serial_reader = SerialReader(port=port, baudrate=baud, socketio=socketio)
    serial_reader.start()
    connected_clients.add(sid)
    emit('serial_started', {'port': port, 'baudrate': baud})


@socketio.on('stop_serial')
def handle_stop_serial():
    global serial_reader
    sid = request.sid

    # Only admin can stop
    if client_roles.get(sid) != "admin":
        emit(
            'error', {'message': 'Permission denied: Only admin can stop serial'})
        return

    if serial_reader:
        serial_reader.stop()
    emit('serial_stopped')


if __name__ == '__main__':
    if not os.path.exists('assets'):
        os.makedirs('assets')
    print('Starting server on http://localhost:5000')
    socketio.run(app, host='0.0.0.0', port=5000)
