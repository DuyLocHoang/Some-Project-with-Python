import numpy as np
import time
import HandTrackingModule as htm
import os
import cv2
cap = cv2.VideoCapture(0)
wCam,hCam = 640,480
cap.set(3,wCam)
cap.set(4,hCam)

cTime = 0
pTime = 0

folderPath = 'fingerimages'
myList = os.listdir(folderPath)
# print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    # print(f'{folderPath}/{imPath}')
    overlayList.append(image)

detector = htm.HandTrackingModule(mdc = 0.75)
tipIds = [4,8,12,16,20]

while 1:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img,draw = False)
    # print(lmList)
    fingers = []
    if lmList :

        if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        for i in range(1,5):
            if lmList[tipIds[i]][2] < lmList[tipIds[i]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        # print(fingers)
    totalFingers = fingers.count(1)
    print(totalFingers)

    h,w,c = overlayList[totalFingers-1].shape
    img[0:h,0:w] = overlayList[totalFingers -1]
    cv2.rectangle(img,(20,255),(170,425),(0,255,0),cv2.FILLED)
    cv2.putText(img,str(totalFingers),(45,375),cv2.FONT_HERSHEY_PLAIN,10,(255,0,0),25)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,f'FPS: {int(fps)}',(500,50),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),1)
    cv2.imshow("Live",img)
    if cv2.waitKey(1) == ord('q'):
        break
