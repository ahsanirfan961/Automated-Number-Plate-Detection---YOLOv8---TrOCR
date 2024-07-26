from ultralytics import YOLO

model = YOLO('runs/detect/dataset 1 --- 40 epoch/weights/best.pt')

if __name__ == '__main__':  
    model.val()