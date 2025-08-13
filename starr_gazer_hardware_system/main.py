"""
Title: Hardware System Main
Authors: Sovereign Shahid, Brian Lin
Date: 2025-06-02
"""

import time
from datetime import datetime

import pygame as pg
import RPi.GPIO as GPIO

from motor import GimbalMotor
from tracker import Tracker
from ultralytics import YOLO
import cv2

JOYSTICK = True
MODEL_PATH = "yolo11s.pt"  # Path to the YOLO model file
CAMERA_INDEX = 0  # Index of the camera to use, usually 0 for the first camera

def put_text_rect(img, text, pos, scale=0.5, thickness=1, bg_color=(0,0,0), text_color=(255,255,255)):
    font = cv2.FONT_HERSHEY_SIMPLEX
    text_size, _ = cv2.getTextSize(text, font, scale, thickness)
    text_w, text_h = text_size
    x, y = pos
    cv2.rectangle(img, (x, y - text_h - 6), (x + text_w + 4, y + 4), bg_color, -1)
    cv2.putText(img, text, (x + 2, y - 2), font, scale, text_color, thickness)

def line_sep(text: str, length: int = 50, character: str = '=') -> str:
    """
    Returns a string with the text centered and padded with dashes.
    """
    if len(text) >= length:
        return text
    padding = (length - len(text)) // 2
    return character * padding + text + character * padding + (character if (length - len(text)) % 2 else '')

def joystick(js, motor_x, motor_y):
    x_axis = js.get_axis(2)
    y_axis = js.get_axis(1)
    motor_x.move(x_axis)
    motor_y.move(y_axis)

def main():
    print("Starting up IO")
    print(f"Setting up motor for {GPIO.model}")
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    motor_x = GimbalMotor(33, 13, 37)
    motor_x.set_enable(GPIO.LOW)
    motor_y = GimbalMotor(15, 11, 38)
    motor_y.set_enable(GPIO.LOW)

    pg.init()
    pg.joystick.init()

    if pg.joystick.get_count() == 0:
        raise RuntimeError(
            "No Joystick Detected. Connect the Logitech Extreme 3D Pro and retry"
        )

    js = pg.joystick.Joystick(0)
    js.init()

    input_mode = "joystick"
    print(f"Input mode: {input_mode}")

    # Initialize the YOLO model
    model = YOLO(MODEL_PATH, task="detect")
    tracker = Tracker(motor_x, motor_y)
    # Starts the display
    cap = cv2.VideoCapture(f'/dev/video{CAMERA_INDEX}', cv2.CAP_V4L2)
    prev_time = 0

    fourcc = cv2.VideoWriter_fourcc(*'X264')
    writer = cv2.VideoWriter(f'saved_footage/{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.mkv', fourcc, 30.0, (cap.get(3), cap.get(4)))

    try:
        while True:
            for event in pg.event.get():
                # Exit button
                if event.type == pg.JOYBUTTONUP and event.button == 1:
                    print("Exitting program on trigger press")
                    raise KeyboardInterrupt
                
                # Joystick motion movement printing
                if event.type == pg.JOYAXISMOTION and input_mode == "joystick":
                    print(f"Axis {event.axis}: {event.value}")
                    print(f"Running {motor_x.running}")

                # Switch input mode
                if event.type == pg.JOYBUTTONUP and event.button == 7:
                    if input_mode == "joystick":
                        input_mode = "model"
                        print(line_sep("Switching to model control mode"))
                    else:
                        input_mode = "joystick"
                        print(line_sep("Switching to joystick mode"))

            et, img = cap.read()

            writer.write(img)

            # Joystick control
            if input_mode == "joystick":
                joystick(js, motor_x, motor_y)
            # Model control
            else:
                results = model.track(img, imgsz=1024, classes=[0], persist=True, stream=True)
                result = next(results)
                boxes = result.boxes
                if boxes.id is not None:
                    pos = boxes.xywhn[0].cpu().tolist()[:2]
                    print(f"ID: {boxes.id[0]} Position: {pos}")
                    tracker.track([pos[0] - 0.5, pos[1] - 0.5])  # Centering the position
                    img = result.plot()

            # Calculate FPS
            curr_time = time.time()
            fps = 1 / (curr_time - prev_time) if prev_time else 0
            prev_time = curr_time
            put_text_rect(img, f'FPS: {fps:.2f}', (10, 30), 0.7, bg_color=(50, 50, 50))

            cv2.imshow("DSLR Live", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Exiting program on 'q' key press")
                raise KeyboardInterrupt


    except KeyboardInterrupt:
        pass
    finally:
        print("cleaning up joystick")
        for _ in pg.event.get():
            pass

        print("Exiting program")
        pg.quit()

        print("Releasing camera")
        cv2.destroyAllWindows()
        cap.release()

        print("Motor stopping")
        motor_x.stop_pwm()
        motor_y.stop_pwm()
        try:
            GPIO.cleanup()
        except OSError:  # For some reason cleanup gives us an os error
            pass
    print("Finishing IO")


if __name__ == "__main__":
    main()