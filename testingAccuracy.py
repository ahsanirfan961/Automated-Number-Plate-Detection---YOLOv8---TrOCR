import cv2 as cv
from singleFrameComplete import process_frame
cv.namedWindow("Resized_Window", cv.WINDOW_NORMAL)
cv.resizeWindow("Resized_Window", 300, 300)
img=cv.imread('tests/download.jpg')
img=process_frame(img)
cv.imshow('Resized_Window', img)
cv.waitKey(0)