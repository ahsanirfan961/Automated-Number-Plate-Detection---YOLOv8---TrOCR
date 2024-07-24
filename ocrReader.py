import easyocr
import cv2 as cv
import os
from plateDetection import plateDetection
from image_preprocess import preprocess_image



def Reader(img):
 reader = easyocr.Reader(['en'])
 txt=''
 result=reader.readtext(preprocess_image(img))
 for res in result:
     txt+=res[1]
 return txt    

