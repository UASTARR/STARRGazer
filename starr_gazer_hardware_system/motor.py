"""
Title: Gimbal Motor Module
Author: Sovereign Shahid
Date: 2025-06-02
"""

import common
import time
import serial

STARTUP_MSG = "Starting board"

class SerialMotorController:
    def __init__(self, port: str, baud_rate: int):
        self.serial = serial.Serial(port, baud_rate)
        if not self.serial.isOpen():
            self.serial.open()
            time.sleep(0.5) # wait for connection to open

        self.serial.reset_output_buffer()
        self.serial.write(b"\x04")
        self.serial.flush()
        time.sleep(0.1) # wait for connection to open
        startup_msg = self.serial.read_all().decode("utf-8")

        while STARTUP_MSG not in startup_msg:
            self.serial.write(b"\x04")
            self.serial.flush()
            time.sleep(0.1) # wait for connection to open
            startup_msg = self.serial.read_all().decode("utf-8")

        self.serial.reset_input_buffer()

    def move(self, x_freq: float|int, y_freq: float|int):
        # bound frequencies
        x_freq = x_freq if x_freq < common.MAX_FREQ else common.MAX_FREQ
        x_freq = x_freq if x_freq > -common.MAX_FREQ else -common.MAX_FREQ
        y_freq = y_freq if y_freq < common.MAX_FREQ else common.MAX_FREQ
        y_freq = y_freq if y_freq > -common.MAX_FREQ else -common.MAX_FREQ

        # round values
        x_freq = int(x_freq)
        y_freq = int(y_freq)

        print(f"sending ({x_freq},{y_freq})")
        self.serial.write(f"({x_freq},{y_freq})\r\n".encode())
        self.serial.flush()

    def close(self):
        self.serial.close()

if __name__ == "__main__":
    device = "/dev/ttyACM0"
    baud_rate = 115200
    motors = SerialMotorController(device, baud_rate)
    motors.move(0,0)
    motors.move(100,100)
    time.sleep(1)
    motors.move(0,0)
    time.sleep(1)
    motors.move(-100,-100)
    time.sleep(1)
    motors.move(0,0)
    motors.close()
