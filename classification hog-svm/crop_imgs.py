from sklearn import svm
import numpy as np
import cv2
import os
import random
from sklearn.preprocessing import LabelEncoder
import pandas as pd
from sklearn.model_selection import train_test_split


def crop_and_save_images(contour_file, input_image_folder, output_folder):
    # Read contours from the text file
    with open(contour_file, 'r') as file:
        lines = file.readlines()

    for line in lines:
        parts = line.split()
        image_name = parts[0]
        num_objects = int(parts[1])
        x, y, w, h = map(int, parts[1:5])

        # Read the original image
        image_path = os.path.join(input_image_folder, image_name)
        original_image = cv2.imread(image_path)



        if original_image is None:
            print(f"Error reading image: {image_path}")
            continue

        for i in range(num_objects):
            x, y, w, h = map(int, parts[2 + i * 4: 6 + i * 4])
            cropped_image = original_image[y:y+h, x:x+w]
            if cropped_image.size == 0:
                print(f"Error cropping image: {image_path}")
                continue
        # Crop the region defined by the contour
        # cropped_image = original_image[y:h, x:w]


        # Save the cropped image to the output folder
        output_path = os.path.join(output_folder, image_name)
        cv2.imwrite(output_path, cropped_image)
        print(f"Saved: {output_path}")

if __name__ == "__main__":
    # Adjust the paths and directories
    contour_file_path = r'../dataset/HD/zaza/HDzaza.txt'
    input_image_folder_path = r'../dataset/HD/zaza'
    output_folder_path = r'../dataset/train/pos_imgs/croppedHD/zaza'

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder_path, exist_ok=True)

    # Call the function to crop and save images
    crop_and_save_images(contour_file_path, input_image_folder_path, output_folder_path)