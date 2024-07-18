from ultralytics import YOLO

model = YOLO('yolov8n.yaml')

result = model.train(data='./datasets/dataset - AB-Rehman/data.yaml', epochs=1)