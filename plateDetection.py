from ultralytics import YOLO
import cv2 as cv

def plateDetection(img):
    images=[]
    model_path = 'runs/detect/train - dataset 1 --- 40 epoch/weights/best.pt'
    model = YOLO(model_path)
    prediction = model(img)[0]
    coord=[]
    for result in prediction.boxes.data.tolist():
        
        x1, y1, x2, y2, score, class_id = result
        cv.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 1)
        images.append(img[int(y1):int(y2),int(x1):int(x2)])    
        coord.append((x1,x2,y1,y2))
    return img,images,coord  