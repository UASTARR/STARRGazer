import time
import numpy as np

MAX_FREQ = 500


class Tracker:

    def __init__(self, motor_x, motor_y):
        self.previous_time = time.perf_counter()
        self.previous_error = [0, 0]
        self.total_error = [0, 0]
        self.motor_x = motor_x
        self.motor_y = motor_y
        self.Kp = [500, 500]
        self.Kd = [10, 10]
        self.Ki = [10, 10]

    def track(self, error):
        """
        Moves the motors based on the rocket position returned by the model
        """
        current_time = time.perf_counter()
        dt = current_time - self.previous_time
        self.previous_time = current_time
        derivative = [
            (error[0] - self.previous_error[0]) / dt,
            (error[1] - self.previous_error[1]) / dt,
        ]
        self.total_error = [
            (error[0] - self.previous_error[0]) * dt,
            (error[1] - self.previous_error[1]) * dt,
        ]
        self.previous_error = error

        motor_speed = [
            round(self.Kp[0] * error[0]
            + self.Ki[0] * self.total_error[0]
            + self.Kd[0] * derivative[0]),
            round(self.Kp[1] * error[1]
            + self.Ki[1] * self.total_error[1]
            + self.Kd[1] * derivative[1]) ,
        ]

        print(f"Motor Speed: {motor_speed}")

        if motor_speed[0] > MAX_FREQ:
            motor_speed[0] = MAX_FREQ
        elif motor_speed[0] < -MAX_FREQ:
            motor_speed[0] = -MAX_FREQ

        #if motor_speed[0] == 0:
         #   motor_speed[0] = 2

        #if motor_speed[1] == 0:
         #   motor_speed[1] = 2

        try:
            if motor_speed[0] > 1:
                self.motor_x.start_pwm()
                self.motor_x.set_freq(motor_speed[0])
                self.motor_x.set_dir(1)
            elif motor_speed[0] < -1:
                self.motor_x.start_pwm()
                self.motor_x.set_freq(-motor_speed[0])
                self.motor_x.set_dir(0)
            else:
                self.motor_x.stop_pwm()


            if motor_speed[1] > MAX_FREQ:
                motor_speed[1] = MAX_FREQ
            elif motor_speed[1] < -MAX_FREQ:
                motor_speed[1] = -MAX_FREQ

            if motor_speed[1] > 1:
                self.motor_y.start_pwm()
                self.motor_y.set_freq(motor_speed[1])
                self.motor_y.set_dir(0)
            elif motor_speed[1] < -1:
                self.motor_y.start_pwm()
                self.motor_y.set_freq(-motor_speed[1])
                self.motor_y.set_dir(1)
            else:
                self.motor_y.stop_pwm()
        except Exception as e:
            print(f"Error: motor speed")
            raise e