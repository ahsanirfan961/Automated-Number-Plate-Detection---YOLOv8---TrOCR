# Automated Number Plate Detection System

This project is a comprehensive tool for number plate detection and optical character recognition (OCR) using a combination of advanced machine learning models and a user-friendly interface. The tool is built using PyQt6 and Python 3.10 and leverages the YOLOv8n model, TR-OCR (Microsoft Open-source model), OpenCV, and Numpy. It can detect and read number plates from images and videos. 


## Table of Contents

- [Automated Number Plate Detection System](#automated-number-plate-detection-system)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Features](#features)
  - [Tools and Libraries Used](#tools-and-libraries-used)
  - [YOLO Model Fine-Tuning](#yolo-model-fine-tuning)
    - [Dataset](#dataset)
    - [Training](#training)
    - [Testing on Test Set](#testing-on-test-set)
    - [Note](#note)
  - [Installation and Setup](#installation-and-setup)
  - [Usage Instructions](#usage-instructions)
  - [Issues](#issues)
  - [Contributing](#contributing)
  - [Contributors](#contributors)
  - [License](#license)

## Overview

This application is designed to detect number plates in images and videos, and perform OCR to extract and display the text from the detected number plates. The tool has been fine-tuned using a large dataset of 28,000 images with their corresponding annotations, making it highly accurate for number plate detection.

## Features

- **Fine-tuned YOLOv8n Model**: Optimized for number plate detection.
- **TR-OCR Integration**: Powerful OCR model from Microsoft for text extraction.
- **Image and Video Processing**: Inference on both images and videos.
- **User-Friendly Interface**: Built with PyQt6 for a seamless experience.

## Tools and Libraries Used

- **PyQt6**: For building the graphical user interface.
- **Python v3.10**: The core programming language.
- **[YOLOv8n](https://docs.ultralytics.com)**: Fine-tuned for number plate detection.
- **[TR-OCR](https://huggingface.co/microsoft/trocr-base-printed)**: Microsoft’s open-source OCR model.
- **OpenCV (Contrib version 4.8.0.74)**: For image and video processing.
- **Numpy (Version 1.26.4)**: For numerical operations.

## YOLO Model Fine-Tuning

The YOLOv8n model has been fine-tuned specifically for number plate detection using a dataset containing 28,000 images and their corresponding annotations. This extensive dataset has allowed the model to achieve high accuracy and reliability in detecting number plates in a variety of conditions.

### Dataset
The dataset is taken from kaggle. It contains almost 30k images from a diverse range of vehicles. It is annotated in Yolo v5 format.\
Link: [here](https://www.kaggle.com/datasets/abrahman97/number-plate-recognition-dataset)

### Training 
The training is done on custom dataset for 40 epochs using CUDA support. It took arround 4.5 hours to train. (We don't have strong paid GPUs 😂)

The confusion matrix for training is as under:
![matrix](./runs/detect/train%20-%20dataset%201%20---%2040%20epoch/confusion_matrix.png)

The results of the training are as under:
![results](./runs/detect/train%20-%20dataset%201%20---%2040%20epoch/results.png)

### Testing on Test Set
When the model is tested on a new test set, it gives the following results:
![test set results](./samples/sample%201.jpg)


### Note
1. update absolute path for each dataset in Dataset Folder/data.yaml
2. The format of dataset folder is dataset/images/test\
                                   dataset/images/val\
                                   dataset/images/train\
                                   dataset/labels/train\
                                   dataset/labels/train\
                                   dataset/labels/train\


## Installation and Setup

To install and set up the tool, follow these steps:

1. **Download the Installer**: Download the `.exe` installer from the release page.
2. **Run the Installer**: Follow the installation steps provided by the installer.
3. **Initial Setup**:
    - Run the anpr.exe as an **administrator**. (Writing files and making directories in `Program Files` require aministrator permissions)
    - Upon first launch, click on the settings icon in the lower left corner of the app.
    - Click on the "Download" button to download the OCR model. This process will require approximately 1.5 GB of space and is a one-time process. (Detection model is pre-installed in the application)
    - **Note:** if the downloader fails, restart the application

## Usage Instructions

Once the initial setup is complete, you can start using the tool for number plate detection and OCR:

1. **Launch the Application**.
2. **Image/Video Inference**:
   - On the main page, select either "Image" or "Video" for inference.
   - If you select "Image", a new window will open.
   - In the new window, use the left option tray:
     - **Load Image/Video**: Click the first option to load the file.
     - **Run YOLO Inference**: Click the second option to run the YOLO model. This may take 1-2 minutes.
     - **Run OCR Inference**: Click the third option to run the OCR model. This may take about a minute.
   - The results will be rendered on the image/video and displayed in tables on the right side of the app.

## Issues
1. The application requires **administartor** access when run for the first time and when downloading models.
2. The **downloader might not work** if stopped by user and reopned. The user needs to **restart the application** to use the downloader again.
3. The text scaling in the detected images/videos might not work correctly, sometimes. Refer to the data tables provided in the right tab of the workspace

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request. Issues and suggestions are also welcome.

## Contributors
- **Muhammad Ahsan**
  - Email: muahsan.bese22seecs@seecs.edu.pk
  - LinkedIn: [Muhammad Ahsan](https://www.linkedin.com/in/muhammad-ahsan-b6796124b/)

- **Muhammad Nabeel**
  - Email: mnabeel.bese22seecs@seecs.edu.pk
  - LinkedIn: [Muhammad Nabeel](https://www.linkedin.com/in/muhammed-nabeel-2a9412246/)


## License

This project is licensed under the MIT License. See the LICENSE file for more details.
