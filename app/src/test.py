import cv2

img = cv2.imread('app/assets/images/unnamed.png')

img = cv2.resize(img, (511, 511))

cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()