from PyQt6.QtWidgets import QStackedWidget, QApplication
from sys import argv
import os

app = QApplication(argv)
stackedWidget = QStackedWidget()

codecs = {
    'mp4': 'mp4v',
    'avi': 'XVID'
}

modelPath = 'assets/models/d1-40e.pt'

current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
second_dir = os.path.dirname(current_dir)
project_dir = os.path.dirname(second_dir)

ocrModelPath = os.path.join(project_dir, 'assets\\models\\ocr_model')
