"""
Title: Gimbal Motor Module
Author: Sovereign Shahid
Date: 2025-06-02
"""

import time

import RPi.GPIO as GPIO


class GimbalMotor:

    def __init__(self, step: int, direction: int, enable: int):
        # EVERYTHING IS ACTIVE LOW
        GPIO.setup(step, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(direction, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(enable, GPIO.OUT, initial=GPIO.HIGH)

        self.step_pin = GPIO.PWM(step, 250)  # 1kHz Frequency
        self.dir_pin = direction
        self.enable_pin = enable

    def set_dir(self, direction: int):
        """
        Sets the direction pin of the motor (ccw low and cw high) 
        """
        GPIO.output(self.dir_pin, direction)

    def set_enable(self, enable: int):
        """
        Sets the enable pin of the motor
        """
        GPIO.output(self.dir_pin, enable)

    def set_duty_cycle(self, duty_cycle: int):
        """
        Sets the duty cycle of the step signal
        """
        self.step_pin.ChangeDutyCycle(duty_cycle)

    def set_freq(self, freq: int):
        """
        Sets the duty cycle of the step signal
        """
        self.step_pin.ChangeFrequency(freq)

    def step_motor(self):
        """
        Steps the motor once
        """
        self.step_pin.start(100)
        time.sleep(1e-6)  # sleep for 1 microsecond
        self.step_pin.stop()

    def run(self, duty_cycle: int = 50):
        """
        Runs the motor at a given duty cycle
        """
        self.step_pin.start(duty_cycle)

    def stop(self):
        """
        Stops a currently running motor
        """
        self.step_pin.stop()
