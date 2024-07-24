import cv2 as cv
import os
import easyocr
from plateDetection import plateDetection
from ocrReader import Reader

cv.namedWindow("Resized_Window", cv.WINDOW_NORMAL)
cv.resizeWindow("Resized_Window", 300, 300)
img=cv.imread('tests/download.jpg')
img1,images,coord=plateDetection(img)
text=Reader(images)

x1,x2,y1,y2=coord
cv.putText(img, text[0], (int(x1), int(y1 - 5)),cv.FONT_HERSHEY_SIMPLEX, 0.3, (255,0, 0), 1, cv.LINE_AA)
cv.imshow('Resized_Window', img)
print(text[0])
cv.waitKey(0)