import joblib

from sklearn import svm
import numpy as np
import cv2
import os
import random


target_img_size = (32, 32) # fix image size because classification algorithms THAT WE WILL USE HERE expect that

random_seed = 42  
random.seed(random_seed)
np.random.seed(random_seed)


import os

def evaluate_model(model, test_path):
    correct_predictions = 0
    total_images = 0

    for class_folder in os.listdir(test_path):
        class_folder_path = os.path.join(test_path, class_folder)

        if os.path.isdir(class_folder_path):
            for img_name in os.listdir(class_folder_path):
                img_path = os.path.join(class_folder_path, img_name)

                img = cv2.imread(img_path)
                features = extract_hog_features(img)
                predicted_label = model.predict([features])[0]
                print("expected: ",str(class_folder), ",,,predicted:" ,str(predicted_label) )
                

                if str(predicted_label) == str(class_folder):
                    correct_predictions += 1

                total_images += 1


    accuracy = correct_predictions / total_images
    print(f"Accuracy: {accuracy * 100:.2f}%")
    print("total test images: " ,total_images , " correct: ",correct_predictions , " false: ",total_images-correct_predictions)


def extract_hog_features(img):

    img = cv2.resize(img, target_img_size)
    win_size = (32, 32)
    cell_size = (4, 4)
    block_size_in_cells = (2, 2)
    
    block_size = (block_size_in_cells[1] * cell_size[1], block_size_in_cells[0] * cell_size[0])
    block_stride = (cell_size[1], cell_size[0])
    nbins = 12  # Number of orientation bins
    hog = cv2.HOGDescriptor(win_size, block_size, block_stride, cell_size, nbins)
    h = hog.compute(img)
    h = h.flatten()
    return h.flatten()

model = joblib.load('groceries_classifier_model.pkl')
# model = cv2.ml.SVM_load("svm_model.xml")


# Assuming your test images are in a folder named 'test_dataset'
test_dataset_path = r'../dataset/test'
evaluate_model(model, test_dataset_path)




