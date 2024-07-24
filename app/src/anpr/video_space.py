from anpr.workspace import Workspace
from PyQt6.QtGui import QPixmap
from anpr import data
from PyQt6 import uic
from ultralytics import YOLO
from PyQt6.QtCore import QObject, QThread, pyqtSignal
import cv2

class VideoSpace(Workspace):

    filename = ''

    def __init__(self):
        super().__init__()

        self.initCanvasImage = QPixmap('app/assets/images/reel icon small.png')
        self.resetCanvas()

        self.videoBar = uic.load_ui.loadUi('app/assets/ui/video_bar.ui')

        canvasLayout = self.canvasFrame.layout()
        canvasLayout.addWidget(self.videoBar)
