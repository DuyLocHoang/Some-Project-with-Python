import time
import cv2
import mediapipe
import os
import HandTrackingModule as htm
import numpy as np
#################
brushThickness = 25
eraserThickness = 100
#################

folderPath = 'Header-Files'
myList = os.listdir(folderPath)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

header = overlayList[0]

cap = cv2.VideoCapture(0)
wCam,hCam = 1280,720
cap.set(3,wCam)
cap.set(4,hCam)
pTime = 0
cTime = 0

detector = htm.HandTrackingModule(mdc = 0.6)
drawColor = (255, 0, 255)
xp,yp = 0,0
imgCanvas = np.zeros((720,1280,3),np.uint8)
while True:
    success,img = cap.read()
    img = cv2.flip(img,1)
    #1. Find Hand
    img = detector.findHands(img)
    #2. Find landmark
    lmList = detector.findPosition(img,draw = False)
    # print(lmList)
    #3. Check fingerup
    if lmList :
        #Get landmark
        x1,y1 = lmList[8][1:]
        x2,y2 = lmList[12][1:]

        fingers = detector.fingerUp()
        print(fingers)

    #4.  If 2 finger => model = selection
        if fingers[1] and fingers[2] :
            xp, yp = 0, 0
            print("Select mode")
            if y1 < 125 :
                if 250< x1 <450 :
                    drawColor = (255,0,255)
                    header = overlayList[0]
                elif 550 < x1 < 750 :
                    drawColor = (255,0,0)
                    header = overlayList[1]
                elif 800 < x1 < 950 :
                    drawColor = (0,255,0)
                    header = overlayList[2]
                elif 1050 < x1 < 1200 :
                    drawColor = (0,0,0)
                    header = overlayList[3]
            cv2.rectangle(img,(x1,y1-25),(x2,y2+25),drawColor,cv2.FILLED)
    #5.IF 1 finger => mode = Paint
        if fingers[1] and fingers[2] == False :
            print("Drawing mode")
            cv2.circle(img,(x1,y1),15,drawColor,cv2.FILLED)
            if xp == 0 and yp == 0 :
                xp,yp = x1,y1
            if drawColor == (0,0,0):
                cv2.line(img,(xp,yp),(x1,y1),drawColor,15,eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, 15, eraserThickness)
            else:
                cv2.line(img,(xp,yp),(x1,y1),drawColor,15,brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, 15, brushThickness)

            xp,yp =x1,y1

    imgGray = cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)
    _,imgInv = cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img2 = cv2.bitwise_and(img,imgInv)
    img = cv2.bitwise_or(img2,imgCanvas)




    #6. Setting header file
    img[0:125,0:1280] = header
    #fps
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    # print(fps)
    #Show image
    cv2.imshow("Screen",img2)
    cv2.imshow("draw", imgInv)
    if cv2.waitKey(1) == ord('q'):
        break


