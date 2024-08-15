from PyQt6.QtWidgets import QMainWindow
from PyQt6.uic import load_ui
from PyQt6.QtCore import QObject, QThread, pyqtSignal
from anpr.image_space import ImageSpace
from anpr.video_space import VideoSpace
from anpr.downloader import Downloader
from anpr import data
import os

 
class Settings(QMainWindow):

    downloader = None
    model_downloaded = pyqtSignal()

    def __init__(self):
        super(Settings, self).__init__()
        load_ui.loadUi('assets/ui/settings.ui', self)
        
        self.download.clicked.connect(self.download_model)
        self.model_downloaded.connect(self.validateModels)

        self.validateModels()
    
    def download_model(self):
        if self.downloader is not None:
            self.downloader.deleteLater()
            self.downloader = None

        # Create a new Downloader window
        self.downloader = Downloader(self.model_downloaded)
        self.downloader.setWindowTitle("Downloader")
        self.downloader.setFixedSize(self.downloader.width(), self.downloader.height())
        self.downloader.show()
        self.download.setEnabled(False)
    
    def validateModels(self):
        self.download.setEnabled(True)
        self.detection_model_lbl.setText(self.getDetectionModel())
        self.ocr_model_lbl.setText(self.getOCRModel())

    def getDetectionModel(self):
        if os.path.exists(data.DETECTION_MODEL_PATH):
            return data.DETECTION_MODEL_NAME
        else:
            return 'No model found!'
    
    def getOCRModel(self):
        if 'model.safetensors' in os.listdir(data.OCR_MODEL_PATH):
            self.download.setEnabled(False)
            return data.OCR_MODEL_NAME
        elif os.path.exists(data.OCR_MODEL_DOWNLOAD_PATH):
            if data.getOcrModelCachePath() is not None:
                data.copy_files(data.getOcrModelCachePath(), data.OCR_MODEL_PATH)
                self.download.setEnabled(False)
                return data.OCR_MODEL_NAME
            else:
                return 'No model found!'
        else:
            return 'No model found!'
