import cv2 as cv
import os
import easyocr
from plateDetection import plateDetection
from ocrReader import Reader

def process_frame(img):
 img1,images,coord=plateDetection(img)
 cache=[]
 for index,im in enumerate(images):
        text=Reader(im)
        cache.append(text)
        x1,x2,y1,y2=coord[index]
        position = (int(x1), int(y1))
        text = text
        (text_width, text_height), baseline = cv.getTextSize(text, cv.FONT_HERSHEY_SIMPLEX, 0.5, 2)
        padding = 5
        rect_top_left = (position[0], position[1] - text_height - padding)
        rect_bottom_right = (position[0] + text_width + 2 * padding, position[1] + padding)
        cv.rectangle(img, rect_top_left, rect_bottom_right, (0, 0, 255), cv.FILLED)
        cv.putText(img, text, position, cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv.LINE_AA)
 return images,cache,coord,img
