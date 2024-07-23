import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QProgressBar, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QBasicTimer
import progress_bar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Progress Bar Example")
        self.setGeometry(100, 100, 300, 150)

        self.progress_bar = progress_bar.ProgressBar(self)
        self.progress_bar.setGeometry(50, 50, 200, 30)
        self.progress_bar.setValue(30)

        self.button = QPushButton("Start", self)
        self.button.setGeometry(100, 100, 100, 30)
        self.button.clicked.connect(self.start_progress)

        self.timer = QBasicTimer()
        self.step = 0

        layout = QVBoxLayout()
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_progress(self):
        self.progress_bar.increaseValue(30)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
