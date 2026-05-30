"""
Joystick Control
Author: Sovereign Shahid, Brian Lin, refactored by Arron Roasa
Date: 2026/03/25
"""
import pygame as pg
import common
from motor import SerialMotorController
from tracker import Tracker

class Joystick:
    def __init__(self, motor_controller: SerialMotorController, tracker: Tracker, has_camera: bool = False):
        pg.init()
        pg.joystick.init()

        if pg.joystick.get_count() == 0:
            raise RuntimeError("ERROR: No joystick connected. " \
            "Please connect the Logitech Extreme 3D Pro and retry.")
        
        self.joystick = pg.joystick.Joystick(0)
        self.joystick.init()

        self.input_mode: str = "joystick"
        self.should_exit: bool = False
        self.has_camera: bool = has_camera

        self.motor_controller: SerialMotorController = motor_controller
        self.tracker: Tracker = tracker

    
    def _process_events(self):
        """
        Process pygame events
        """
        for event in pg.event.get():
            self._handle_event(event)

    def _handle_event(self, event):
        """
        Handle button or joystick events
        """
        if event.type == pg.JOYBUTTONUP:
            self._handle_button(event.button)
        if event.type == pg.JOYAXISMOTION:
            self._handle_axis(event.axis, event.value)

    def _handle_button(self, button):
        """
        Button input
        """
        if button == 0:
            self.should_exit = True
        if button == 1 and self.has_camera:
            if self.input_mode == "joystick":
                self.input_mode = "model"
            else:
                self.input_mode = "joystick"
                self.motor_controller.move(0, 0)
                self.tracker.speed = [0,0]
                self.tracker.accel = [0,0]
        if button == 2: self.tracker.N -= 5
        if button == 3: self.tracker.N += 5
        if button == 4: self.tracker.Kp -= 1
        if button == 5: self.tracker.Kp += 1
        if button == 8: self.tracker.Ki -= 1
        if button == 9: self.tracker.Ki += 1
        if button == 10: self.tracker.Kd -= 1
        if button == 11: self.tracker.Kd += 1
    
    def _handle_axis(self, axis, value):
        """
        Joystick input
        """
        if axis == 3:
            common.MAX_FREQ = ((1 - value) / 2 * 1900) + 100
    
    def drive(self):
        """
        Driver function
        """
        if self.joystick is None: # Keyboard input for testing
            keys = pg.key.get_pressed()
            x_axis = common.MAX_FREQ if keys[pg.K_RIGHT] else -common.MAX_FREQ if keys[pg.K_LEFT] else 0
            y_axis = common.MAX_FREQ if keys[pg.K_DOWN] else -common.MAX_FREQ if keys[pg.K_UP] else 0
        else: # Joystick connected
            x_axis = common.MAX_FREQ * self.joystick.get_axis(2)
            y_axis = common.MAX_FREQ * self.joystick.get_axis(1)

        self.motor_controller.move(x_axis, y_axis)

    def get_hud_string(self, fps: float) -> str:
        """
        Hud string
        """
        return (
            f'Joystick ({self.joystick.get_axis(2):.2f}, {self.joystick.get_axis(1):.2f}) '
            f'Serial Msg: {self.motor_controller.get_msg()} '
            f'FPS: {fps:.2f}'
        )
    
    def _shutdown(self):
        """
        Shutdown function
        """
        pg.event.clear()
        pg.quit()