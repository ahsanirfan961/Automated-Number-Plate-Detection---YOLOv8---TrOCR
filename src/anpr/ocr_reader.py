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
            self.workspace.enableVideoPlayerButtons(False)

            self.loadingSignal.emit(30)
            for i, plate in enumerate(self.workspace.plates):
                self.loadingSignal.emit(int(30 + (i/len(self.workspace.plates))*40))
                plate = cv2.cvtColor(plate, cv2.COLOR_BGR2RGB)
                self.workspace.plateTexts.append(self.workspace.ocrReader.read(plate))
            self.loadingSignal.emit(70)

            ext = self.workspace.filename.split('.')[-1]
            codec = data.codecs[ext] 

            fourcc = cv2.VideoWriter_fourcc(*codec)
            out = cv2.VideoWriter(os.getenv('TEMP')+'ocr.'+ext, fourcc, self.workspace.fps, (self.workspace.videoWidth, self.workspace.videoHeight))

            currentFrame = self.workspace.videoCap.get(cv2.CAP_PROP_POS_FRAMES)
            self.workspace.videoCap.set(cv2.CAP_PROP_POS_FRAMES, 0)


            i=0
            while(self.workspace.videoCap.isOpened()):
                ret, frame = self.workspace.videoCap.read()
                if ret:
                    self.loadingSignal.emit(int(70 + (self.workspace.videoCap.get(cv2.CAP_PROP_POS_FRAMES)/self.workspace.frameCount)*25))
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

            self.workspace.enableVideoPlayerButtons(True)

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
    

    def remove_noise(self, image):
        return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 15)



    def get_grayscale(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def thresholding(self, image):
        thresh = cv2.threshold(image,0,255,cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)[1]
        return thresh

    def opening(self, image):
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
        opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
        return opening

    def preprocess_image(self, image):
        dst = self.remove_noise(image)  # Using remove_noise method
        img = self.get_grayscale(dst)
        thresh=self.thresholding(img)
        cv2.imwrite("threshed.jpg",thresh)
        return thresh



