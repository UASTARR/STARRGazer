import time
import numpy as np
import common


class Tracker:

    def __init__(self, motor_x, motor_y, sensor_length, focal_length):
        self.previous_time = time.perf_counter()
        self.previous_error = [0, 0]
        self.motor_x = motor_x
        self.motor_y = motor_y
        self.speed = [0, 0]
        self.los_angles = [np.arctan2(2*focal_length, sensor_length[0]),np.arctan2(2*focal_length, sensor_length[1])]

    def _propnav(self, error):
        delta_error = [
            error[0] - self.previous_error[0],
            error[1] - self.previous_error[1],
        ]

        return [
            -1*delta_error[0]*2*self.los_angles[0]*error[0]*common.GAIN[0],
            -1*delta_error[0]*2*self.los_angles[0]*error[1]*common.GAIN[1]
        ]

    def move(self, accel = [0, 0]):

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

        self.move(self._propnav(error))

