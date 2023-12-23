from sklearn import svm
import numpy as np
import cv2
import os
from sklearn.preprocessing import LabelEncoder
import pandas as pd

path_to_dataset = r'../dataset/train/pos_imgs/cropped'


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
    img_eq = cv2.GaussianBlur(img_eq, (5, 5), 0)

    # Normalize pixel values to the range [0, 1]
    img_eq = img_eq / 255.0

    return img_eq


def load_dataset_from_excel(excel_path):

    # Read data from Excel sheet
    df = pd.read_excel(excel_path)

    for i, row in df.iterrows():
        fn = row['Image_Name']
        label = str(row['Label'])

        path = os.path.join(path_to_dataset,label, fn)
        img = cv2.imread(path)

        # Preprocess the image
        img = preprocess_image(img)

        # Create the output directory if it doesn't exist
        output_class_directory = os.path.join(r'../dataset/train/pos_imgs/preproc', label)
        os.makedirs(output_class_directory, exist_ok=True)

        # Save the preprocessed image
        output_path = os.path.join(output_class_directory, fn)
        cv2.imwrite(output_path, (img * 255).astype(np.uint8))

excel_path = 'labels.xlsx'
load_dataset_from_excel(excel_path)