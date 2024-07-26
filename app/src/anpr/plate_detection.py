import cv2, numpy as np
from ultralytics import YOLO
from anpr.data import modelPath

class PlateDetector:

    def __init__(self) -> None:
        self.model = YOLO(modelPath)

    def detect(self, image):
        images=[]
        coord=[]
        accuracy=[]
        track_id = []
        prediction = self.model.track(image)[0]
        for result in prediction.boxes.data.tolist():
            x1, y1, x2, y2, tr_id, score, class_id = result
            images.append(image[int(y1):int(y2),int(x1):int(x2)])    
            coord.append({
                'x1': int(x1),
                'y1': int(y1),
                'x2': int(x2),
                'y2': int(y2),
            })
            accuracy.append(score)
            track_id.append(int(tr_id))
        return images,coord, accuracy, track_id
    
    def detectAndTrack(self, image):
        images=[]
        coord=[]
        accuracy=[]
        track_id = []
        prediction = self.model.track(image, persist=True)[0]
        for result in prediction.boxes.data.tolist():
            try:
                x1, y1, x2, y2, tr_id, score, class_id = result
                images.append(image[int(y1):int(y2),int(x1):int(x2)])    
                coord.append({
                    'x1': int(x1),
                    'y1': int(y1),
                    'x2': int(x2),
                    'y2': int(y2),
                })
                accuracy.append(score)
                track_id.append(int(tr_id))
            except ValueError:
                print("Unexpected result format:", result)
        return images,coord, accuracy, track_id
