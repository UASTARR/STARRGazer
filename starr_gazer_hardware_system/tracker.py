import time
import numpy as np
import common


class Tracker:

    def __init__(self, motor_controller, sensor_length, focal_length):
        self.previous_time = time.perf_counter()
        self.previous_pid = [0, 0]
        self.previous_error = [0, 0]
        self.total_pid = [0, 0]
        self.Kp = [1, 1]
        self.Kd = [10, 10]
        self.Ki = [0, 0]
        self.N = [10, 10]
        self.motor_controller = motor_controller
        self.accel = [0, 0]
        self.speed = [0, 0]
        self.los_angles = [np.arctan2(2*focal_length, sensor_length[0]),np.arctan2(2*focal_length, sensor_length[1])]

    # WE ARE NOT USING PROPNAV
    # def _propnav(self, error):
    #     print(f"Position: {error})")
    #     delta_error = [
    #         np.abs(error[0] - self.previous_error[0]),
    #         np.abs(error[1] - self.previous_error[1])
    #     ]
    #
    #     return [
    #         delta_error[0]*2*self.los_angles[0]*error[0]*self.N[0],
    #         delta_error[0]*2*self.los_angles[0]*error[1]*self.N[1]
    #     ]

    def _pid(self, pid_in):
        current_time = time.perf_counter()
        dt = current_time - self.previous_time
        self.previous_time = current_time
        derivative = [
            (pid_in[0] - self.previous_pid[0]) / dt,
            (pid_in[1] - self.previous_pid[1]) / dt,
        ]
        self.total_pid = [
            (pid_in[0] + self.previous_pid[0]) * dt,
            (pid_in[1] + self.previous_pid[1]) * dt,
        ]
        self.previous_pid = pid_in

        return [
            self.Kp[0] * pid_in[0]
            + self.Ki[0] * self.total_pid[0]
            + self.Kd[0] * derivative[0],
            self.Kp[1] * pid_in[1]
            + self.Ki[1] * self.total_pid[1]
            + self.Kd[1] * derivative[1],
        ]

    def move(self, accel = [0, 0]):
        self.accel = accel
        self.speed = [
                self.speed[0] + accel[0],
                self.speed[1] + accel[1]
                ]

        print(f"accel: {accel}")
        print(f"speed: {self.speed}")


        if self.speed[0] > common.MAX_FREQ:
            self.speed[0] = common.MAX_FREQ
        elif self.speed[0] < -common.MAX_FREQ:
            self.speed[0] = -common.MAX_FREQ

        self.motor_controller.move(*self.speed) # pass speed to motor controller as two arguments

    def track(self, error):
        """
        Moves the motors based on the rocket position returned by the model
        """

        self.move(self._pid(error))

