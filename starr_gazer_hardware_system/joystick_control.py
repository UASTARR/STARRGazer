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
        
        self.joystick = Joystick(0)
        self.joystick.init()

        self.input_mode: str = "joystick"
        self.should_exit: bool = False
        self.has_camera: bool = has_camera

        self.motor_controller: SerialMotorController = motor_controller
        self.tracker: Tracker = tracker

    def processEvents():
        for event in pg.event.get():
            _handle_event(event)

    def _handle_event(event):
        if event.type == pg.JOYBUTTONUP:
            _handle_button(event.button)
        if event.type == pg.JOYAXISMOTION:
            _handle_axis(event.axis, event.value)

    def _handle_button(button):
        if button == 0:
            should_exit = True;
        if button == 1 and cap.isOpen():
            if input_mode == "joystick":
                input_mode = "model"
            else:
                input_mode = "joystick"
                motor_controller.move(0, 0)
                tracker.speed = [0,0]
                tracker.accel = [0,0]
