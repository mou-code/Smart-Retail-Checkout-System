import cv2
import os
import time

myPath = 'image_collection/images'
CameraNo = 2
cameraBrightness = 190
moduleVal = 10
minBlur = 50
grayImage = False
saveData = True
showImage = True
imgWidth = 256
imgHeight = 256

global countFolder
cap = cv2.VideoCapture(CameraNo)
cap.set(3,640)
cap.set(4,480)
cap.set(10,cameraBrightness)

count = 0
countSave = 0

def saveDataFunc():
    global countFolder
    countFolder = 0
    while os.path.exists(myPath+ str(countFolder)):
        countFolder = countFolder + 1
    os.makedirs(myPath + str(countFolder))

if saveData: saveDataFunc()

while True:

    success, img = cap.read()
    img = cv2.resize(img,(imgWidth,imgHeight))
    if grayImage: img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    if saveData:
        blur = cv2.Laplacian(img,cv2.CV_64F).var()
        if count % moduleVal == 0 and blur > minBlur:
            nowTime = time.time()
            cv2.imwrite(myPath + str(countFolder) + '/' + 
                        str(countSave) + "_" + str(int(blur)) + "_"+ str(nowTime) + ".jpg", img)
            countSave+=1
        count += 1

    if showImage:
        cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWidnwos()            