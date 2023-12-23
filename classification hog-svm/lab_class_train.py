
from sklearn import svm
import numpy as np
import cv2
import os
import random
from sklearn.preprocessing import LabelEncoder
import pandas as pd
from sklearn.model_selection import train_test_split

path_to_dataset = r'../dataset/train/pos_imgs/preproc'
target_img_size = (32, 32) # fix image size because classification algorithms THAT WE WILL USE HERE expect that

# We are going to fix the random seed to make our experiments reproducible 
# since some algorithms use pseudorandom generators
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



def load_dataset_from_excel(excel_path):
    features = []
    labels = []

    # Read data from Excel sheet
    df = pd.read_excel(excel_path)

    for i, row in df.iterrows():
        fn = row['Image_Name']
        label = str(row['Label'])

        path = os.path.join(path_to_dataset,label, fn)
        img = cv2.imread(path)

        
        features.append(extract_hog_features(img))
        # Add other feature extraction methods if needed

        labels.append(label)

        # Show an update every 1,000 images
        if i > 0 and i % 1000 == 0:
            print("[INFO] processed {}/{}".format(i, len(df)))

    print(len(features), len(labels))
    return features, labels
      

def run_experiment(excel_path):
    
    # Load dataset with extracted features
    print('Loading dataset. This will take time ...')
    features, labels = load_dataset_from_excel(excel_path)
    print('Finished loading dataset.')
    
    # Since we don't want to know the performance of our classifier on images it has seen before
    # we are going to withhold some images that we will test the classifier on after training 
    train_features, test_features, train_labels, test_labels = train_test_split(
        features, labels, test_size=0.2, random_state=random_seed)
    
    print('############## Training ##############')
    # Train the model only on the training features
    model=svm.SVC()
    model.fit(train_features, train_labels)
    
    # Test the model on images it hasn't seen before
    accuracy = model.score(test_features, test_labels)
    
    print('svm accuracy:', accuracy*100, '%')

    import joblib
    joblib.dump(model, 'groceries_classifier_model.pkl')




excel_path = 'labels.xlsx'
run_experiment(excel_path)

