import cv2 as cv
import os
from singleFrameComplete import process_frame
import pickle
video_path = 'tests/numberPlate.mp4'    
cap = cv.VideoCapture(video_path)
processed_frame=[]
length = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
processed=0
while True:     
    ret, frame = cap.read()
    if not ret:
        break
    processed+=1    
    processed_frame.append(process_frame(frame))
    print(f"Processed {processed}/{length} frames processed")
    
with open('list.pkl', 'wb') as file:
    pickle.dump(processed_frame, file)    
    
video = cv.VideoWriter('output.avi', 0, 1, (processed_frame[0].shape[1],processed_frame[0].shape[0]))   
for img in processed_frame:
    video.write(img)
    
cv.destroyAllWindows()
video.release()   
cap.release() 