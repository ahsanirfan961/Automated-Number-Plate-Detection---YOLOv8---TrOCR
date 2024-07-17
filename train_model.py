from ultralytics import YOLO

model = YOLO('yolov8n.yaml')

result = model.train(data='data.yaml', epochs=100)