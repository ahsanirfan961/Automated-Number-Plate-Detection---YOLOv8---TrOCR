from PyQt6.QtWidgets import QStackedWidget, QApplication
from PyQt6.QtGui import QIcon
from sys import argv
import os, shutil

import cv2

app = QApplication(argv)
stackedWidget = QStackedWidget()

app.setWindowIcon(QIcon('assets/images/scan icon.png'))

codecs = {
    'mp4': 'mp4v',
    'avi': 'XVID'
}

current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
second_dir = os.path.dirname(current_dir)
project_dir = os.path.dirname(second_dir)

MAIN_DIR = os.path.abspath(os.getcwd())

DETECTION_MODEL_NAME = 'Yolo Fine Tuned\\d1-40e.pt'
DETECTION_MODEL_PATH = os.path.join(project_dir, 'assets\\models\\detection', DETECTION_MODEL_NAME)


OCR_MODEL_NAME = 'TrOCR'
OCR_MODEL_NAME_CACHE = 'models--microsoft--trocr-base-printed'
OCR_MODEL_NAME_REMOTE = 'microsoft/trocr-base-printed'

OCR_MODEL_PATH = os.path.join(project_dir, 'assets\\models\\ocr', OCR_MODEL_NAME)
OCR_MODEL_DOWNLOAD_PATH = os.path.expanduser("~") + f"\\.cache\\huggingface\\hub\\{OCR_MODEL_NAME_CACHE}\\snapshots"


if not os.path.exists(OCR_MODEL_PATH):
    os.mkdir(OCR_MODEL_PATH, 0o666)

# functions
def copy_files(src_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    # Copy files (no need to emit progress for copying)
    for file_name in os.listdir(src_dir):
        src_file = os.path.join(src_dir, file_name)
        dest_file = os.path.join(dest_dir, file_name)
        shutil.copy2(src_file, dest_file)

def getOcrModelCachePath():
    model_download_path = None
    for dir in os.listdir(OCR_MODEL_DOWNLOAD_PATH):
        path = os.path.join(OCR_MODEL_DOWNLOAD_PATH, dir)
        for file in os.listdir(path):
            if file == 'model.safetensors':
                model_download_path = path
    return model_download_path

def ocrModelExists():
    return 'model.safetensors' in os.listdir(OCR_MODEL_PATH)

def put_outlined_text(img, text, position, font_scale, thickness, text_color=(0, 0, 0), outline_color=(255, 255, 255)):
    font = cv2.FONT_HERSHEY_SIMPLEX
    # Draw the outline
    cv2.putText(img, text, position, font, font_scale, outline_color, thickness + 3, lineType=cv2.LINE_AA)

    # Draw the inner text
    cv2.putText(img, text, position, font, font_scale, text_color, thickness, lineType=cv2.LINE_AA)
