import cv2 
import numpy as np
from plateDetection import plateDetection

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #img=cv2.medianBlur(gray,3)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV)
    return gray


cv2.namedWindow("Resized_Window", cv2.WINDOW_NORMAL) 
cv2.resizeWindow("Resized_Window", 20, 10)
img= cv2.imread('tests/download.jpg')

img1,images,coord=plateDetection(img)
cv2.imshow('Resized_Window', preprocess_image(images[0]))
cv2.waitKey(0)  