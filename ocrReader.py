import easyocr
import cv2 as cv
import os
from plateDetection import plateDetection

def Reader(imges):
 reader = easyocr.Reader(['en'])
 txt=[]
 for img in imges:
     t=''
     result=reader.readtext(img)
     for res in result:
         t+=res[1]
     txt.append(t)
 return txt    

