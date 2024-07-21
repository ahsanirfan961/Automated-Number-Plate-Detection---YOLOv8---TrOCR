# Automated Number Plate Detection System
This is a software to detect number plates of cars uing Computer Vision and AI. It can dtect and read number plates from an image, a video or from live camera.

### Tools Used and Dependency versions:
1. Python V 3.11 (Important)
2. Yolov8n
3. EasyOCR
4. OpenCV (Contrib version 4.8.0.74)
5. Numpy (Version 1.26.4)

## All the versions mentioned above should me followed. A specific bug will arise when using EasyOCR. To solve the following bug:
 1. open directory containing EasyOCR package in Python Directory and open file named 'easyocr.py'.
 2. in top import line look for the line contaning 'from bidi.algorithms import .......' and replace the word 'bidi.algorithm' with just bidi and save the file.


### Dataset
The dataset is taken from kaggle. It contains almost 30k images from a diverse range of vehicles. It is annotated in Yolo v5 format.\
Link: [here](https://www.kaggle.com/datasets/abrahman97/number-plate-recognition-dataset)

### Model
The YOLO pre-trained model (yolov8n.pt) on COCO dataset in used. It is then fine tuned on custom dataset.

### Training 
The training is done on custom dataset for 40 epochs using CUDA support. It took arround 4.5 hours to train. 

The confusion matrix for training is as under:
![matrix](https://github.com/ahsanirfan961/Automated-Number-Plate-Detection---YOLOv8---EasyOCR/blob/main/runs/detect/train%20-%20dataset%201%20---%2040%20epoch/confusion_matrix_normalized.png)

The results of the training are as under:
![results](https://github.com/ahsanirfan961/Automated-Number-Plate-Detection---YOLOv8---EasyOCR/blob/main/runs/detect/train%20-%20dataset%201%20---%2040%20epoch/results.png)

### Testing on Test Set
When the model is tested on a new test set, it gives the following results:
![test set results](https://github.com/ahsanirfan961/Automated-Number-Plate-Detection---YOLOv8---EasyOCR/blob/main/runs/detect/test%20-%20dataset%201%20---%2040%20epoch/predict%201.png)


### Note
1. update absolute path for each dataset in Dataset Folder/data.yaml
2. The format of dataset folder is dataset/images/test\
                                   dataset/images/val\
                                   dataset/images/train\
                                   dataset/labels/train\
                                   dataset/labels/train\
                                   dataset/labels/train\
