import time

CENTER = [0, 0]


class Tracker:

    def __init__(self, motor_x, motor_y):
        self.previous_time = time.perf_counter()
        self.previous_error = [0, 0]
        self.total_error = [0, 0]
        self.motor_x = motor_x
        self.motor_y = motor_y
        self.Kp = [5e-2, 5e-1]
        self.Kd = [1e-1, 1e-1]
        self.Ki = [1e-1, 1e-1]

    def track(self, rocketPos):
        """
        Moves the motors based on the rocket position returned by the model
        """
        current_time = time.perf_counter()
        dt = current_time - self.previous_time
        self.previous_time = current_time
        error = [CENTER[0] - rocketPos[0], CENTER[1] - rocketPos[1]]
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
            self.Kp[0] * error[0]
            + self.Ki[0] * self.total_error[0]
            + self.Kd[0] * derivative[0],
            self.Kp[1] * error[1]
            + self.Ki[1] * self.total_error[1]
            + self.Kd[1] * derivative[1],
        ]

        # TBD control the motor (duty cycle must be within 1-99 inclusive)
