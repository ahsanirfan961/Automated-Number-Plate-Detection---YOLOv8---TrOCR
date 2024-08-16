from ultralytics import YOLO
from anpr.data import DETECTION_MODEL_PATH
from PyQt6.QtCore import QThread, pyqtSignal
from anpr.workspace import Workspace
from cv2 import CAP_PROP_POS_FRAMES, VideoWriter, VideoWriter_fourcc, VideoCapture
from anpr import data
from os import getenv

MODE_IMAGE = 0
MODE_VIDEO = 1

class YoloPlateDetector:

    def __init__(self) -> None:
        self.model = YOLO(data.DETECTION_MODEL_PATH)

    def detect(self, image):
        images=[]
        coord=[]
        accuracy=[]
        track_id = []
        prediction = self.model.track(image)[0]
        for result in prediction.boxes.data.tolist():
            try:
                x1, y1, x2, y2, tr_id, score, class_id = result
                images.append(image[int(y1):int(y2),int(x1):int(x2)])    
                coord.append({
                    'x1': int(x1),
                    'y1': int(y1),
                    'x2': int(x2),
                    'y2': int(y2),
                })
                accuracy.append(score)
                track_id.append(int(tr_id))
            except ValueError:
                print("Unexpected result format:", result)
        return images,coord, accuracy, track_id
    
    def detectAndTrack(self, image):
        images=[]
        coord=[]
        accuracy=[]
        track_id = []
        prediction = self.model.track(image, persist=True)[0]
        for result in prediction.boxes.data.tolist():
            try:
                x1, y1, x2, y2, tr_id, score, class_id = result
                images.append(image[int(y1):int(y2),int(x1):int(x2)])    
                coord.append({
                    'x1': int(x1),
                    'y1': int(y1),
                    'x2': int(x2),
                    'y2': int(y2),
                })
                accuracy.append(score)
                track_id.append(int(tr_id))
            except ValueError:
                print("Unexpected result format:", result)
        return images,coord, accuracy, track_id

class PlateScanner(QThread):
        statusBarSignal = pyqtSignal(str)
        loadingSignal = pyqtSignal(int)
        updateUiSignal = pyqtSignal()

        def __init__(self, workspace: 'Workspace', mode: 'int'):
            super().__init__()
            self.workspace = workspace
            self.mode = mode 
        
        def detectFromImage(self):
            self.workspace.plates, self.workspace.plateCoords, self.workspace.plateAccuracy, self.workspace.track_id = self.workspace.plateDetector.detect(self.workspace.canvasImage)
            self.loadingSignal.emit(70)
            self.workspace.markPlates(self.workspace.canvasImage, self.workspace.plateCoords, self.workspace.track_id)
            self.loadingSignal.emit(85)
        
        def detectFromVideo(self):
            self.workspace.enableVideoPlayerButtons(False)

            ext = self.workspace.filename.split('.')[-1]
            codec = data.codecs[ext]

            fourcc = VideoWriter_fourcc(*codec)
            out = VideoWriter(getenv('TEMP')+'detect.'+ext, fourcc, self.workspace.fps, (self.workspace.videoWidth, self.workspace.videoHeight))
            self.loadingSignal.emit(30)

            currentFrame = self.workspace.videoCap.get(CAP_PROP_POS_FRAMES) 
            self.workspace.videoCap.set(CAP_PROP_POS_FRAMES, 0)

            self.loadingSignal.emit(40)
            while(self.workspace.videoCap.isOpened()):
                ret, frame = self.workspace.videoCap.read()
                self.loadingSignal.emit(int(40 + (self.workspace.videoCap.get(CAP_PROP_POS_FRAMES)/self.workspace.frameCount)*50))
                if ret:
                    plates, coord, accuracy, track_id = self.workspace.plateDetector.detectAndTrack(frame)
                    plateCoordPerFrame = {}
                    for i, tr_id in enumerate(track_id):
                        plateCoordPerFrame[tr_id] = coord[i]
                        if not tr_id in self.workspace.track_id:
                            self.workspace.track_id.append(tr_id)
                            self.workspace.plateArrivals.append(self.workspace.getCurrentVideoTime(self.workspace.videoCap))
                            self.workspace.plateRetreats.append(self.workspace.getCurrentVideoTime(self.workspace.videoCap))
                            self.workspace.plates.append(plates[i])
                            self.workspace.plateAccuracy.append([accuracy[i]])
                        else:
                            index = self.workspace.track_id.index(tr_id)
                            self.workspace.plateRetreats[index] = self.workspace.getCurrentVideoTime(self.workspace.videoCap)
                            self.workspace.plateAccuracy[index].append(accuracy[i])
                            if len(plates[i]) * len(plates[i][0]) > len(self.workspace.plates[index]) * len(self.workspace.plates[index][0]):
                                self.workspace.plates[index] = plates[i]
                    self.workspace.markPlates(frame, coord, track_id)
                    self.workspace.plateCoords.append(plateCoordPerFrame)
                    out.write(frame)
                else:
                    break

            self.workspace.videoCap.release()
            out.release()

            self.loadingSignal.emit(90)
            self.workspace.videoCap = VideoCapture(getenv('TEMP')+'detect.'+ext)
            self.workspace.videoCap.set(CAP_PROP_POS_FRAMES, currentFrame)
            self.workspace.getVideoFrame()

            self.workspace.enableVideoPlayerButtons(True)
        
        def run(self):
            self.loadingSignal.emit(20)
            self.workspace.scan_btn.setDisabled(True)

            if self.mode == MODE_IMAGE:
                self.detectFromImage()
            elif self.mode == MODE_VIDEO:
                self.detectFromVideo()

            self.workspace.populateDetectionTable()
            self.loadingSignal.emit(100)
            self.updateUiSignal.emit()
            self.statusBarSignal.emit('Successfuly scanned for number plates!')
            self.workspace.scan_btn.setEnabled(True)
            self.workspace.scan_text_btn.setEnabled(True)
    
