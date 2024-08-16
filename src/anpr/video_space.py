from anpr.workspace import *
from PyQt6.QtGui import QPixmap
from anpr import data
from PyQt6 import uic
from anpr.plate_detection import *
from anpr.ocr_reader import *
from PyQt6.QtCore import QThread, pyqtSignal
from statistics import mode
from time import sleep
from cv2 import CAP_PROP_FPS, CAP_PROP_FRAME_COUNT
from anpr.plate_detection import YoloPlateDetector

class VideoSpace(Workspace):

    videoCap = VideoCapture()
    videoRunning = False
    videoPlayer = None 
    videoLoaded = False
    videoMoveOffsetSeconds = 5
    videoWriter = None

    def __init__(self):
        super().__init__()

        self.initCanvasImage = QPixmap('assets/images/reel icon small.png')
        self.resetCanvas()

        self.newFileTypes = 'MP4 AVI MKV (*.mp4 *.avi)'
        self.saveFileTypes = 'MP4 (*.mp4);;AVI (*.avi)'

        # Add Video Player Bar
        self.videoBar = uic.load_ui.loadUi('assets/ui/video_bar.ui')
        canvasLayout = self.canvasFrame.layout()
        canvasLayout.addWidget(self.videoBar)

        self.videoBar.play_btn.clicked.connect(self.playVideo)
        self.videoBar.pause_btn.clicked.connect(self.pauseVideo)
        self.videoBar.forward_btn.clicked.connect(self.forwardVideo)
        self.videoBar.backward_btn.clicked.connect(self.backwardVideo)
        self.videoBar.start_btn.clicked.connect(self.moveToStart)
        self.videoBar.end_btn.clicked.connect(self.moveToEnd)
        self.videoBar.stop_btn.clicked.connect(self.stopVideo)

        self.videoBar.video_slider.sliderMoved.connect(self.moveVideo)

        self.videoPlayer = self.VideoPlayer(self)
        self.videoWriter = self.VideoWriter(self)
        self.videoWriter.loadingSignal.connect(self.loading.update)

    def loadFileFromPath(self, path):
        self.videoCap.release()
        self.videoCap = VideoCapture(path)
        ret, self.canvasImage = self.videoCap.read()
        if not ret:
            self.showStatusBarMessage('Error: Video Cannot Be Loaded!')
            return False
        
        self.fps = self.videoCap.get(CAP_PROP_FPS)
        self.frameCount = self.videoCap.get(CAP_PROP_FRAME_COUNT)
        self.videoLength = int(self.frameCount/self.fps)
        mins = int(self.videoLength/60)
        secs = int(self.videoLength%60)
        if(mins<10):
            mins = f"0{mins}"
        if(secs<10):
            secs = f"0{secs}"

        self.videoWidth = self.canvasImage.shape[1]
        self.videoHeight = self.canvasImage.shape[0]
            
        self.insertRowInTable(self.infoTable, ['Video name', self.filename])
        self.insertRowInTable(self.infoTable, ['Dimensions', f"{self.videoWidth} x {self.videoHeight}"])
        self.insertRowInTable(self.infoTable, ['Video Duration', f"{mins}:{secs}"])
        self.videoLoaded = True
        return True
    
    def playVideo(self):
        if self.videoLoaded:
            if not self.videoPlayer.isRunning():
                self.videoPlayer.start()
            self.videoRunning = True
        else:
            self.showStatusBarMessage('No Video Loaded!')
    
    def pauseVideo(self):
        self.videoRunning = False

    def forwardVideo(self):
        self.videoRunning = False
        currentFrame = self.videoCap.get(CAP_PROP_POS_FRAMES)
        self.videoCap.set(CAP_PROP_POS_FRAMES, currentFrame + int(self.videoMoveOffsetSeconds*self.fps))
        self.getVideoFrame()
        self.updateUi()
        self.videoRunning = True

    def backwardVideo(self):
        self.videoRunning = False
        currentFrame = self.videoCap.get(CAP_PROP_POS_FRAMES)
        self.videoCap.set(CAP_PROP_POS_FRAMES, currentFrame - int(self.videoMoveOffsetSeconds*self.fps))
        self.getVideoFrame()
        self.updateUi()
        self.videoRunning = True
    
    def moveToStart(self):
        self.videoRunning = False
        self.videoCap.set(CAP_PROP_POS_FRAMES, 0)
        self.getVideoFrame()
        self.updateUi()
        self.updateSlider()

    def moveToEnd(self):
        self.videoRunning = False
        self.videoCap.set(CAP_PROP_POS_FRAMES, self.frameCount - 1)
        self.getVideoFrame()
        self.updateUi()
        self.updateSlider()
    
    def stopVideo(self):
        self.moveToStart()
    
    def getVideoFrame(self):
        ret, self.canvasImage = self.videoCap.read()
        if not ret:
            return False
        self.canvasImage = cvtColor(self.canvasImage, COLOR_BGR2RGB)
        return True
    
    def updateSlider(self):
        currentFrame = self.videoCap.get(CAP_PROP_POS_FRAMES)
        self.videoBar.video_slider.setValue(int(1000*(currentFrame/self.frameCount)))
        self.videoBar.time.setText(self.getCurrentVideoTime(self.videoCap))
    
    def moveVideo(self):
        self.videoRunning = False
        movePosition = (self.videoBar.video_slider.value()/1000)*self.frameCount
        self.videoCap.set(CAP_PROP_POS_FRAMES, movePosition)
        self.videoBar.time.setText(self.getCurrentVideoTime(self.videoCap))
        self.getVideoFrame()
        self.updateUi()
    
    def saveFile(self):
        self.videoWriter.start()
    
    def scan(self):
        if self.imageLoaded and len(self.plates) == 0:
            self.detectionTable.clearContents()
            self.detectionTable.setRowCount(0)
            self.scanThread = PlateScanner(self, MODE_VIDEO)
            self.scanThread.statusBarSignal.connect(self.showStatusBarMessage)
            self.scanThread.updateUiSignal.connect(self.updateUi)
            self.scanThread.loadingSignal.connect(self.loading.update)
            self.loading.reset()
            self.plateDetector = YoloPlateDetector()
            self.scanThread.start()
        else:
            if len(self.plates) > 0:
                self.showStatusBarMessage('Already scanned for number plates!')
            else:
                self.showStatusBarMessage('No image loaded!')

    def scanText(self):
        if data.ocrModelExists():
            if self.imageLoaded and len(self.plateTexts) == 0:
                self.plateTextTable.clearContents()
                self.plateTextTable.setRowCount(0)
                self.scanThread = PlateTextScanner(self, MODE_VIDEO)
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

    def getCurrentVideoTime(self, cap):
        currentTime = (cap.get(CAP_PROP_POS_FRAMES)/self.frameCount)*self.videoLength
        mins = int(currentTime/60)
        secs = int(currentTime%60)
        if(mins<10):
            mins = f"0{mins}"
        if(secs<10):
            secs = f"0{secs}"
        return f"{mins}:{secs}"

    def markPlatesText(self, frame, plateCoords, plateTexts):
        for tr_id in plateCoords.keys():
            position = plateCoords[tr_id]
            index = self.track_id.index(tr_id)
            x1, y1, x2, y2 = position['x1'], position['y1'], position['x2'], position['y2']
            # rectangle(frame, (int(x1), int(y1-20)), (int(x2), int(y1)), (0, 255, 0), -1)
            # putText(frame, plateTexts[index], (int(x1+5), int(y1 - 5)),FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, LINE_AA)
            data.put_outlined_text(frame, plateTexts[index], (int(x1+5), int(y1 - 5)), self.textSize, 1)

    def populateDetectionTable(self):
        self.insertRowInTable(self.detectionTable, ['# of plates', f"{len(self.track_id)}"])
        self.insertRowInTable(self.detectionTable, ['Detection Durations', '------------'])
        for i, position in enumerate(self.track_id):
            self.insertRowInTable(self.detectionTable, [f"Plate - {self.track_id[i]}", f"from {self.plateArrivals[i]} to {self.plateRetreats[i]}"])
        self.insertRowInTable(self.detectionTable, ['Accuracy', '------------'])
        totalAcc = 0
        for i, acc in enumerate(self.plateAccuracy):
            self.insertRowInTable(self.detectionTable, [f"Plate - {self.track_id[i]}", f"{round(mode(acc)*100, 2)}%"])
            totalAcc = totalAcc + round(mode(acc)*100, 2)
        self.insertRowInTable(self.detectionTable, ['Total Accuracy', f"{totalAcc/len(self.plateAccuracy)}%"])
    

    def enableVideoPlayerButtons(self, value):
        self.videoBar.play_btn.setEnabled(value)
        self.videoBar.pause_btn.setEnabled(value)
        self.videoBar.forward_btn.setEnabled(value)
        self.videoBar.backward_btn.setEnabled(value)
        self.videoBar.start_btn.setEnabled(value)
        self.videoBar.end_btn.setEnabled(value)
        self.videoBar.stop_btn.setEnabled(value)

    class VideoWriter(QThread):
        loadingSignal = pyqtSignal(int)

        def __init__(self, videoSpace: 'VideoSpace') -> None:
            super().__init__()
            self.videoSpace = videoSpace
        
        def run(self):
            self.loadingSignal.emit(1)
            ext = self.videoSpace.savePath.split('.')[-1]
            codec = data.codecs[ext]

            self.loadingSignal.emit(20)
            fourcc = VideoWriter_fourcc(*codec)
            out = VideoWriter(self.videoSpace.savePath, fourcc, self.videoSpace.fps, (self.videoSpace.videoWidth, self.videoSpace.videoHeight))

            self.loadingSignal.emit(30)
            currentFrame = self.videoSpace.videoCap.get(CAP_PROP_POS_FRAMES)
            self.videoSpace.videoCap.set(CAP_PROP_POS_FRAMES, 0)

            self.loadingSignal.emit(50)
            while(self.videoSpace.videoCap.isOpened()):
                ret, frame = self.videoSpace.videoCap.read()
                if ret:
                    out.write(frame)
                else:
                    break
            self.loadingSignal.emit(90)
            self.videoSpace.videoCap.set(CAP_PROP_POS_FRAMES, currentFrame)
            self.loadingSignal.emit(100)
            self.videoSpace.showStatusBarMessage(f"Video Saved Successfully at {self.videoSpace.savePath}")

    class VideoPlayer(QThread):
        def __init__(self, videoSpace: 'VideoSpace') -> None:
            super().__init__()
            self.videoSpace = videoSpace
        
        def run(self):
            while self.videoSpace.videoCap.isOpened():
                while self.videoSpace.videoRunning:
                    if not self.videoSpace.getVideoFrame():
                        self.videoSpace.videoCap.set(CAP_PROP_POS_FRAMES, 0)
                        self.videoSpace.showStatusBarMessage('Video Finished!')
                        return
                    self.videoSpace.updateUi()
                    self.videoSpace.updateSlider()
                    sleep(1/self.videoSpace.fps)
        
    