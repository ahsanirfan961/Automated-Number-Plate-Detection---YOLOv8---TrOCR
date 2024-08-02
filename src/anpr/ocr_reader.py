from PyQt6.QtCore import QThread, pyqtSignal
from anpr.workspace import *
from anpr import data
from anpr.plate_detection import MODE_IMAGE, MODE_VIDEO
from cv2 import CAP_PROP_POS_FRAMES, VideoWriter, VideoWriter_fourcc, VideoCapture, fastNlMeansDenoisingColored, COLOR_BGR2GRAY, threshold, THRESH_BINARY_INV, THRESH_OTSU, MORPH_ELLIPSE, getStructuringElement, morphologyEx, MORPH_OPEN, imwrite
from os import getenv
from easyocr import Reader
from collections import Counter

class OCRReader:
    def __init__(self):
        self.reader = Reader(['en'])
        self.preProcessor = ImagePreProcessor()
        

    def read(self, image):
        result = self.reader.readtext(self.preProcessor.preprocess_image(image))
        for res in result:
            return (res[1], res[2])


class PlateTextScanner(QThread):
        statusBarSignal = pyqtSignal(str)
        loadingSignal = pyqtSignal(int)
        updateUiSignal = pyqtSignal()

        def __init__(self, workspace: 'Workspace', mode: 'int'):
            super().__init__()
            self.workspace = workspace
            self.mode = mode
            self.final_text=[]   # this will hold final processed text of number plate
            
        def longest_words_and_length(self,words):
           if not words:
             return []
           max_length = max(len(word) for word in words)
           longest_words = [word for word in words if len(word) == max_length]
           return longest_words
       
        

        def most_occurring_char_at_index(self,words, index):
          if not words:
            return None

          characters_at_index = [word[index] for word in words]
          char_counter = Counter(characters_at_index)
          most_common = char_counter.most_common(1)
          
          if most_common:
            most_common_char = most_common[0][0]
            
          else:
            most_common_char = None
    
          return most_common_char       
       
       
        def detectFromImage(self):
            for plate in self.workspace.plates:
                plate = cvtColor(plate, COLOR_BGR2RGB)
                result = self.workspace.ocrReader.read(plate)
                if result is None:
                    self.workspace.plateTexts.append(('Nil', 0))
                else:
                    self.workspace.plateTexts.append(result)
            self.loadingSignal.emit(70)

            texts = []
            for text, score in self.workspace.plateTexts:
                texts.append(text)

            self.workspace.markPlatesText(self.workspace.canvasImage, self.workspace.plateCoords, texts)
            self.loadingSignal.emit(85)
        
        def detectFromVideo(self):
            self.workspace.enableVideoPlayerButtons(False)

            self.loadingSignal.emit(30)
            currentFrame = self.workspace.videoCap.get(CAP_PROP_POS_FRAMES)

            # Old Logic
            # for i, plate in enumerate(self.workspace.plates):
            #     self.loadingSignal.emit(int(30 + (i/len(self.workspace.plates))*40))
            #     plate = cvtColor(plate, COLOR_BGR2RGB)
            #     result = self.workspace.ocrReader.read(plate)
            #     if result is None:
            #         self.workspace.plateTexts.append(('Nil', 0))
            #     else:
            #         self.workspace.plateTexts.append(result)


            # New Logic
            self.workspace.videoCap.set(CAP_PROP_POS_FRAMES, 0)
            
            self.workspace.plateTexts = []
            for tr_id in self.workspace.track_id:
                self.workspace.plateTexts.append(('Nil', 0))

            i=0
            dict_store={}
            while(self.workspace.videoCap.isOpened()):
                ret, frame = self.workspace.videoCap.read()
                if ret:
                    self.loadingSignal.emit(int(30 + (self.workspace.videoCap.get(CAP_PROP_POS_FRAMES)/self.workspace.frameCount)*40))
                    for tr_id in self.workspace.plateCoords[i].keys():
                        coord = self.workspace.plateCoords[i][tr_id]
                        plate = frame[coord['y1']:coord['y2'], coord['x1']:coord['x2']]
                        plate = cvtColor(plate, COLOR_BGR2RGB)
                        result = self.workspace.ocrReader.read(plate)
                        if result is None:
                            continue
                        else:
                            text, acc = result
                            if tr_id in dict_store:
                                dict_store[tr_id].append((text,acc))
                            else:
                                dict_store[tr_id]=[(text,acc)]    
                        #if self.workspace.plateTexts[self.workspace.track_id.index(tr_id)][1] < acc:
                         #   self.workspace.plateTexts[self.workspace.track_id.index(tr_id)] = (text, acc)
                else:
                    break
                i=i+1  
            for key in dict_store:
                text_list= [t[0] for t in dict_store[key]]
                text_list=self.longest_words_and_length(text_list)
                print(text_list)
                txt=''
                for i in range(len(text_list[0])):
                    txt+=self.most_occurring_char_at_index(text_list,i)
                self.final_text.append(txt)    
                self.workspace.plateTexts[self.workspace.track_id.index(tr_id)] = (txt, 0.85) 
                
                
                    

            self.loadingSignal.emit(70)

            ext = self.workspace.filename.split('.')[-1]
            codec = data.codecs[ext] 

            fourcc = VideoWriter_fourcc(*codec)
            out = VideoWriter(getenv('TEMP')+'ocr.'+ext, fourcc, self.workspace.fps, (self.workspace.videoWidth, self.workspace.videoHeight))

            self.workspace.videoCap.set(CAP_PROP_POS_FRAMES, 0)

            texts = []
            for text, score in self.workspace.plateTexts:
                texts.append(text)

            i=0
            while(self.workspace.videoCap.isOpened()):
                ret, frame = self.workspace.videoCap.read()
                if ret:
                    self.loadingSignal.emit(int(70 + (self.workspace.videoCap.get(CAP_PROP_POS_FRAMES)/self.workspace.frameCount)*25))
                    self.workspace.markPlatesText(frame, self.workspace.plateCoords[i], texts)
                    out.write(frame)
                else:
                    break
                i=i+1
            
            self.loadingSignal.emit(95)
            self.workspace.videoCap.release()
            out.release()

            self.workspace.videoCap = VideoCapture(getenv('TEMP')+'ocr.'+ext)
            self.workspace.videoCap.set(CAP_PROP_POS_FRAMES, currentFrame)
            self.workspace.getVideoFrame()

            self.workspace.enableVideoPlayerButtons(True)

        def run(self):
            self.loadingSignal.emit(5)
            if self.workspace.ocrReader is None:
                self.workspace.ocrReader = OCRReader()
            self.loadingSignal.emit(20)

            if self.mode == MODE_IMAGE:
                self.detectFromImage()
            elif self.mode == MODE_VIDEO:
                self.detectFromVideo()

            self.workspace.populatePlateTextTable()
            self.loadingSignal.emit(100)
            self.updateUiSignal.emit()
            self.statusBarSignal.emit('Successfuly scanned for number plates text!')


class ImagePreProcessor:
    
    def remove_noise(self, image):
        return fastNlMeansDenoisingColored(image, None, 10, 10, 7, 15)

    def get_grayscale(self, image):
        return cvtColor(image, COLOR_BGR2GRAY)

    def thresholding(self, image):
        thresh = threshold(image,0,255,THRESH_BINARY_INV|THRESH_OTSU)[1]
        return thresh

    def opening(self, image):
        kernel = getStructuringElement(MORPH_ELLIPSE, (2, 2))
        opening = morphologyEx(image, MORPH_OPEN, kernel)
        return opening

    def preprocess_image(self, image):
        dst = self.remove_noise(image)  # Using remove_noise method
        img = self.get_grayscale(dst)
        thresh=self.thresholding(img)
        return thresh