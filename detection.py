#####fatma
import cv2
import numpy as np
import matplotlib.pyplot as plt
# from skimage import io
# from skimage.util import img_as_ubyte
# from skimage.io import imsave

# Load the image
img = cv2.imread("test11.jpg", cv2.IMREAD_COLOR)
check1 = np.mean(img)
# Increase brightness by adding a constant value to all pixels
brighter_img = cv2.convertScaleAbs(img, alpha=1, beta= 75 -check1)
# Convert to grayscale
gray = cv2.cvtColor(brighter_img, cv2.COLOR_BGR2GRAY)


# Apply Gaussian blur to reduce noise
blur = cv2.GaussianBlur(gray,(5,5),0)

# Apply Canny edge detection
edges = cv2.Canny(blur, 90, 10)

# Use contour detection
dilation_kernel = np.ones((2, 2), np.uint8)
edges_dilated = cv2.dilate(edges, dilation_kernel, iterations=1)

# Closing operation to connect outer edges
closing_kernel = np.ones((2, 2), np.uint8)
edges_closed = cv2.morphologyEx(edges_dilated, cv2.MORPH_CLOSE, closing_kernel)
plt.imshow(cv2.cvtColor(edges_closed , cv2.COLOR_BGR2RGB))
plt.show()
# Find contours
contours, _ = cv2.findContours(edges_closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Draw rectangles around detected objects
# rectangle_positions = []
# for contour in contours:
#     # Ignore small contours (adjust the threshold as needed)
#     if cv2.contourArea(contour) > 500:
#         x, y, w, h = cv2.boundingRect(contour)
#         cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
#         rectangle_positions.append((x, y, x + w, y + h))
# Draw rectangles around detected objects without overlapping
rectangle_positions = []
for i, contour1 in enumerate(contours):
    # Ignore small contours (adjust the threshold as needed)
    if cv2.contourArea(contour1) >500:
        # print(cv2.contourArea(contour1))
        x1, y1, w1, h1 = cv2.boundingRect(contour1)
        is_inside = False
        for j, contour2 in enumerate(contours):
            if (i != j and cv2.contourArea(contour2) >500 ) :  # Avoid comparing the same rectangle
                x2, y2, w2, h2 = cv2.boundingRect(contour2)
                # Check if rectangle1 is inside rectangle2
                if (x1 >= x2 and y1 >= y2 and x1 + w1 <= x2 + w2 and y1 + h1 <= y2 + h2)  :
                    is_inside = True
                    break  # No need to check further
                if((abs(x1-x2) < 40) and x1-x2 <0 and ((abs((y2+h2)-(y1+h1)) < 20) or abs(y2-y1) < 20)) :
                    # print(x1,x2)
                    is_inside = True
                    break  # No need to check further
                if ((abs((x1+w1) - (x2+w2)) < 40) and x1 - x2 > 0 and ((abs((y2 + h2) - (y1 + h1)) < 20) or abs(y2 - y1) < 20)):
                    print(x1, x2)
                    is_inside = True
                    break  # No need to check further

        # Draw the rectangle only if it's not inside any larger rectangle
        if not is_inside:
            cv2.rectangle(img, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)
            rectangle_positions.append((x1, y1, x1 + w1, y1 + h1))


# for i, (minx, miny, maxx, maxy) in enumerate(rectangle_positions):
#     minx = int(minx)
#     miny = int(miny)
#     maxx = int(maxx)
#     maxy = int(maxy)
#     cropped_image = img[miny:maxy, minx:maxx]
#     cv2.imwrite(f"cropped_test/cropped_image_{i}.png", cropped_image)
# # Display the result
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.show()