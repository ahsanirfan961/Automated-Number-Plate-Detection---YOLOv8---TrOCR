import easyocr
import cv2 as cv
import os
from plateDetection import plateDetection
from image_preprocess import preprocess_image



def Reader(imges):
 reader = easyocr.Reader(['en'])
 txt=[]
 for img in imges:
     t=''
     result=reader.readtext(preprocess_image(img))
     for res in result:
         t+=res[1]
     txt.append(t)
 return txt    

