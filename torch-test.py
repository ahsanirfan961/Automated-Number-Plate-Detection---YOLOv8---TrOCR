import cv2 as cv
import os
from singleFrameComplete import process_frame
import pickle
video_path = 'tests/vid1.mp4'    
cap = cv.VideoCapture(video_path)
fourcc = cv.VideoWriter_fourcc(*'mp4v') 
fps = cap.get(cv.CAP_PROP_FPS)
processed_frame=[]
length = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
processed=19
fr=None
cord=None
txt=None
while True:     
    ret, frame = cap.read()
    if not ret:
        break
    processed+=1 
    if(processed%20==0):
     p,text,coord,img_s=process_frame(frame)    
     processed_frame.append(img_s)
     fr=p
     cord=coord
     txt=text
    else:
        for index,im in enumerate(fr):
         x1,x2,y1,y2=cord[index]
         position = (int(x1), int(y1))
         (text_width, text_height), baseline = cv.getTextSize(txt[index], cv.FONT_HERSHEY_SIMPLEX, 0.5, 2)
         padding = 5
         rect_top_left = (position[0], position[1] - text_height - padding)
         rect_bottom_right = (position[0] + text_width + 2 * padding, position[1] + padding)
         cv.rectangle(frame, rect_top_left, rect_bottom_right, (0, 0, 255), cv.FILLED)
         cv.putText(frame, txt[index], position, cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv.LINE_AA)
         processed_frame.append(frame)
    print(f"Processed {processed-19}/{length} frames processed")  
    
video = cv.VideoWriter('output.avi', fourcc, fps, (processed_frame[0].shape[1],processed_frame[0].shape[0]))   
for img in processed_frame:
    video.write(img)
    
cv.destroyAllWindows()
video.release()   
cap.release() 