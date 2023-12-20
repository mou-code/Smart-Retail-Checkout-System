import detection
import cv2
import matplotlib.pyplot as plt

# rectangle_positions, img = detection_algorithms.detect()
img = cv2.imread("inputEX 2.jpg", cv2.IMREAD_COLOR)  # to be edited

for i, (x1, y1, x2, y2) in enumerate(rectangle_positions):
    # Crop the region of interest (ROI)
    roi = img[y1:y2, x1:x2]

    # Perform SIFT on the cropped region
    sift = cv2.SIFT_create()
    keypoints, descriptors = sift.detectAndCompute(cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY), None)

    # Optionally, you can visualize the keypoints on the cropped region
    roi_with_keypoints = cv2.drawKeypoints(roi, keypoints, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # Display the original image with the keypoints on the cropped region
    plt.subplot(3, 5, i + 1)  # Adjust the subplot parameters based on the number of detected objects
    plt.imshow(cv2.cvtColor(roi_with_keypoints, cv2.COLOR_BGR2RGB))
    # plt.title(f'Object {i + 1}')

# plt.show()
