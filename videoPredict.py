
import cv2 as cv
import os

cv.namedWindow("Resized_Window", cv.WINDOW_NORMAL) 
cv.resizeWindow("Resized_Window", 600, 600)
img=cv.imread('tests/check1.webp')




# vid= cv.VideoCapture('testVideos/vid1.mp4')p
# fps = vid.get(cv.CAP_PROP_FPS)
# val=0
# frame_delay = int(1000 / fps)  # Delay between frames in milliseconds
# while (vid.isOpened()):
#     val+=1
#     if val==11:
#         val=1
        
#     ret, frame = vid.read()
#     if not ret:
#         break
#     if val%10==0:
#      frame = plateDetection(frame)   
#     cv.imshow('Resized_Window', frame)
#     if cv.waitKey(frame_delay) & 0xFF == ord('q'):
#         break
# vid.release()    


