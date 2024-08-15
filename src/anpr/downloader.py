from PyQt6.QtWidgets import QMainWindow, QMessageBox, QLabel
from PyQt6.QtCore import QObject, QThread, pyqtSignal, QTimer
from PyQt6.uic import load_ui
from anpr import data
from anpr.progress_bar import ProgressBar
import re, contextlib, logging, os, shutil
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
import sys

class Downloader(QMainWindow):

    user_closed = True

    def __init__(self, downloadSignal):
        super(Downloader, self).__init__()
        load_ui.loadUi('assets/ui/downloader.ui', self)
        
        self.progressBar = ProgressBar(self.centralwidget, shouldHide=False)
        self.centralwidget.layout().addWidget(self.progressBar)
        self.progressBar.show()

        self.success = downloadSignal

        print('downloader created')

        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr

        self.resetStdout()

        self.downloaderThread = OCRModelDownloader(self, self.progressBar)
        self.downloaderThread.progress.connect(self.progressBar.update)
        self.downloaderThread.reset_progress.connect(self.progressBar.reset)
        self.downloaderThread.closeSignal.connect(self.closeForcefully)
        self.downloaderThread.finished.connect(self.downloaderThread.deleteLater)
        self.downloaderThread.start()
    
    def resetStdout(self):
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr
    
    def closeEvent(self, event):
        if self.user_closed:
            # Perform your task if the user closes the window
            print("User is closing the window. Performing cleanup task...")

            # Optional: Show a confirmation dialog before closing
            reply = QMessageBox.question(
                self, 'Confirm Exit',
                "Are you sure you want to exit?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                self.resetStdout()
                if self.downloaderThread.isRunning():
                    self.downloaderThread.terminate()
                # self.downloaderThread.requestInterruption()
                # self.downloaderThread.wait()
                self.success.emit()
                event.accept()  # Close the window
                # self.deleteLater()
            else:
                event.ignore()  # Ignore the close event and keep the window open
        else:
            self.success.emit()
            event.accept()
            # self.deleteLater()
    
    def closeForcefully(self):
        self.user_closed = False
        self.close()


class OCRModelDownloader(QThread):
    progress = pyqtSignal(int)
    reset_progress = pyqtSignal()
    progress_data = pyqtSignal(dict)
    closeSignal = pyqtSignal()

    def __init__(self, downloaderWindow: Downloader, progressbar: ProgressBar):
        super().__init__()
        self.downloaderWin = downloaderWindow

        self.progress_data.connect(self.updateProgress)
        self.progressBar = progressbar
        print('thread created')

        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr

        # self.counter = 1
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.checkRunningStatus)
        # self.timer.start(1000)

        self.downloaderWin.status.setText('Downloader initializing...')

    def run(self):
        try:
            print('thread started')
            self.downloaderWin.status.setText('Redirecting output...')
            capturer = RealtimeOutputCapturer(self.progress_data)
            with contextlib.redirect_stdout(capturer), contextlib.redirect_stderr(capturer):
                # Set up logging to also go to the same capturer
            # logging.basicConfig(level=logging.INFO)
            # logging.getLogger().addHandler(logging.StreamHandler(capturer))

                # Download the model and tokenizer
                self.downloaderWin.status.setText('Downloading....')
                processor = TrOCRProcessor.from_pretrained(data.OCR_MODEL_NAME_REMOTE)
                model = VisionEncoderDecoderModel.from_pretrained(data.OCR_MODEL_NAME_REMOTE)

            self.downloaderWin.status.setText('Copying Files...')
            cache_path = data.getOcrModelCachePath()
            if cache_path is not None:
                data.copy_files(cache_path, data.OCR_MODEL_PATH)
            else:
                raise Exception('Cant download model')
            
            self.downloaderWin.status.setText('Downloading completed successfully')
            print("successful")
            self.closeSignal.emit()
        except Exception as e:
            print(e)
            print('Error while downloading!')
            self.closeSignal.emit()
        finally:
            self.resetStdout()
        
    
    def updateProgress(self, data: dict):
        self.downloaderWin.filename.setText(data['filename'])
        self.downloaderWin.downloaded.setText(data['downloaded_size'])
        self.downloaderWin.totalsize.setText(data['total_size'])
        self.downloaderWin.elapsedtime.setText(data['elapsed_time'])
        self.downloaderWin.estimatedtime.setText(data['estimated_time'])
        self.downloaderWin.speed.setText(data['speed'])
        if self.progressBar.value() > int(data['percentage']):
            self.reset_progress.emit()
        self.progress.emit(int(data['percentage']))

    def resetStdout(self):
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr


    
class RealtimeOutputCapturer:
    def __init__(self, emit_signal):
        self.emit_signal = emit_signal

    def write(self, message):
        if message.strip():  # Only emit non-empty messages
            parsed_output = self.parse_progress_output(message.strip())
            
            if parsed_output:
                self.emit_signal.emit(parsed_output)

    def flush(self):
        pass  # No need to flush as we're handling real-time updates

    def parse_progress_output(self, message):
        # Regex to capture the progress output format
        regex = (
            r'(?P<filename>[\w\.-]+):\s*'                # Match the filename followed by ':'
            r'(?P<percentage>\d+)%\|'                     # Match the percentage (e.g., 100%) and pipe '|'
            r'.*\|'                                       # Match the progress bar, which could be any character sequence
            r'\s*(?P<downloaded_size>[\d\.]+[kMG]?)?'     # Match the downloaded size, which could be missing
            r'(\/(?P<total_size>[\d\.]+[kMG]?))?'         # Match the total size, which could be missing (along with the '/')
            r'\s*\[?'                                     # Match the optional starting square bracket
            r'(?P<elapsed_time>[\d\:]+)?'                 # Match the elapsed time, which could be missing
            r'(<(?P<estimated_time>[\d\:]+))?'            # Match the estimated time, which could be missing
            r',?\s*(?P<speed>[\d\.]+[kMG]?B/s)?'          # Match the speed, which could be missing
            r'\]?'
        )
        match = re.search(regex, message)
        if match:
            progress_data = {
                "filename": match.group("filename"),
                "percentage": match.group("percentage"),
                "downloaded_size": match.group("downloaded_size"),
                "total_size": match.group("total_size"),
                "elapsed_time": match.group("elapsed_time"),
                "estimated_time": match.group("estimated_time"),
                "speed": match.group("speed")
            }
            return progress_data
        return None