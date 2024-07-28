import webbrowser, cv2, numpy as np, os
from PyQt6.QtCore import QCoreApplication, QTimer
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QTableWidgetItem
from PyQt6.QtGui import QPixmap
from PyQt6.uic import load_ui
from anpr import data
from anpr.progress_bar import ProgressBar

class Workspace(QMainWindow):

    canvasWidth = 0
    canvasHeight = 0
    initCanvasImage = QPixmap()
    canvasImage = None
    savePath = None
    imageLoaded = False
    DISAPPEAR = True
    DISAPPEAR_FALSE = False
    newFileTypes = ''
    saveFileTypes = ''
    filename = ''
    plates = []
    plateCoords = []
    plateAccuracy = []
    plateTexts = []
    track_id = []
    plateDetector = None
    ocrReader = None
    plateArrivals = []
    plateRetreats = []

    def __init__(self):
        super(Workspace, self).__init__()
        load_ui.loadUi('app/assets/ui/workspace.ui', self)

        QTimer.singleShot(200, self.updateCanvasSize)

        # File Menu
        self.actionNew.triggered.connect(self.new)
        self.actionSave.triggered.connect(self.save)
        self.actionSave_As.triggered.connect(self.saveAs)
        self.actionExport_Stats_to_CSV.triggered.connect(self.exportStatsToCSV)
        self.actionExit.triggered.connect(self.exit)
        self.actionGo_To_Menu.triggered.connect(self.goBack)

        #Help Menu
        self.actionPrivacy_Policy.triggered.connect(self.openPrivacyPolicy)
        self.actionDownload_Code.triggered.connect(self.downloadCode)

        # Vertical Toolbar
        self.new_btn.clicked.connect(self.new)
        self.scan_btn.clicked.connect(self.scan)
        self.scan_text_btn.clicked.connect(self.scanText)
        self.reset_btn.clicked.connect(self.resetCanvas)

        # Loading
        self.loading = ProgressBar(self.statusbar)
        self.loading.setGeometry(500, 4, 300, 12)

        self.scan_text_btn.setDisabled(True)

        # Clear the tables
        self.resetTables()
    
    def resizeEvent(self, event):
        try:
            self.updateCanvasSize()
            self.resizeFitToCanvas()
            self.updateUi()
        except:
            print('')

    def exit(self):
        QCoreApplication.exit(0)
    
    def goBack(self):
        currentWidget = data.stackedWidget.currentWidget()
        data.stackedWidget.removeWidget(currentWidget)
        currentWidget.deleteLater()

    def openPrivacyPolicy(self):
        self.goToGithub()

    def downloadCode(self):
        self.goToGithub()

    def goToGithub(self):
        webbrowser.open('https://github.com/ahsanirfan961/Automated-Number-Plate-Detection---YOLOv8---EasyOCR')

    def resetCanvas(self):
        self.canvas.setPixmap(self.initCanvasImage)
        self.canvasImage = np.ones([self.canvasHeight, self.canvasWidth, 3], dtype=np.uint8)*255
        self.imageLoaded = False
        self.resetTables()
        self.resetLocalData()
        self.showStatusBarMessage('Canvas Reset!')
    
    def selectFile(self, types):
        fileDialog = QFileDialog(self)
        options = QFileDialog.options(fileDialog)
        filePath, _ = QFileDialog.getOpenFileName(self, 'Select a file', 'app/assets/images', types, options=options)
        return filePath
   
    def getSavePath(self, types):
        fileDialog = QFileDialog(self)
        options = QFileDialog.options(fileDialog)
        self.savePath, _ = QFileDialog.getSaveFileName(self, 'Save File As', 'app/assets/images', types, options=options)
    
    def resizeFitToCanvas(self):
        if self.canvasImage.any():
            height, width, channel = self.canvasImage.shape
            # if height > 0 and width > 0:
            if width > height:
                height = int((self.canvasWidth/width)*height)
                self.canvasImage = cv2.resize(self.canvasImage, (self.canvasWidth, height))
            else:
                width = int((self.canvasHeight/height)*width)
                self.canvasImage = cv2.resize(self.canvasImage, (width, self.canvasHeight))
    
    def showStatusBarMessage(self, message, flag=DISAPPEAR):
        self.statusbar.showMessage(message)
        if flag:
            QTimer.singleShot(5000, self.resetStatusBar)
    
    def resetStatusBar(self):
        self.statusbar.showMessage('')
    
    def resetTables(self):
        self.infoTable.clearContents()
        self.detectionTable.clearContents()
        self.plateTextTable.clearContents()
        self.infoTable.setRowCount(0)
        self.detectionTable.setRowCount(0)
        self.plateTextTable.setRowCount(0)

    def insertRowInTable(self, table, row):
        currentRowCount = table.rowCount()
        table.insertRow(currentRowCount)
        for column in range(len(row)):
            table.setItem(currentRowCount, column, QTableWidgetItem(row[column]))
    
    def getImageSize(self):
        ext = self.filename.split('.')[-1]
        _, buffer = cv2.imencode(f".{ext}", self.canvasImage)
        return round(buffer.size/1024, 2)
    
    def markPlates(self, frame, plateCoords, track_id):
        for i, position in enumerate(plateCoords):
            x1, y1, x2, y2 = position['x1'], position['y1'], position['x2'], position['y2']
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.rectangle(frame, (int(x1), int(y2)), (int(x2), int(y2+20)), (0, 255, 0), -1)
            cv2.putText(frame, f"P {track_id[i]}", (int(x1+5), int(y2 + 15)),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)

    def markPlatesText(self, frame, plateCoords, plateTexts):
        for i, position in enumerate(plateCoords):
            x1, y1, x2, y2 = position['x1'], position['y1'], position['x2'], position['y2']    
            cv2.rectangle(frame, (int(x1), int(y1-20)), (int(x2), int(y1)), (0, 255, 0), -1)
            cv2.putText(frame, plateTexts[i], (int(x1+5), int(y1 - 5)),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
    
    def updateCanvasSize(self):
        self.canvasWidth = self.canvas.width()
        self.canvasHeight = self.canvas.height()
    
    def updateUi(self):
        self.resizeFitToCanvas()
        height, width, channel = self.canvasImage.shape
        qimage = QImage(self.canvasImage.data, width, height, width*channel, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        self.canvas.setPixmap(pixmap)

    def save(self):
        if not self.savePath:
            self.getSavePath(self.saveFileTypes)
        if self.savePath:
            self.saveFile()
    
    def saveAs(self):
        self.getSavePath(self.saveFileTypes)
        if self.savePath:
            self.saveFile()

    def new(self):
        filePath = self.selectFile(self.newFileTypes)
        if filePath:
            self.resetTables()
            self.filename = os.path.basename(filePath)
            if self.loadFileFromPath(filePath):
                self.savePath = None
                self.imageLoaded = True
                self.canvasImage = cv2.cvtColor(self.canvasImage, cv2.COLOR_BGR2RGB)
                self.updateUi()
                self.resetLocalData()
                self.scan_text_btn.setEnabled(False)
                self.showStatusBarMessage(f"Successfully Loaded {self.filename}!")
        else:
            self.showStatusBarMessage(f"Cancelled!")

    def populateDetectionTable(self, plateCoords, plateAccuracy, track_id):
        pass

    def populatePlateTextTable(self, plateTexts, track_id):
        pass

    def resetLocalData(self):
        self.plates = []
        self.plateCoords = []
        self.plateAccuracy = []
        self.plateTexts = []
        self.track_id = []
        self.plateArrivals = []
        self.plateRetreats =[]

    def loadFileFromPath(self, path):
        pass

    def exportStatsToCSV(self):
        pass

    def scan(self):
        pass

    def scanText(self):
        pass

    def saveFile(self):
        pass