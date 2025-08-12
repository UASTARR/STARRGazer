"""
Title: Gimbal Motor Module
Author: Sovereign Shahid
Date: 2025-06-02
"""

import time
import threading
import RPi.GPIO as GPIO
import numpy as np

class GimbalMotor:

    def __init__(self, step: int, direction: int, enable: int):
        # EVERYTHING IS ACTIVE LOW
        GPIO.setup(step, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(direction, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(enable, GPIO.OUT, initial=GPIO.HIGH)

        self.step_pin = GPIO.PWM(step, 10)  # 1kHz Frequency
        self.dir_pin = direction
        self.enable_pin = enable
        self._lock = threading.Lock()
        self.running = False
        self.thread_running = False
        self._thread = threading.Thread(target=self.run())

    def start(self):
        with self._lock:
            if not self.thread_running:
                self.thread_running = True
                self._thread.start()

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

    def set_freq(self, freq: float):
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

    def start_pwm(self, duty_cycle: int = 50):
        """
        Runs the motor at a given duty cycle
        """
        self.step_pin.start(duty_cycle)
        self.running = True

    def stop_pwm(self):
        """
        Stops a currently running motor
        """
        self.step_pin.stop()
        self.running = False

    def move(self, axis: float):
        MAX_FREQ = 800
        if np.abs(axis) < 0.1:
            if self.running:
                self.stop_pwm()
                self.running = False
        else:
            self.start_pwm()
            if self.running:
                if axis < 0:
                    self.set_freq(axis*MAX_FREQ+1)
                    self.set_dir(1)
                else:
                    self.set_freq(axis*MAX_FREQ+1)
                    self.set_dir(0)

    def run(self):
        with self._lock:
            while self.thread_running:
                self.start_pwm()
                try:
                    pass
                except KeyboardInterrupt as e:
                    self.stop_pwm()
                    raise e 
            self.stop_pwm()

    def stop(self):
        with self._lock:
            if self.thread_running:
                self.thread_running = False

        


