from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QWidget
from PyQt6.uic import load_ui
from anpr.workspace import Workspace
from anpr import data

class Home(QMainWindow):

    def __init__(self):
        super(Home, self).__init__()
        load_ui.loadUi('app/assets/ui/home.ui', self)
        self.img_btn.clicked.connect(self.go_to_workspace)
    
    def go_to_workspace(self):
        workspace = Workspace()
        data.stackedWidget.addWidget(workspace)
        data.stackedWidget.setCurrentIndex(data.stackedWidget.currentIndex() + 1)