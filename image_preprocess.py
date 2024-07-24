import cv2
import numpy as np
import cv2
from PIL import Image
import tempfile





#1
def Normalize_image(image):
    norm_img = np.zeros((image.shape[0], image.shape[1]))
    img1 = cv2.normalize(image, norm_img, 0, 255, cv2.NORM_MINMAX)
    return img1



#2
import numpy as np
import cv2

def deskew(image):
    # Find all non-zero points (i.e., points with text)
    co_ords = np.column_stack(np.where(image > 0))

    # Ensure there are non-zero points to process
    if co_ords.size == 0:
        print("No non-zero points found in the image.")
        return image

    print(f"Coordinates shape: {co_ords.shape}")
    print(f"Coordinates dtype: {co_ords.dtype}")

    # Convert coordinates to float32 if necessary
    if co_ords.dtype != np.float32:
        co_ords = np.array(co_ords, dtype=np.float32)

    print(f"Converted coordinates dtype: {co_ords.dtype}")

    # Get the minimum area rectangle that encloses the text
    try:
        angle = cv2.minAreaRect(co_ords.copy())[-1]
    except cv2.error as e:
        print(f"Error in minAreaRect: {e}")
        return image

    # Adjust the angle to ensure it is within the correct range
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    # Get the image dimensions and the center point
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)

    # Get the rotation matrix
    M = cv2.getRotationMatrix2D(center, angle, 1.0)

    # Perform the actual rotation
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    return rotated




#3

def set_image_dpi(opencv_image):
    # Convert OpenCV image (NumPy array) to Pillow image
    im = Image.fromarray(cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB))

    # Get original dimensions
    length_x, width_y = im.size

    # Calculate the resizing factor
    factor = min(1, float(1024.0 / length_x))

    # Calculate the new size
    size = int(factor * length_x), int(factor * width_y)

    # Resize the image
    im_resized = im.resize(size, Image.LANCZOS)

    # Optionally, convert the Pillow image back to OpenCV format
    im_resized_opencv = cv2.cvtColor(np.array(im_resized), cv2.COLOR_RGB2BGR)

    return im_resized_opencv








#4
def remove_noise(image):
  return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 15)

#5
def thining(image):
 kernel = np.ones((5,5),np.uint8)
 erosion = cv2.erode(image, kernel, iterations = 1)

#6
def get_grayscale(image):
 return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)



#7
def thresholding(image):
 return cv2.threshold(image, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) [1]


def preprocess_image(image):
    img=Normalize_image(image)
    img=remove_noise(img)
    img=get_grayscale(image)
   # img=cv2.medianBlur(img,3)
    return cv2.resize(image,(int(image.shape[1]/1),int(image.shape[0]/1)))
    
