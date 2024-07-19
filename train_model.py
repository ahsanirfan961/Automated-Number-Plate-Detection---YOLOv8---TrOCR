from ultralytics import YOLO

model = YOLO('yolov8n.pt')

if __name__ == "__main__":
    result = model.train(data='datasets\dataset 1\data.yaml', epochs=40)