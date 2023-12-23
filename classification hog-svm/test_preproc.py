from sklearn import svm
import numpy as np
import cv2
import os
from sklearn.preprocessing import LabelEncoder
import pandas as pd

def preprocess_image(img):
    # Resize the image to a specific size (e.g., 64x64 pixels)

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
    img_eq = cv2.GaussianBlur(img_eq, (3, 3), 0)

    # Normalize pixel values to the range [0, 1]
    img_eq = img_eq / 255.0

    return img_eq

def read_proc_save(test_path):

    for class_folder in os.listdir(test_path):
        class_folder_path = os.path.join(test_path, class_folder)

        if os.path.isdir(class_folder_path):
            for img_name in os.listdir(class_folder_path):
                img_path = os.path.join(class_folder_path, img_name)

                img = cv2.imread(img_path)
                img= preprocess_image(img)

                output_class_directory = os.path.join(r'../dataset/test/preproc', class_folder)
                os.makedirs(output_class_directory, exist_ok=True)

                # Save the preprocessed image
                output_path = os.path.join(output_class_directory, img_name)
                cv2.imwrite(output_path, (img * 255).astype(np.uint8))

test_dataset_path = r'../dataset/test'
read_proc_save(test_dataset_path)