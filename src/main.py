from sys import exit
from anpr.home import Home
from anpr import data

import multiprocessing
multiprocessing.freeze_support()

home = Home()
data.stackedWidget.setWindowTitle('Automated Number Plate Recognizer')
data.stackedWidget.addWidget(home)
data.stackedWidget.setMinimumSize(1200, 600)
data.stackedWidget.show()

if __name__=="__main__":
    try:
        exit(data.app.exec())
    except Exception as e:
        print(e)
        print('Exiting')