from PyQt6.QtWidgets import QStackedWidget, QApplication
from sys import argv

app = QApplication(argv)
stackedWidget = QStackedWidget()

codecs = {
    'mp4': 'mp4v',
    'avi': 'XVID'
}

modelPath = 'runs/detect/train - dataset 1 --- 40 epoch/weights/best.pt'