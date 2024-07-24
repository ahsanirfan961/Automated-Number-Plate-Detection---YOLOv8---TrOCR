import cv2

try:
    img = cv2.imread('a.png')
except:
    print('cant load')