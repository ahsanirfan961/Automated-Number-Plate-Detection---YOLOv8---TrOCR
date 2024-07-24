import cv2
import easyocr
from pylab import rcParams
import numpy as np
from plateDetection import plateDetection

# define the path
path = 'tests/check1.webp'

# read the image
img = cv2.imread(path)
img = cv2.resize(img, (800, 600))

_, img = plateDetection(img)
img = img[0]
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# find the white rectangle
th = img.copy()
th[th<200] = 0

bbox = np.where(th>0)
y0 = bbox[0].min()
y1 = bbox[0].max()
x0 = bbox[1].min()
x1 = bbox[1].max()


# crop the region of interest (ROI)
img = img[y0:y1, x0:x1]

# histogram equalization
equ = cv2.equalizeHist(img)
# Gaussian blur
blur = cv2.GaussianBlur(equ, (5, 5), 1)

# # manual thresholding
th2 = 130 # this threshold might vary!
equ[equ>=th2] = 255
equ[equ<th2]  = 0

# Now apply the OCR on the processed image
rcParams['figure.figsize'] = 8, 16
reader = easyocr.Reader(['en'])


output = reader.readtext(equ)

for i in range(len(output)):
    print(output[i][-2])

cv2.imshow('img', equ)
cv2.waitKey(0)
cv2.destroyAllWindows()