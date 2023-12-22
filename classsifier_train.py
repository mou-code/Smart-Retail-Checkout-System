import cv2
import numpy as np
import os

# Step 1: Collect Data
positive_samples_path = 'dataset/train/pos_imgs'
negative_samples_path = 'dataset/train/neg_imgs'

# Step 2: Label Data
# Positive samples are assumed to be annotated with bounding boxes
# You may use a tool like LabelImg for manual annotation

# Step 3: Extract HOG Features
def extract_hog_features(image):
    # Create a HOGDescriptor object
    hog = cv2.HOGDescriptor()
    # Compute HOG features
    features = hog.compute(image)
    # Flatten the features
    features = features.flatten()
    return features

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img_path = os.path.join(folder, filename)
        if os.path.isfile(img_path):
            img = cv2.imread(img_path)
            if img is not None:
                images.append(img)
    return images

# Positive samples
positive_images = load_images_from_folder(positive_samples_path)
positive_features = [extract_hog_features(img) for img in positive_images]
positive_labels = np.ones(len(positive_features))

# Negative samples
negative_images = load_images_from_folder(negative_samples_path)
negative_features = [extract_hog_features(img) for img in negative_images]
negative_labels = np.zeros(len(negative_features))

print(len(positive_features))
print(len(negative_features))

# Combine positive and negative samples
all_features = np.concatenate((positive_features, negative_features), axis=0)
all_labels = np.concatenate((positive_labels, negative_labels))

# Shuffle the data
indices = np.arange(all_features.shape[0])
np.random.shuffle(indices)

# Convert features to float32
shuffled_features = all_features[indices].astype(np.float32)
shuffled_labels = all_labels[indices]

# Split the data into training and testing sets
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    shuffled_features, shuffled_labels, test_size=0.2, random_state=42
)

# Step 4: Train the Classifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# Train an SVM classifier
classifier = SVC(kernel='linear')
classifier.fit(X_train, y_train)

# Make predictions on the test set
y_pred = classifier.predict(X_test)

# Evaluate the classifier
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")

# Save the trained model
import joblib
joblib.dump(classifier, 'groceries_detector_model.pkl')
