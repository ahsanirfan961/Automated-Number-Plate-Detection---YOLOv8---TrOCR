from PyQt6.QtWidgets import QStackedWidget, QApplication
import sys

app = QApplication(sys.argv)
stackedWidget = QStackedWidget()

codecs = {
    'mp4': 'mp4v',
    'avi': 'XVID'
}