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


test_img_path = r'../dataset/test/100_443_1702949768.095945.jpg'
img = cv2.imread(test_img_path)
features = extract_hog_features(img)  # be careful of the choice of feature set

print(model.predict([features]))



#svm using cv2
# # Reshape the features array to be a single-row 2D array
# features = np.array(features, dtype=np.float32)
# features = features.reshape(1, -1)

# # Use the predict method
# response = model.predict(features)

# # The result is a tuple where the first element contains the predicted label
# predicted_label = response[1][0][0]
# print(predicted_label)
