import cv2
import numpy as np
import os
from sklearn.svm import SVC
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import joblib

# Step 1: Collect Data
base_path = 'dataset/train/'
products = ['product1', 'product2', 'product3', 'product4', 'product5']


# Step 2: Extract SIFT Features
def extract_sift_features(image):
    sift = cv2.SIFT_create()
    keypoints, descriptors = sift.detectAndCompute(image, None)
    return descriptors


def build_codebook(base_path, products, sift, k):
    all_descriptors = []
    for product_name in products:
        product_folder = os.path.join(base_path, product_name)

        # Load all images in the product folder
        for filename in os.listdir(product_folder):
            img_path = os.path.join(product_folder, filename)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            descriptors = extract_sift_features(img)
            if descriptors is not None:
                all_descriptors.extend(descriptors)

    if len(all_descriptors) == 0:
        return None

    # Use k-means clustering to create the codebook
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(all_descriptors)

    return kmeans


def quantize_features(descriptors, codebook):
    if descriptors is None or codebook is None:
        return None

    # Assign descriptors to the nearest cluster center (visual word)
    words = codebook.predict(descriptors)

    # Create a histogram of visual words
    histogram, _ = np.histogram(words, bins=range(len(codebook.cluster_centers_) + 1))

    return histogram


def load_images_and_labels():
    features = []
    labels = []

    for product_id, product_name in enumerate(products, start=1):
        product_folder = os.path.join(base_path, product_name)

        for filename in os.listdir(product_folder):
            img_path = os.path.join(product_folder, filename)
            if os.path.isfile(img_path):
                img = cv2.imread(img_path)
                sift_features = extract_sift_features(img)

                features.append((img_path, sift_features))  # Save both the path and features
                labels.append(product_id)

    return features, np.array(labels)


# Load SIFT features and corresponding labels
all_features, all_labels = load_images_and_labels()

# Extract only the SIFT features for codebook creation
sift_features_for_codebook = [features[1] for features in all_features]

# Build the codebook using k-means clustering
codebook_size = 50  # You can adjust this parameter based on your dataset
codebook = build_codebook(base_path, products, cv2.SIFT_create(), codebook_size)


if codebook is not None:
    # Quantize features using the codebook
    quantized_features = [quantize_features(features[1], codebook) for features in all_features]

    # Convert features to a NumPy array
    features_array = np.array(quantized_features, dtype=np.float32)
    labels_array = np.array(all_labels)

    # Shuffle the data
    indices = np.arange(features_array.shape[0])
    np.random.shuffle(indices)

    shuffled_features = features_array[indices]
    shuffled_labels = labels_array[indices]

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        shuffled_features, shuffled_labels, test_size=0.1, random_state=42
    )

    # Step 3: Train the Classifier
    # Train an SVM classifier
    classifier = SVC()
    classifier.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = classifier.predict(X_test)

    # Evaluate the classifier
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy}")

    # Save the trained model
    joblib.dump(classifier, 'product_recognition_model.pkl')
else:
    print("Codebook is empty. No descriptors found in the dataset.")
