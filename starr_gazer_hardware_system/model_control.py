from ultralytics import YOLO
from tracker import Tracker

class ModelTracker:
    def __init__(self, model_path: str, tracker: Tracker):
        self.model = YOLO(model_path, task="detect")
        self.tracker = tracker
        self.results = None

    def _track(self, img):
        """
        Model tracking function
        """
        results = self.model.track(img, imgsz=1024, classes=[0], persist = True, stream = True)
        result = next(results)
        self.boxes = result.boxes

        if self.boxes.id is not None:
            pos = self.boxes.xywhn[0].cpu().tolist()[:2]
            print(f"ID: {self.boxes.id[0]} Position: {pos}")
            self.tracker.track([2*pos[0] - 1, 2*pos[1] - 1])  # Centering the position
            img = result.plot()
        else:
            self.tracker.move(self.tracker.speed)
        
        return img
    
    def _get_hud_string(self, fps: float) -> str:
        """
        Hud string
        """
        return (
            f'N {self.tracker.N[0]} '
            f'Kp: {self.tracker.Kp[0]} '
            f'Ki: {self.tracker.Ki[0]} '
            f'Kd: {self.tracker.Kd[0]} '
            f'FPS: {fps:.2f}'
        )
    
    def _is_tracking(self) -> bool:
        """
        Tracking boolean
        """
        return self.boxes is not None and self.boxes.id is not None