
# Smart Retail Checkout System

## Description
Upon reaching the checkout counter, customers place their items on the
designated area, initiating the process of automated product recognition using
cutting-edge image processing and computer vision technologies. The system
detects and recognizes the items without manual barcode scanning, displaying
a real-time breakdown of recognized products on a screen. Then the system
generates the bill. After a successful transaction, a digital or printed receipt is
provided, summarizing the purchased items and payment details, culminating
in a seamless and accurate shopping experience.


## Installation
For the training phase of this project, it is essential to use OpenCV version 3.4.11. Please ensure that you have the correct version installed to maintain compatibility and achieve optimal results. You can download OpenCV version 3.4.11 from the following link:

[Download OpenCV 3.4.11](https://sourceforge.net/projects/opencvlibrary/files/3.4.11/opencv-3.4.11-vc14_vc15.exe/download)
    

After this you can find the files we will need inside the following path 
    
    opencv/build/x64/vc15/bin



## Products Detection
This section outlines the process followed to train an object detection model using the Viola-Jones algorithm. The workflow involves several key steps, ensuring a structured approach to achieve accurate and efficient results.

#### 1. Data Collection
In order to get the best possible set of images in less time,
we used a [Data Collection Script](/object_detection/datacollection.py) that uses OpenCV to capture and save images from the webcam, with adjustable camera settings, image resizing, and the ability to filter and store images based on their sharpness in order to get the best possible set of images.

The output of this process is two folders
- Positive images: Images that has the products we want to detect.
- Negative images: Images that has distracting objects or backgrounds.

#### 2. Positive Images Annotation
Annotating the positive images means drawing rectangle over the objects.

We used opencv_annotation tool to annotate positive images, producing a pos.txt file which will be needed for the next steps.

To achieve this step you'll need to run this command:

    path/to/your/opencv_annotation.exe -annotations=path/to/your/pos.txt --images=path/to/your/positive_images/ -m=1 -r=5

    -m (optional) : if the input image is larger in height then the given resolution here, resize the image for easier annotation, using --resizeFactor.
    -r (optional) : factor used to resize the input image when using the --maxWindowHeight parameter.
    
    Example:
     E:/Project/opencv/build/x64/vc15/bin/opencv_annotation.exe -annotations=E:/Project/object_detection/data/pos.txt --images=E:/Project/object_detection/data/positive_images -m=1 -r=5
    
The output of this step is pos.txt file looks something like this:

    img/img1.jpg  1  140 100 45 45
    img/img2.jpg  2  100 200 50 50   50 30 25 25

Image img1.jpg contains single object instance with the following coordinates of bounding rectangle: (140, 100, 45, 45). Image img2.jpg contains two object instances.

This steps adds more accuracy in the training phase.

#### 3. Positive Samples Compilation
In this step, we use the pos.txt file along with OpenCV's opencv_createsamples utility to compile positive samples, resulting in the creation of a pos.vec file.

To achieve this step you'll need to run this command:

    path/to/your/opencv_createsamples.exe -info path/to/your/pos.txt -w 24 -h 24 -num 50 -vec path/to/your/pos.vec

    Example:
    E:/Project/opencv/build/x64/vc15/bin/opencv_createsamples.exe -info E:/Project/object_detection/data/pos.txt -w 24 -h 24 -num 50 -vec E:/Project/object_detection/data/pos.vec
It's recommended to use -w 24 -h 24 for window size.

-num must be larger than the number of the positive samples.

#### 4. Model Training
using opencv_traincascade, the pos.vec file, and the negative images we will be able to generate a model.xml file which will be used in the detection phase.

To achieve this step you'll need to run this command:

    path/to/your/opencv_traincascade.exe -data path/to/your/output_folder/ -vec path/to/your/pos.vec -bg path/to/your/bg.txt -w 24 -h 24 -numPos 200 -numNeg 350 -numStages 10

    Example:
    E:/Project/opencv/build/x64/vc15/bin/opencv_traincascade.exe -data E:/Project/object_detection/data/model -vec E:\Project\data\pos.vec -bg E:/Project/object_detection/data/negative_images/bg.txt -w 24 -h 24 -numPos 200 -numNeg 350 -numStages 10

- -data is the output file that contains the cascade.xml file (the model)
- -vec is the path of the pos.vec file which was generated in step #3
- -bg is the path to bg.txt file which is a text file that contains the paths to all negative images, you can run the following script inside the negative images folder to generate this file

        dir /b *.jpg >bg.txt

- -w 24 -h 24 must be the set same as the previous step
- -numPos must be smaller than the number of positive samples
- -numStages number of stages of training 

#### 5. Product Detection

By supplying the cascade.xml file to [detection.py](/object_detection/detection.py) file you can detect objects, providing a GUI for model parameters to improve detection if needed.

## Products Classification
#### 1. Dataset Preprocessing 
This Python script utilizes the scikit-learn (sklearn), NumPy (numpy), OpenCV (cv2), and pandas libraries to preprocess images for a machine learning dataset. The primary purpose is to enhance the images for better model performance by applying various image processing techniques like Histogram Equalization and Image Filtering.

Ensure the required libraries (scikit-learn, NumPy, OpenCV, os, pandas) are installed.
```sh
    pip install scikit-learn numpy opencv-python pandas
```

This is how to run the dataset preprocessing script:
```sh
    python .\dataset_preproc.py
```

#### 2. Model Training 
This Python script conducts an image classification experiment using Histogram of Oriented Gradients (HOG) features and Support Vector Machine (SVM) for classification. The experiment utilizes the scikit-learn (sklearn), NumPy (numpy), OpenCV (cv2), and pandas (pandas) libraries. The goal is to train an SVM model to classify preprocessed images based on features extracted using the HOG descriptor.

Ensure the required libraries (scikit-learn, NumPy, OpenCV, os, pandas) are installed.
```sh
    pip install scikit-learn numpy opencv-python pandas joblib
```

This is how to run the model training script:
```sh
    python .\lab_class_train.py
```

#### 3. Test images preprocessing (output from detection stage)
This Python script utilizes the scikit-learn (sklearn), NumPy (numpy), OpenCV (cv2), and pandas libraries to preprocess test images (real-time step). The primary purpose is to enhance the test images to match the dataset after preprocessing for better model performance by applying various image processing techniques like Histogram Equalization and Image Filtering.

Ensure the required libraries (scikit-learn, NumPy, OpenCV, os, pandas) are installed.
```sh
    pip install scikit-learn numpy opencv-python pandas
```

This is how to run the test images preprocessing script:
```sh
    python .\test_preproc.py
```

#### 4. Prediction stage
This Python script evaluates a trained image classification model using Histogram of Oriented Gradients (HOG) features and Support Vector Machine (SVM). The experiment utilizes the scikit-learn (sklearn), NumPy (numpy), OpenCV (cv2), and the joblib library for model loading. The model predicts labels for each test image and compares them to the ground truth. Accuracy is calculated based on correct predictions.

Ensure the required libraries (scikit-learn, NumPy, OpenCV, os, pandas) are installed.
```sh
    pip install scikit-learn numpy opencv-python pandas
```

This is how to run the prediction script:
```sh
    python .\lab_class_predict.py
```

## References

 - Umer, S., Mohanta, P.P., Rout, R.K. et al. Machine learning method for cosmetic product recognition: a visual searching approach. Multimed Tools Appl 80, 34997–35023 (2021). https://doi.org/10.1007/s11042-020-09079-y
## Authors

- [@MostafaBinHani](https://github.com/MostafaBinHani)
- [@fatmaebrahim](https://github.com/fatmaebrahim)
- [@MohammadAlomar8](https://github.com/MohammadAlomar8)
- [@mou-code](mou-code)
- [@RawanMostafa08](https://github.com/RawanMostafa08)


## How to use our application

### Installation
    

### Screenshots

![WhatsApp Image 2023-12-25 at 22 31 02_a09ac34e](https://github.com/mou-code/Smart-Retail-Checkout-System/assets/97397431/f3656afb-dce7-43a4-877e-e0da5fd6f3b6)

![WhatsApp Image 2023-12-25 at 22 31 02_5efc7a13](https://github.com/mou-code/Smart-Retail-Checkout-System/assets/97397431/36e35bf6-fd4a-4047-950b-ef1659e24260)

