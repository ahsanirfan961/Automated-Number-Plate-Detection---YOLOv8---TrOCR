from anpr.workspace import Workspace
from PyQt6.QtGui import QPixmap, QImage
from anpr import data
from ultralytics import YOLO
from PyQt6.QtCore import QObject, QThread, pyqtSignal
import cv2
import numpy as np
import os

class ImageSpace(Workspace):

    filename = ''

    def __init__(self):
        super().__init__()

        self.initCanvasImage = QPixmap('app/assets/images/image icon small.png')
        self.resetCanvas()
    

    def new(self):
        imgPath = self.selectFile()
        if imgPath:
            self.resetTables()
            self.filename = os.path.basename(imgPath)
            self.canvasImage = cv2.imread(imgPath)
            self.resizeFitToCanvas()
            self.canvasImage = cv2.cvtColor(self.canvasImage, cv2.COLOR_BGR2RGB)
            self.savePath = None
            self.imageLoaded = True
            self.updateUi()
            self.showStatusBarMessage(f"Successfully Loaded {self.filename}!")


            self.insertRowInTable(self.infoTable, ['Image name', self.filename])
            self.insertRowInTable(self.infoTable, ['Dimensions', f"{self.canvasImage.shape[1]} x {self.canvasImage.shape[0]}"])
            self.insertRowInTable(self.infoTable, ['Size', f"{self.getImageSize()} KB"])
        else:
            self.showStatusBarMessage(f"Cancelled!")
    
    def save(self):
        if not self.savePath:
            self.saveFile()
        if self.savePath:
            saveImg = cv2.cvtColor(self.canvasImage, cv2.COLOR_RGB2BGR)
            cv2.imwrite(self.savePath, saveImg)
            self.showStatusBarMessage(f"Successfully Saved {os.path.basename(self.savePath)} at {os.path.dirname(self.savePath)}!")
    
    def saveAs(self):
        self.saveFile()
        if self.savePath:
            saveImg = cv2.cvtColor(self.canvasImage, cv2.COLOR_RGB2BGR)
            cv2.imwrite(self.savePath, saveImg)
            self.showStatusBarMessage(f"Successfully Saved {os.path.basename(self.savePath)} at {os.path.dirname(self.savePath)}!")
    
    def updateUi(self):
        height, width, channel = self.canvasImage.shape
        qimage = QImage(self.canvasImage.data, width, height, width*channel, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        self.canvas.setPixmap(pixmap)
    
    def scan(self):
        if self.imageLoaded:
            self.detectionTable.clearContents()
            self.detectionTable.setRowCount(0)
            self.scanThread = ScanImage(self)
            self.scanThread.statusBarSignal.connect(self.showStatusBarMessage)
            self.scanThread.updateUiSignal.connect(self.updateUi)
            self.scanThread.loadingSignal.connect(self.loading.update)
            self.loading.reset()
            self.scanThread.start()
        else:
            self.showStatusBarMessage('No image loaded!')

class ScanImage(QThread):
    statusBarSignal = pyqtSignal(str)
    loadingSignal = pyqtSignal(int)
    updateUiSignal = pyqtSignal()

    def __init__(self, imageSpace):
        super().__init__()
        self.imageSpace = imageSpace

    def run(self):
        self.loadingSignal.emit(5)
        model = YOLO(self.imageSpace.modelPath)
        self.loadingSignal.emit(40)
        prediction = model(self.imageSpace.canvasImage)[0]
        self.loadingSignal.emit(70)

        positions = []
        accuracy = []
        for result in prediction.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = result
            self.imageSpace.markPlate(prediction.names[int(class_id)].upper(), x1, y1, x2, y2)
            positions.append({
                'x1': int(x1),
                'y1': int(y1),
                'x2': int(x2),
                'y2': int(y2),
            })
            accuracy.append(score)
        
        self.loadingSignal.emit(85)

        self.imageSpace.insertRowInTable(self.imageSpace.detectionTable, ['# of plates', f"{len(prediction.boxes.data.tolist())}"])
        self.imageSpace.insertRowInTable(self.imageSpace.detectionTable, ['Positions', '------------'])
        for i, position in enumerate(positions):
            self.imageSpace.insertRowInTable(self.imageSpace.detectionTable, [f"Plate - {i+1}", f"{position['x1']}x{position['y1']}, {position['x2']}x{position['y2']}"])
        self.imageSpace.insertRowInTable(self.imageSpace.detectionTable, ['Accuracy', '------------'])
        for i, acc in enumerate(accuracy):
            self.imageSpace.insertRowInTable(self.imageSpace.detectionTable, [f"Plate - {i+1}", f"{round(acc*100, 2)}%"])
        
        self.loadingSignal.emit(100)
        self.updateUiSignal.emit()
        self.statusBarSignal.emit('Successfuly scanned for number plates!')
