
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

## System Overview

#### 1. Model Training
    1.  Data acquisition and sensing: Collecting Images of all products of a certain store using a camera
    2.  Internal Image Processing: Pre-processing Stage - Feature Extraction Stage - Classification Stage
    3.  Model Parameter Storage: The phase in which the trained classifier's essential parameters, which include the learned decision boundaries and rules, are securely stored in a database or a designated storage system.
#### 2. Real-time Inference
    1.  Image Acquisition: The process of using cameras to capture images of items in real-time as they are placed at the checkout counter.
    2.  Internal Image Processing: Pre-processing Stage - Feature Extraction Stage - Classification Stage
    3.  Database Query: The phase in which the smart retail checkout system accesses a database to retrieve relevant product information based on the classification
    4.  Post-processing: Evaluation of confidence in decisions using thresholding algorithm

#### Internal Image Processing

Pre-processing Stage
Scaling and transforming images into grayscale
Noise removal: using various noise reduction techniques like Gaussian or median filtering.
Isolation of patterns of interest from the background.         (using Edge-Based Segmentation or Region-Based Segmentation)

Feature Extraction Stage: 
SIFT (Scale-Invariant Feature Transform) is a good choice as it’s robust to rotation and scaling.
HOG (Histogram of Oriented Gradients) is also useful for object detection.
Our primary preference will be SIFT

Classification Stage: 
SVM (Support Vector Machines) is effective for separating data into different categories.
KNN (k-Nearest Neighbours) is also a good option for object detection
Our primary preference will be SVM

### Expected inputs & outputs
Expected Inputs:
Image Captured by Top-View Camera: The primary input is the image
captured by the top-view camera.
Product Models: We will provide a set of product models or reference
images. These are images of individual products that the system should
recognize. Each product model should be labeled or associated with a
specific category (e.g., "beverages," "snacks," "canned goods," etc.).

Expected Outputs:
Displaying a real-time breakdown of recognized products on a screen.
Digital or printed receipt is provided, summarizing the purchased items
and payment details, culminating in a seamless and accurate shopping
experience.


## References

 - Umer, S., Mohanta, P.P., Rout, R.K. et al. Machine learning method for cosmetic product recognition: a visual searching approach. Multimed Tools Appl 80, 34997–35023 (2021). https://doi.org/10.1007/s11042-020-09079-y
## Authors

- [@MostafaBinHani](https://github.com/MostafaBinHani)
- [@fatmaebrahim](https://github.com/fatmaebrahim)
- [@MohammadAlomar8](https://github.com/MohammadAlomar8)
- [@mou-code](mou-code)
- [@RawanMostafa08](https://github.com/RawanMostafa08)



## Installation

todo
    
## Running Tests

todo
## Usage/Examples

todo

## Screenshots

![App Screenshot](https://via.placeholder.com/468x300?text=App+Screenshot+Here)

