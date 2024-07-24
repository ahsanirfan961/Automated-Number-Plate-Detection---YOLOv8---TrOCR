from plateDetection import plateDetection
import cv2 as cv
from ocrReader import Reader
import os


img=cv.imread('tests/images.jpg')
img=cv.resize(img, (600, 600))

img, plates = plateDetection(img)

for i, plate in enumerate(plates):
    # histogram equalization
    equ = cv.equalizeHist(img)
    # Gaussian blur
    blur = cv.GaussianBlur(equ, (5, 5), 1)

    # manual thresholding
    th2 = 60 # this threshold might vary!
    equ[equ>=th2] = 255
    equ[equ<th2]  = 0
    cv.imshow(f"{i}", equ)
    print(Reader([equ]))

cv.imshow('img', img)    
cv.waitKey(0)


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


