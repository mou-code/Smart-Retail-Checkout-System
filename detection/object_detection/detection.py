import cv2
import imutils
from time import time

cascPath = 'data/model/cascade.xml'
imagePath = 'test.jpg'

cameraNo = 2
frameWidth = 640
frameHeight = 480
color = (255,0,255)

cap = cv2.VideoCapture(cameraNo)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

def draw_rectangles( haystack_img, rectangles):
        # these colors are actually BGR
        line_color = (0, 255, 0)
        line_type = cv2.LINE_4

        for (x, y, w, h) in rectangles:
            # determine the box positions
            top_left = (x, y)
            bottom_right = (x + w, y + h)
            # draw the box
            cv2.rectangle(haystack_img, top_left, bottom_right, line_color, lineType=line_type)

        return haystack_img

def empty(a):
    pass

cv2.namedWindow("Result")
cv2.resizeWindow("Result", frameWidth, frameHeight+100)
cv2.createTrackbar("Scale","Result", 400,1000,empty)
cv2.createTrackbar("Neig","Result", 8,50,empty)
cv2.createTrackbar("Min Area","Result", 0,100000,empty)

# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)
loop_time = time()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break

    # Resize the frame so it fits in the screen
    frame = imutils.resize(frame, height=512, width=512)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Get trackbar values
    scale_val = cv2.getTrackbarPos("Scale", "Result") / 100.0
    neig_val = cv2.getTrackbarPos("Neig", "Result")
    min_area_val = cv2.getTrackbarPos("Min Area", "Result")

    # Detect objects in the frame
    objects = faceCascade.detectMultiScale(
        gray,
        scaleFactor=scale_val,
        minNeighbors=neig_val,
        minSize=(24, 24),
        flags=0
    )

    if format(len(objects)) == 1:
        print("Found {0} object!".format(len(objects)))
    else:
        print("Found {0} objects!".format(len(objects)))

    detection_image = draw_rectangles(frame, objects)

    cv2.imshow("Result", frame)

    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()
    key = cv2.waitKey(1)
    if key == ord('q'):
        cv2.destroyAllWindows()
        break
    elif key == ord('f'):
        cv2.imwrite('positive/{}.jpg'.format(loop_time), frame)
    elif key == ord('d'):
        cv2.imwrite('negative/{}.jpg'.format(loop_time), frame)


cap.release()
cv2.destroyAllWindows()
