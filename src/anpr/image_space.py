from anpr.workspace import Workspace
from PyQt6.QtGui import QPixmap
from anpr.plate_detection import *
from anpr.ocr_reader import *
from cv2 import imread, COLOR_RGB2BGR
from anpr.plate_detection import YoloPlateDetector

class ImageSpace(Workspace):
 
    def __init__(self):
        super().__init__()
 
        self.initCanvasImage = QPixmap('assets/images/image icon small.png')
        self.newFileTypes = 'PNG JPEG (*.jpg *.png)'
        self.saveFileTypes = 'PNG (*.png);;JPEG (*.jpg)'
        self.plateDetector = YoloPlateDetector()
        self.resetCanvas()

    def loadFileFromPath(self, path):
            self.canvasImage = imread(path)
            if self.canvasImage is None:
                return False
            self.insertRowInTable(self.infoTable, ['Image name', self.filename])
            self.insertRowInTable(self.infoTable, ['Dimensions', f"{self.canvasImage.shape[1]} x {self.canvasImage.shape[0]}"])
            self.insertRowInTable(self.infoTable, ['Size', f"{self.getImageSize()} KB"])
            return True
    
    def saveFile(self):
        saveImg = cvtColor(self.canvasImage, COLOR_RGB2BGR)
        imwrite(self.savePath, saveImg)
        self.showStatusBarMessage(f"Successfully Saved {path.basename(self.savePath)} at {path.dirname(self.savePath)}!")
    
    def scan(self):
        if self.imageLoaded and len(self.plates) == 0:
            self.detectionTable.clearContents()
            self.detectionTable.setRowCount(0)
            self.scanThread = PlateScanner(self, MODE_IMAGE)
            self.scanThread.statusBarSignal.connect(self.showStatusBarMessage)
            self.scanThread.updateUiSignal.connect(self.updateUi)
            self.scanThread.loadingSignal.connect(self.loading.update)
            self.loading.reset()
            self.scanThread.start()
        else:
            if len(self.plates) > 0:
                self.showStatusBarMessage('Already scanned for number plates!')
            else:
                self.showStatusBarMessage('No Video loaded!')
            
    def scanText(self):
        if data.ocrModelExists():
            if self.imageLoaded and len(self.plateTexts) == 0:
                self.plateTextTable.clearContents()
                self.plateTextTable.setRowCount(0)
                self.scanThread = PlateTextScanner(self, MODE_IMAGE)
                self.scanThread.statusBarSignal.connect(self.showStatusBarMessage)
                self.scanThread.updateUiSignal.connect(self.updateUi)
                self.scanThread.loadingSignal.connect(self.loading.update)
                self.loading.reset()
                self.scanThread.start()
            else:
                if len(self.plateTexts) > 0:
                    self.showStatusBarMessage('Already scanned for number plates text!')
                else:
                    self.showStatusBarMessage('No image loaded!')
        else:
            self.showStatusBarMessage('OCR Model not found! Please download the OCR model from the settings menu!')
 
    def populateDetectionTable(self):
        self.insertRowInTable(self.detectionTable, ['# of plates', f"{len(self.plateCoords)}"])
        self.insertRowInTable(self.detectionTable, ['Positions', '------------'])
        for i, position in enumerate(self.plateCoords):
            self.insertRowInTable(self.detectionTable, [f"Plate - {self.track_id[i]}", f"{position['x1']}x{position['y1']}, {position['x2']}x{position['y2']}"])
        self.insertRowInTable(self.detectionTable, ['Accuracy', '------------'])
        totalAcc = 0
        for i, acc in enumerate(self.plateAccuracy):
            self.insertRowInTable(self.detectionTable, [f"Plate - {self.track_id[i]}", f"{round(acc*100, 2)}%"])
            totalAcc = totalAcc + round(acc*100, 2)
        if len(self.plateAccuracy) > 0:
            self.insertRowInTable(self.detectionTable, ['Total Accuracy', f"{totalAcc/len(self.plateAccuracy)}%"])
    
