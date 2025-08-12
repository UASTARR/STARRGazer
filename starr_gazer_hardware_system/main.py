"""
Title: Hardware System Main
Author: Sovereign Shahid
Date: 2025-06-02
"""

import time

import RPi.GPIO as GPIO
import pygame as pg

from motor import GimbalMotor

# no lock needed since an operation on this is guaranteed to set it false
RUNNING = True

def get_movement(axis: float) -> (float, int):
    MAX_FREQ = 800
    if np.abs(axis) < 0.01:
        return (0, 0)
    else:
        if axis < 0:
            return (axis*MAX_FREQ, 1)
        else:
            return (axis*MAX_FREQ, 0)
# TODO: Add multithreading
def io_thread():
    # I/O Setup
    print(f"Setting up motor for {GPIO.model}")
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    pg.init()
    pg.joystick.init()

    if pg.joystick.get_count() == 0:
        raise RuntimeError("No Joystick Detected. Connect the Logitech Extreme 3D Pro and retry")

    js = pg.joystick.Joystick(0)
    js.init()

    motor = GimbalMotor(32, 33, 38)  # example pins change later
    motor.set_enable(GPIO.LOW)

    # motor.start()
    try:
        while True:
            for event in pg.event.get():
                if event.type == pg.JOYAXISMOTION:
                    print(f"Axis {event.axis}: {event.value}")
                if event.type == pg.JOYBUTTONUP and event.button == 0:
                    print("Exitting program on trigger press")
                    raise KeyboardInterrupt
            x_axis = js.get_axis(2)
            freq, direction = get_movement(x_axis)
            motor.set_freq(freq)
            motor.set_dir(direction)

    except KeyboardInterrupt:
        pass
    finally:
        print("Motor stopping")
        motor.stop()
        try:
            GPIO.cleanup()
        except OSError:  # For some reason cleanup gives us an os error
            pass


def main():
    print("Starting up io thread")
    io_thread()
    print("Exiting io thread")


if __name__ == "__main__":
    main()
