"""
Title: Hardware System Main
Authors: Sovereign Shahid, Brian Lin
Date: 2025-06-02
"""

import time
from datetime import datetime

import pygame as pg

from motor import SerialMotorController
from tracker import Tracker
from ultralytics import YOLO
import cv2
import common
import serial

# MODEL_PATH = "weights/multiple.engine"  # Path to the YOLO model file
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

def joystick(js, motor_controller):
    x_axis = common.MAX_FREQ*js.get_axis(2)
    y_axis = common.MAX_FREQ*js.get_axis(1)
    motor_controller.move(x_axis, y_axis)

def main():
    print("Starting up IO")

    serial_device = "/dev/ttyACM" + input("Enter port number: ") 
    print(f"Setting up motor for {serial_device}")
    motor_controller = SerialMotorController(serial_device,115200)
    motor_controller.run()

    print("Initializng Joystick")
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

    print("Initializng YOLO")
    # Initialize the YOLO model
    model = YOLO(MODEL_PATH, task="detect")
    tracker = Tracker(motor_controller, [22.3, 14.9], 18) # the units for the last three numbers are in mm

    
    print("Initializng OpenCV")
    # Starts the display
    cap = cv2.VideoCapture(f'/dev/video{CAMERA_INDEX}', cv2.CAP_V4L2)
    if cap.isOpened():
        prev_time = 0

        # Video saving set up
        fourcc = cv2.VideoWriter_fourcc(*'XVID') # or X264
        frame_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        camera_fps = int(cap.get(cv2.CAP_PROP_FPS))
        print(f"Camera FPS: {camera_fps}")
        writer = cv2.VideoWriter(f'saved_footage/{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.mkv', fourcc, camera_fps, frame_size, True)

    try:
        while True:
            for event in pg.event.get():
                # Exit button
                if event.type == pg.JOYBUTTONUP and event.button == 0:
                    print("Exitting program on trigger press")
                    raise KeyboardInterrupt
                
                # Joystick motion movement printing
                if event.type == pg.JOYAXISMOTION:
                    if event.axis == 3:
                        common.MAX_FREQ = (((1-event.value)/2) * 1900) + 100
                        #print(f"MAX_FREQ = {common.MAX_FREQ}")

                    if input_mode == "joystick":
                        pass
                        # print(f"Axis {event.axis}: {event.value}")

                # Switch input mode
                if event.type == pg.JOYBUTTONUP: 
                    if event.button == 1 and cap.isOpened():
                        if input_mode == "joystick":
                            input_mode = "model"
                            print(line_sep("Switching to model control mode"))
                        else:
                            print(line_sep("Switching to joystick mode"))
                            motor_controller.move(0,0)
                            input_mode = "joystick"
                            tracker.speed = [0,0]
                            tracker.accel = [0,0]
                    elif event.button == 2:
                        tracker.N = [
                                tracker.N[0] - 5,
                                tracker.N[1] - 5
                                ]
                    elif event.button == 3:
                        tracker.N = [
                                tracker.N[0] + 5,
                                tracker.N[1] + 5
                                ]
                    elif event.button == 4:
                        tracker.Kp = [
                                tracker.Kp[0] - 1,
                                tracker.Kp[1] - 1
                                ]
                    elif event.button == 5:
                        tracker.Kp = [
                                tracker.Kp[0] + 1,
                                tracker.Kp[1] + 1
                                ]
                    elif event.button == 8:
                        tracker.Ki = [
                                tracker.Ki[0] - 1,
                                tracker.Ki[1] - 1
                                ]
                    elif event.button == 9:
                        tracker.Ki = [
                                tracker.Ki[0] + 1,
                                tracker.Ki[1] + 1
                                ]
                    elif event.button == 10:
                        tracker.Kd = [
                                tracker.Kd[0] - 1,
                                tracker.Kd[1] - 1
                                ]
                    elif event.button == 11:
                        tracker.Kd = [
                                tracker.Kd[0] + 1,
                                tracker.Kd[1] + 1
                                ]

            if cap.isOpened():
                et, img = cap.read()

                # Video saving with timestamp
                raw_frame = img.copy()
                put_text_rect(raw_frame, f'{datetime.now()}', (10,30), 0.7, bg_color=(50, 50, 50))
                writer.write(raw_frame)

                # Joystick control
                if input_mode == "joystick":
                    joystick(js, motor_controller)
                # Model control
                else:
                    results = model.track(img, imgsz=1024, classes=[0], persist=True, stream=True)
                    result = next(results)
                    boxes = result.boxes
                    if boxes.id is not None:
                        pos = boxes.xywhn[0].cpu().tolist()[:2]
                        print(f"ID: {boxes.id[0]} Position: {pos}")
                        tracker.track([2*pos[0] - 1, 2*pos[1] - 1])  # Centering the position
                        img = result.plot()
                    else:
                        tracker.move(tracker.speed)

                # Calculate FPS
                curr_time = time.time()
                fps = 1 / (curr_time - prev_time) if prev_time else 0
                prev_time = curr_time
                if input_mode == "joystick":
                    put_text_rect(img, f'Joystick ({js.get_axis(2):.2f},{js.get_axis(1):.2f}) Serial Msg: {motor_controller.get_msg()} FPS: {fps:.2f}', (10, 30), 0.7, bg_color=(50, 50, 50))
                else:
                    put_text_rect(img, f'N {tracker.N[0]} Kp: {tracker.Kp[0]} Ki: {tracker.Ki[0]}, Kd: {tracker.Kd[0]} FPS: {fps:.2f}', (10, 30), 0.7, bg_color=(50, 50, 50))
                put_text_rect(img, f'Speed: ({tracker.speed[0]:.2f}, {tracker.speed[1]:.2f}) Accel: ({tracker.accel[0]:.2f}, {tracker.accel[1]:.2f}) Max Freq: {common.MAX_FREQ:.2f}', (10, 60), 0.7, bg_color=(50, 50, 50))

                cv2.imshow("DSLR Live", img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("Exiting program on 'q' key press")
                    raise KeyboardInterrupt

            else: # if we dont have a camera ignore input mode
                joystick(js, motor_controller)



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

        motor_controller.close(close_serial=False)

    
    print("Sending stop msg to motor")
    motor_controller.send_msg(b'0 0\r\n')
    motor_controller.serial.close()
    print("Finishing IO")


if __name__ == "__main__":
    main()
