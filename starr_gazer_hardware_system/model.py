import cv2
from ultralytics import YOLO
import time


class YoloModel:

    def __init__(self, model_path="yolo11s.pt", camera_index=0):
        self.model = YOLO(model_path)
        self.cap = cv2.VideoCapture(f'/dev/video{camera_index}', cv2.CAP_V4L2)
        self.prev_time = 0

    def put_text_rect(img, text, pos, scale=0.5, thickness=1, bg_color=(0,0,0), text_color=(255,255,255)):
        font = cv2.FONT_HERSHEY_SIMPLEX
        text_size, _ = cv2.getTextSize(text, font, scale, thickness)
        text_w, text_h = text_size
        x, y = pos
        cv2.rectangle(img, (x, y - text_h - 6), (x + text_w + 4, y + 4), bg_color, -1)
        cv2.putText(img, text, (x + 2, y - 2), font, scale, text_color, thickness)


    def predict(self):
        et, img = self.cap.read()
        # results = model(img, imgsz=1024)  # Strip 4th channel if needed
        results = self.model.track(img, imgsz=1024, classes=[0], persist=True, stream=True)
        img = next(results).plot()

        curr_time = time.time()
        fps = 1 / (curr_time - self.prev_time) if self.prev_time else 0

        self.prev_time = curr_time
        self.put_text_rect(img, f'FPS: {fps:.2f}', (10, 30), scale=0.7, bg_color=(50, 50, 50))

        cv2.imshow("DSLR Live", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return None
        
        return next(results)
    
    def __del__(self):
        del self.model
        
        cv2.destroyAllWindows()
    