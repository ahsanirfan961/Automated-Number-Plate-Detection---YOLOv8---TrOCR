from ultralytics import YOLO
import cv2


# load yolov8 model
model = YOLO('runs/detect/train - dataset 1 --- 40 epoch/weights/best.pt')

cap = cv2.VideoCapture('numberPlate.mp4')

ret = True
# read frames
while ret:
    ret, frame = cap.read()

    if ret:

        # detect objects
        # track objects
        results = model.track(frame, persist=True)

        # plot results
        # cv2.rectangle
        # cv2.putText
        frame_ = results[0].plot()

        print(results[0].boxes.data.tolist())

        # visualize
        cv2.imshow('frame', frame_)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break