"""
Title: Gimbal Motor Module
Author: Sovereign Shahid
Date: 2025-06-02
"""

import common
import time
import threading

from serial import Serial

STARTUP_MSG = "Starting board"

class SerialMotorController:

    # -- CONSTANTS -- #
    MSG_INTERVAL = 0.05  # 50 ms

    def __init__(self, port: str, baud_rate: int):
        self.serial: Serial = Serial(port, baud_rate)

        # Thread logic
        self._lock = threading.Lock()
        self.running = threading.Event()
        self.running.set()

        self._serial_message = b'0 0\r\n' 
        self._thread = threading.Thread(target=self._thread_loop, daemon=True)
        self._init_serial()

    def _init_serial(self):
        print("Initializing Serial")
        if not self.serial.isOpen():
            self.serial.open()
            time.sleep(0.5) # wait for connection to open

        self.serial.reset_output_buffer()
        self.serial.reset_input_buffer()

        time.sleep(0.1) # wait for connection to open
        startup_msg = self.serial.read_all().decode("utf-8")

        while STARTUP_MSG not in startup_msg:
            print("Soft rebooting board")
            self.serial.write(b"\x04")
            self.serial.flush()
            time.sleep(0.1) # wait for connection to open
            startup_msg = self.serial.read_all().decode("utf-8")


    def move(self, x_freq: float, y_freq: float):
        # bound frequencies
        x_freq = x_freq if x_freq < common.MAX_FREQ else common.MAX_FREQ
        x_freq = x_freq if x_freq > -common.MAX_FREQ else -common.MAX_FREQ
        y_freq = y_freq if y_freq < common.MAX_FREQ else common.MAX_FREQ
        y_freq = y_freq if y_freq > -common.MAX_FREQ else -common.MAX_FREQ

        self._serial_message = f"{x_freq:.0f} {y_freq:.0f}\r\n".encode()

    def _thread_loop(self):
        next_time = time.perf_counter()
        while self.running.is_set() and self.serial.isOpen():
            with self._lock:
                print(self._serial_message)
                self.send_msg(self._serial_message)
            if self.serial.inWaiting() > 0:
                data_str = self.serial.read(self.serial.inWaiting()).decode('ascii') 
                print(data_str, end='') 
            next_time += self.MSG_INTERVAL
            sleep_time = max(0, next_time - time.perf_counter())
            time.sleep(sleep_time)
        self.serial.close()
            
    def send_msg(self, msg: bytes):
        self.serial.write(msg)
        self.serial.flush()

    def get_msg(self):
        return self._serial_message[:-2].decode('utf-8')

    def run(self):
        self._thread.start()

    def close(self):
        self.running.clear()
        if self._thread.is_alive():
            self._thread.join()

if __name__ == "__main__":
    multithreaded = True
    device = "/dev/ttyACM0"
    baud_rate = 115200
    motors = SerialMotorController(device, baud_rate)
    commands = [
        (100,100), 
        (0,0), 
        (-100,-100), 
        (0,0), 
    ]

    if multithreaded:
        motors.run()

    for command in commands:
        print(f"sending {command}")
        if multithreaded:
            motors.move(*command)
        else:
            motors.send_msg(f"{command[0]} {command[1]}\r\n".encode())
        time.sleep(1)

    if multithreaded:
        motors.close()
    else:
        motors.serial.close()

