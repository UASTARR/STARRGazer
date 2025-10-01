"""
Title: Gimbal Motor Module
Author: Sovereign Shahid
Date: 2025-06-02
"""

import time
import numpy as np
import common
import serial

class SerialMotorController:
    def __init__(self, port: str, baud_rate: int):
        self.serial = serial.Serial(port, baud_rate, timeout = 1)


    def move(self, x_freq: float, y_freq: float):
        self.serial.write(f"({int(x_freq)},{int(y_freq)})\n")

