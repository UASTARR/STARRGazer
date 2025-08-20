import time
import numpy as np
import common


class Tracker:

    def __init__(self, motor_x, motor_y):
        self.previous_time = time.perf_counter()
        self.previous_error = [0, 0]
        self.total_error = [0, 0]
        self.motor_x = motor_x
        self.motor_y = motor_y
        self.Kp = [200, 200]
        self.Ki = [50, 50]
        self.Kd = [100, 100]
        self.speed = [0, 0]

    def _pid(self, error):
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

        return [
            self.Kp[0] * error[0]
            + self.Ki[0] * self.total_error[0]
            + self.Kd[0] * derivative[0],
            self.Kp[1] * error[1]
            + self.Ki[1] * self.total_error[1]
            + self.Kd[1] * derivative[1],
        ]

    def move(self, pid_output):

        self.speed = pid_output
        print(f"speed: {self.speed}")

        if self.speed[0] > common.MAX_FREQ:
            self.speed[0] = common.MAX_FREQ
        elif self.speed[0] < -common.MAX_FREQ:
            self.speed[0] = -common.MAX_FREQ

        try:
            # if -2 < self.speed[0] < 2:
            #     self.motor_x.stop_pwm()
            if self.speed[0] > 2:
                self.motor_x.start_pwm()
                self.motor_x.set_freq(self.speed[0])
                self.motor_x.set_dir(1)
            elif self.speed[0] < -2:
                self.motor_x.start_pwm()
                self.motor_x.set_freq(-self.speed[0])
                self.motor_x.set_dir(0)
            else:
                self.motor_x.stop_pwm()


            if self.speed[1] > common.MAX_FREQ:
                self.speed[1] = common.MAX_FREQ
            elif self.speed[1] < -common.MAX_FREQ:
                self.speed[1] = -common.MAX_FREQ

            # if -2 < self.speed[1] < 2:
            #     self.motor_x.stop_pwm()
            if self.speed[1] > 2:
                self.motor_y.start_pwm()
                self.motor_y.set_freq(self.speed[1])
                self.motor_y.set_dir(0)
            elif self.speed[1] < -2:
                self.motor_y.start_pwm()
                self.motor_y.set_freq(-self.speed[1])
                self.motor_y.set_dir(1)
            else:
                self.motor_y.stop_pwm()
        except Exception as e:
            print(f"Error: motor speed")
            raise e


    def track(self, error):
        """
        Moves the motors based on the rocket position returned by the model
        """

        self.move(self._pid(error))

