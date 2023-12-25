from sklearn import svm
import numpy as np
import cv2
import os
from sklearn.preprocessing import LabelEncoder
import pandas as pd

def preprocess_image(img):

    # Convert the image to the LAB color space
    lab_img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

    # Split the LAB image into L, A, and B channels
    l_channel, a_channel, b_channel = cv2.split(lab_img)

    # Apply histogram equalization to the L channel
    l_channel_eq = cv2.equalizeHist(l_channel)

    # Merge the equalized L channel with the original A and B channels
    lab_img_eq = cv2.merge([l_channel_eq, a_channel, b_channel])

    # Convert the LAB image back to BGR color space
    img_eq = cv2.cvtColor(lab_img_eq, cv2.COLOR_LAB2BGR)

    # Apply Gaussian blur for noise reduction
    # img_eq = cv2.GaussianBlur(img_eq, (3, 3), 0)
    bilateral_image = cv2.bilateralFilter(img_eq, d=20, sigmaColor=100, sigmaSpace=70)
    #20,100,70-> 4 false, acc 97.8%
    #50,100,70 -> 4 false acc 96.336%
    #50,100,50 -> 4 false acc 96.336%

    # Normalize pixel values to the range [0, 1]
    bilateral_image = bilateral_image / 255.0

    return bilateral_image

def read_proc_save(test_path):

            for img_name in os.listdir(test_path):
                print(img_name)
                img_path = os.path.join(test_path, img_name)

                img = cv2.imread(img_path)
                img= preprocess_image(img)

                output_class_directory = os.path.join('E:/ip_output/current_process/preprocessed_images/', str(img_name))
                cv2.imwrite(output_class_directory, (img * 255).astype(np.uint8))

test_dataset_path = 'E:/ip_output/current_process/cropped_images'
read_proc_save(test_dataset_path)