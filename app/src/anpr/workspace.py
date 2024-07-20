from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QWidget
from PyQt6.uic import load_ui

class Workspace(QMainWindow):

    def __init__(self):
        super(Workspace, self).__init__()
        load_ui.loadUi('app/assets/ui/workspace.ui', self)