import cv2

cap = cv2.VideoCapture('tests/numberPlate.mp4')

fps = cap.get(cv2.CAP_PROP_FPS)
print(fps)

skipFrames = int(5*fps)

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret:
        cv2.imshow('Vid', frame)

        key = cv2.waitKey(17) & 0xFF 

        if key == ord('q'):
            break
        elif key == ord('l'):
            currentFrame = cap.get(cv2.CAP_PROP_POS_FRAMES)
            cap.set(cv2.CAP_PROP_POS_FRAMES, currentFrame+skipFrames)
        elif key == ord('j'):
            currentFrame = cap.get(cv2.CAP_PROP_POS_FRAMES)
            cap.set(cv2.CAP_PROP_POS_FRAMES, currentFrame-skipFrames)
    else:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

cap.release()
cv2.destroyAllWindows()