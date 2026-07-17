"""
Title: Hardware System Main
Authors: Sovereign Shahid, Brian Lin
Date: 2025-06-02
"""

import time
from datetime import datetime

from joystick_control import Joystick
from motor import SerialMotorController
from tracker import Tracker

from model_control import ModelTracker

import cv2

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


def line_sep(text: str, length: int = 50, character: str = "=") -> str:
    """
    Returns a string with the text centered and padded with dashes.
    """
    if len(text) >= length:
        return text
    padding = (length - len(text)) // 2
    return (
        character * padding
        + text
        + character * padding
        + (character if (length - len(text)) % 2 else "")
    )


def main():
    print("Starting up IO")

    serial_device = "/dev/ttyACM" + input("Enter port number: ")
    print(f"Setting up motor for {serial_device}")
    motor_controller = SerialMotorController(serial_device, 115200)
    motor_controller.run()

    print("Initializng YOLO")
    # Initialize the YOLO model
    tracker = Tracker(motor_controller, [22.3, 14.9], 18) # the units for the last three numbers are in mm

    model_tracker = ModelTracker(MODEL_PATH, tracker)

    
    print("Initializng OpenCV")
    # Starts the display
    cap = cv2.VideoCapture(f'/dev/video{CAMERA_INDEX}', cv2.CAP_V4L2)

    print("Initializng Joystick")
    joystick = Joystick(motor_controller, tracker, has_camera=cap.isOpened())

    if cap.isOpened():
        # Video saving set up
        fourcc = cv2.VideoWriter_fourcc(*"XVID")  # or X264
        frame_size = (
            int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        )
        camera_fps = int(cap.get(cv2.CAP_PROP_FPS))
        print(f"Camera FPS: {camera_fps}")
        writer = cv2.VideoWriter(
            f"saved_footage/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.mkv",
            fourcc,
            camera_fps,
            frame_size,
            True,
        )

    try:
        prev_time = 0
        while True:
            joystick.process_events()

            curr_time = time.time()
            fps = 1 / (curr_time - prev_time) if prev_time else 0
            prev_time = curr_time

            if joystick.should_exit:
                raise KeyboardInterrupt
            

            if cap.isOpened():
                et, img = cap.read()

                if joystick.input_mode == "joystick":
                    joystick.drive()
                else:
                    img = model_tracker._track(img)

                # Video saving with timestamp
                raw_frame = img.copy()
                writer.write(raw_frame)

                if joystick.input_mode == "joystick":
                    put_text_rect(img, joystick.get_hud_string(fps), (10, 30), 0.7, bg_color=(50, 50, 50))
                else:
                    put_text_rect(img, model_tracker._get_hud_string(fps), (10, 30), 0.7, bg_color=(50, 50, 50))

                cv2.imshow("DSLR Live", img)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    print("Exiting program on 'q' key press")
                    raise KeyboardInterrupt

            else: # if we dont have a camera ignore input mode
                joystick.drive()

    except KeyboardInterrupt:
        pass
    finally:
        print("Exiting program")
        joystick.shutdown()

        print("Releasing camera")
        cv2.destroyAllWindows()
        cap.release()

        print("Motor stopping")

        motor_controller.close(close_serial=False)

    print("Sending stop msg to motor")
    motor_controller.send_msg(b"0 0\r\n")
    motor_controller.serial.close()
    print("Finishing IO")

if __name__ == "__main__":
    main()
