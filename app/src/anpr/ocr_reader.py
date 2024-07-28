import cv2, easyocr, os, numpy as np
from PIL import Image
from PyQt6.QtCore import QThread, pyqtSignal
from anpr.workspace import Workspace
from anpr import data
from anpr.plate_detection import MODE_IMAGE, MODE_VIDEO

class OCRReader:
    def __init__(self):
        self.reader = easyocr.Reader(['en'])
        self.preProcessor = ImagePreProcessor()

    def read(self, image):
        result = self.reader.readtext(self.preProcessor.preprocess_image(image))
        for res in result:
            return res[1]


class PlateTextScanner(QThread):
        statusBarSignal = pyqtSignal(str)
        loadingSignal = pyqtSignal(int)
        updateUiSignal = pyqtSignal()

        def __init__(self, workspace: 'Workspace', mode: 'int'):
            super().__init__()
            self.workspace = workspace
            self.mode = mode
        
        def detectFromImage(self):
            for plate in self.workspace.plates:
                plate = cv2.cvtColor(plate, cv2.COLOR_BGR2RGB)
                self.workspace.plateTexts.append(self.workspace.ocrReader.read(plate))
            self.loadingSignal.emit(70)

            self.workspace.markPlatesText(self.workspace.canvasImage, self.workspace.plateCoords, self.workspace.plateTexts)
            self.loadingSignal.emit(85)
        
        def detectFromVideo(self):
            for plate in self.workspace.plates:
                plate = cv2.cvtColor(plate, cv2.COLOR_BGR2RGB)
                self.workspace.plateTexts.append(self.workspace.ocrReader.read(plate))
            self.loadingSignal.emit(70)

            ext = self.workspace.filename.split('.')[-1]
            codec = data.codecs[ext] 

            fourcc = cv2.VideoWriter_fourcc(*codec)
            out = cv2.VideoWriter(os.getenv('TEMP')+'ocr.'+ext, fourcc, self.workspace.fps, (self.workspace.videoWidth, self.workspace.videoHeight))
            self.loadingSignal.emit(75)

            currentFrame = self.workspace.videoCap.get(cv2.CAP_PROP_POS_FRAMES)
            self.workspace.videoCap.set(cv2.CAP_PROP_POS_FRAMES, 0)

            self.loadingSignal.emit(80)

            i=0
            while(self.workspace.videoCap.isOpened()):
                ret, frame = self.workspace.videoCap.read()
                if ret:
                    self.workspace.markPlatesText(frame, self.workspace.plateCoords[i], self.workspace.plateTexts)
                    out.write(frame)
                else:
                    break
                i=i+1
            
            self.loadingSignal.emit(95)
            self.workspace.videoCap.release()
            out.release()

            self.workspace.videoCap = cv2.VideoCapture(os.getenv('TEMP')+'ocr.'+ext)
            self.workspace.videoCap.set(cv2.CAP_PROP_POS_FRAMES, currentFrame)
            self.workspace.getVideoFrame()

        def run(self):
            self.loadingSignal.emit(5)
            if self.workspace.ocrReader is None:
                self.workspace.ocrReader = OCRReader()
            self.loadingSignal.emit(20)

            if self.mode == MODE_IMAGE:
                self.detectFromImage()
            elif self.mode == MODE_VIDEO:
                self.detectFromVideo()

            self.workspace.populatePlateTextTable()
            self.loadingSignal.emit(100)
            self.updateUiSignal.emit()
            self.statusBarSignal.emit('Successfuly scanned for number plates text!')


class ImagePreProcessor:

    def Normalize_image(self, image):
        norm_img = np.zeros((image.shape[0], image.shape[1]))
        img1 = cv2.normalize(image, norm_img, 0, 255, cv2.NORM_MINMAX)
        return img1

    def deskew(self, image):
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

    def set_image_dpi(self, opencv_image):
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

    def remove_noise(self, image):
        return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 15)

    def thining(self, image):
        kernel = np.ones((5,5),np.uint8)
        erosion = cv2.erode(image, kernel, iterations = 1)
        return erosion
    
    def get_grayscale(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def thresholding(self, image):
        _, img = cv2.threshold(image, 64, 255, cv2.THRESH_BINARY_INV)
        return img

    def preprocess_image(self, image):
        img=self.get_grayscale(image)
        img2=self.thresholding(img)
        return img2
    


