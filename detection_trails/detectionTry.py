import numpy as np
import matplotlib.pyplot as plt
import skimage.io as io
import skimage
from skimage.measure import find_contours
from skimage.morphology import closing, square
from matplotlib.patches import Rectangle
import findContours


img = io.imread("objs.jpg", as_gray=True)
closed = closing(img < 0.9, square(3))

contours,_ = findContours.find_contours(closed)
rectangle_positions = []

for contour in contours:
    contour_array = np.array(contour)
    minr, minc, maxr, maxc = np.min(contour_array[:, 0]), np.min(contour_array[:, 1]), np.max(contour_array[:, 0]), np.max(contour_array[:, 1])
    rect = Rectangle((minc, minr), maxc - minc, maxr - minr, fill=False, edgecolor='red', linewidth=2)
    plt.gca().add_patch(rect)
    rectangle_positions.append((minc, minr, maxc, maxr))

print(rectangle_positions)
plt.imshow(img, cmap='gray')
plt.show()
