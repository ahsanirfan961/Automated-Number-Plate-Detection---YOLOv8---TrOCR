# Automated Number Plate Detection System
This is a software to detect number plates of cars uing Computer Vision and AI. It can dtect and read number plates from an image, a video or from live camera.

### Tools Used
1. Python
2. Yolov8
3. EasyOCR

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
![results](https://github.com/ahsanirfan961/Automated-Number-Plate-Detection---YOLOv8---EasyOCR/edit/main/readme.txt)

### Testing on Test Set
When the model is tested on a new test set, it gives the following results:
![test set results]()


### Note
1. update absolute path for each dataset in Dataset Folder/data.yaml
2. The format of dataset folder is dataset/images/test\
                                   dataset/images/val\
                                   dataset/images/train\
                                   dataset/labels/train\
                                   dataset/labels/train\
                                   dataset/labels/train\
