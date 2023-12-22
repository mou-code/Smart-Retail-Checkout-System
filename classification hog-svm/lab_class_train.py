
from sklearn import svm
import numpy as np
import cv2
import os
import random
from sklearn.preprocessing import LabelEncoder
import pandas as pd
from sklearn.model_selection import train_test_split

path_to_dataset = r'../dataset/train/pos_imgs/cropped'
target_img_size = (32, 32) # fix image size because classification algorithms THAT WE WILL USE HERE expect that

# We are going to fix the random seed to make our experiments reproducible 
# since some algorithms use pseudorandom generators
random_seed = 42  
random.seed(random_seed)
np.random.seed(random_seed)


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

# if __name__ == "__main__":
#     # Adjust the paths and directories
#     contour_file_path = r'../dataset/train/pos_imgs/zaza.txt'
#     input_image_folder_path = r'../dataset/train/pos_imgs/zaza'
#     output_folder_path = r'../dataset/train/pos_imgs/cropped/zaza'

#     # Create the output folder if it doesn't exist
#     os.makedirs(output_folder_path, exist_ok=True)

#     # Call the function to crop and save images
#     crop_and_save_images(contour_file_path, input_image_folder_path, output_folder_path)


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



def load_dataset_from_excel(excel_path, feature_set='hog'):
    features = []
    labels = []

    # Read data from Excel sheet
    df = pd.read_excel(excel_path)

    for i, row in df.iterrows():
        fn = row['Image_Name']
        label = str(row['Label'])

        path = os.path.join(path_to_dataset,label, fn)
        img = cv2.imread(path)

        if feature_set == 'hog':
            features.append(extract_hog_features(img))
        # Add other feature extraction methods if needed

        labels.append(label)

        # Show an update every 1,000 images
        if i > 0 and i % 1000 == 0:
            print("[INFO] processed {}/{}".format(i, len(df)))

    print(len(features), len(labels))
    return features, labels
      

def run_experiment(feature_set, excel_path):
    
    # Load dataset with extracted features
    print('Loading dataset. This will take time ...')
    features, labels = load_dataset_from_excel(excel_path, feature_set)
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




# #using cv2
# def run_experiment(feature_set, excel_path):
    
#     # Load dataset with extracted features
#     print('Loading dataset. This will take time ...')
#     features, labels = load_dataset_from_excel(excel_path, feature_set)
#     print('Finished loading dataset.')
    
#     # Since we don't want to know the performance of our classifier on images it has seen before
#     # we are going to withhold some images that we will test the classifier on after training 
#     train_features, test_features, train_labels, test_labels = train_test_split(
#         features, labels, test_size=0.2, random_state=random_seed)
    
#     # Create SVM model
#     svm = cv2.ml.SVM_create()
#     svm.setKernel(cv2.ml.SVM_LINEAR)
#     svm.setType(cv2.ml.SVM_C_SVC)
#     svm.setC(1.0)
#     label_encoder = LabelEncoder()
#     train_labels = label_encoder.fit_transform(train_labels)
#     # Convert training data to numpy arrays
#     train_features = np.array(train_features, dtype=np.float32)
#     train_labels = np.array(train_labels, dtype=np.int32)
#     train_labels = train_labels.reshape(-1, 1)

#     # Create TrainData object
#     train_data = cv2.ml.TrainData_create(samples=train_features,
#                                          layout=cv2.ml.ROW_SAMPLE,
#                                          responses=train_labels)

#     # Train the SVM model
#     svm.train(train_data)

#     # Save the trained model
#     svm.save("svm_model.xml")

#     # Test the model on images it hasn't seen before
#     test_features = np.array(test_features, dtype=np.float32)

#     _, predictions = svm.predict(test_features)

#     # Convert predicted labels back to original class labels
#     predicted_labels = label_encoder.inverse_transform(predictions.astype(int).flatten())

#     # Calculate accuracy
#     accuracy = np.mean(predicted_labels == test_labels)
#     print('SVM accuracy:', accuracy * 100, '%')




excel_path = 'labels.xlsx'
run_experiment('hog', excel_path)

