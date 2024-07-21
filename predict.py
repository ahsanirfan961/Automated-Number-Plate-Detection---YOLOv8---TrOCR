import cv2, os
from ultralytics import YOLO

test_dir_path = 'datasets/dataset 1/images/test'
model_path = 'runs/detect/train - dataset 1 --- 40 epoch/weights/best.pt'

model = YOLO(model_path)

images = []
for i, file in enumerate(os.listdir(test_dir_path)):
    img_path = test_dir_path + '/' + file
    images.append(cv2.imread(img_path))
    if i == 10:
        break
 
for i, img in enumerate(images):
    prediction = model(img)[0]
    for result in prediction.boxes.data.tolist():
        print(result)
        x1, y1, x2, y2, score, class_id = result
        cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
        cv2.putText(img, prediction.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
    cv2.imshow(f"Image {i}", img)

key = cv2.waitKey(0)
if key == 27:
    cv2.destroyAllWindows()