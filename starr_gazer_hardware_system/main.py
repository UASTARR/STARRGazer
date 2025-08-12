"""
Title: Hardware System Main
Author: Sovereign Shahid
Date: 2025-06-02
"""

import time

import RPi.GPIO as GPIO

from motor import GimbalMotor

# no lock needed since an operation on this is guaranteed to set it false
RUNNING = True


# TODO: Add multithreading
def io_thread():
    # I/O Setup
    print(f"Setting up motor for {GPIO.model}")
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    motor = GimbalMotor(32, 33, 38)  # example pins change later
    motor.set_dir(GPIO.LOW)
    motor.set_enable(GPIO.LOW)
    motor.set_freq(250)
    try:
        print("Moving motor ccw for half a second")
        motor.run()
        time.sleep(0.5)
        print("Pausing motor for half a second")
        motor.stop()
        time.sleep(0.5)
        print("Reversing motor for half a second")
        motor.set_dir(GPIO.HIGH)
        motor.run()
        time.sleep(0.5)
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
