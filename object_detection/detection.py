import cv2
import imutils

cascPath = 'path/to/your/cascade.xml'

cameraNo = 2
objectName = "Tahina"
frameWidth = 640
frameHeight = 480
color = (255,0,255)

cap = cv2.VideoCapture(cameraNo)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

def empty(a):
    pass

cv2.namedWindow("Result")
cv2.resizeWindow("Result", frameWidth, frameHeight+100)
cv2.createTrackbar("Scale","Result", 400,1000,empty)
cv2.createTrackbar("Neig","Result", 8,50,empty)
cv2.createTrackbar("Min Area","Result", 0,100000,empty)

# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break

    # Resize the frame so it fits in the screen
    frame = imutils.resize(frame, height=500)

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
        minSize=(30, 30),
        flags=0
    )

    if format(len(objects)) == 1:
        print("Found {0} object!".format(len(objects)))
    else:
        print("Found {0} objects!".format(len(objects)))

    # Draw rectangles around the objects
    for (x, y, w, h) in objects:
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

    cv2.imshow("Result", frame)

    # Break the loop when the 'esc' key is pressed
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()