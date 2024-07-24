from anpr.workspace import Workspace
from PyQt6.QtGui import QPixmap
from anpr import data
from ultralytics import YOLO
from PyQt6.QtCore import QObject, QThread, pyqtSignal
import cv2

class ImageSpace(Workspace):

    filename = ''

    def __init__(self):
        super().__init__()

        self.initCanvasImage = QPixmap('app/assets/images/image icon small.png')
        self.resetCanvas()

    def loadFileFromPath(self, path):
            self.canvasImage = cv2.imread(path)
            self.insertRowInTable(self.infoTable, ['Image name', self.filename])
            self.insertRowInTable(self.infoTable, ['Dimensions', f"{self.canvasImage.shape[1]} x {self.canvasImage.shape[0]}"])
            self.insertRowInTable(self.infoTable, ['Size', f"{self.getImageSize()} KB"])
    
    def saveFile(self):
        saveImg = cv2.cvtColor(self.canvasImage, cv2.COLOR_RGB2BGR)
        cv2.imwrite(self.savePath, saveImg)
    
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
