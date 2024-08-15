from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.uic import load_ui
from anpr.image_space import ImageSpace
from anpr.video_space import VideoSpace
from anpr.settings import Settings
from anpr import data
import sys

class Home(QMainWindow):

    settings_window = None

    def __init__(self):
        super(Home, self).__init__()
        load_ui.loadUi('assets/ui/home.ui', self)
        self.img_btn.clicked.connect(self.go_to_imagespace)
        self.vid_btn.clicked.connect(self.go_to_videospace)

        self.settings.clicked.connect(self.go_to_settings)
    
    def go_to_imagespace(self):
        workspace = ImageSpace()
        data.stackedWidget.addWidget(workspace)
        data.stackedWidget.setCurrentIndex(data.stackedWidget.currentIndex() + 1)
    
    
    def go_to_videospace(self):
        workspace = VideoSpace()
        data.stackedWidget.addWidget(workspace)
        data.stackedWidget.setCurrentIndex(data.stackedWidget.currentIndex() + 1)
    
    def go_to_settings(self):
        if self.settings_window is None or not self.settings_window.isVisible():
            self.settings_window = Settings()
            self.settings_window.setFixedSize(500, 250)
            self.settings_window.setWindowTitle("Settings")
            self.settings_window.show()

    
    