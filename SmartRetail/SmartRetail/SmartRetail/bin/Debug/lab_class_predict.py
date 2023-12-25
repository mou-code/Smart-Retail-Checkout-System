import joblib
import cv2
import os
import numpy as np
from sklearn import svm

target_img_size = (32, 32)

def evaluate_model(model, test_path):
    predicted_labels = []

    for img_name in os.listdir(test_path):
        img_path = os.path.join(test_path, img_name)

        img = cv2.imread(img_path)
        features = extract_hog_features(img)
        predicted_label = model.predict([features])[0]
        predicted_labels.append(predicted_label)

    return predicted_labels

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

# Load the trained model
model = joblib.load('groceries_classifier_model.pkl')

# Assuming your test images are in a folder named 'test_dataset'

test_dataset_path = r'E:/ip_output/current_process/preprocessed_images'

# Evaluate the model and return the predicted labels
predicted_labels = evaluate_model(model, test_dataset_path)
# Print predicted labels separated by commas
print(','.join(map(str, predicted_labels)))
