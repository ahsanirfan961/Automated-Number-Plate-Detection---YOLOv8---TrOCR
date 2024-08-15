from PyQt6.QtWidgets import QProgressBar, QWidget
from PyQt6.QtCore import QTimer

class ProgressBar(QProgressBar):

    def __init__(self, parent: QWidget, shouldHide=True):
        super().__init__(parent)
        self.setMaximum(100)
        self.setStyleSheet("""
                            background-color: rgb(206, 206, 206);
                           color: black;
                           font-size: 10px;
                           text-align: center
                           """)
        self.shouldHide = shouldHide
        self.hide()
    
    def update(self, value):
        self.show()
        if(self.value() >= value or self.value() == 100):
            if(self.value() == 100 and self.shouldHide):
                QTimer.singleShot(5000, self.hide)
            return
        self.setValue(self.value()+1)
        QTimer.singleShot(5, lambda: self.update(value))
    
    def increaseValue(self, value):
        self.update(self.value()+value)
    

