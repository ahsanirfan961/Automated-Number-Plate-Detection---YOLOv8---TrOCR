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
import cv2 as cv


position = (int(x1), int(y1))
text = text[0]

(text_width, text_height), baseline = cv.getTextSize(text, cv.FONT_HERSHEY_SIMPLEX, 0.5, 2)

padding = 5

rect_top_left = (position[0], position[1] - text_height - padding)
rect_bottom_right = (position[0] + text_width + 2 * padding, position[1] + padding)


cv.rectangle(img, rect_top_left, rect_bottom_right, (0, 0, 255), cv.FILLED)


cv.putText(img, text, position, cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv.LINE_AA)

cv.imshow('Resized_Window', img)
print(text[0])
cv.waitKey(0)