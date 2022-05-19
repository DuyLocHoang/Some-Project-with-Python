import cv2
import HandTrackingModule as htm
import time
import autopy
import numpy as np
#################
wCam,hCam = 640,480
cTime = 0
pTime = 0
frameR = 100
wScreen,hScreen = autopy.screen.size()
clocX,clocY = 0,0
plocX,plocY = 0,0
smoothing = 7
#################

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

detector = htm.HandTrackingModule(mdc = 0.7)

while 1 :
    success,img =cap.read()
    img = detector.findHands(img)
    #find landmarks
    lmList,bbox = detector.findPosition(img,draw = False)
    if lmList:
        # print(lmList)
        x1,y1 = lmList[8][1:]
        x2,y2 = lmList[12][1:]
        # Ktra fingerUp
        fingers =detector.fingerUp()
        # print(fingers)
        cv2.rectangle(img,(frameR,frameR),(wCam-frameR,hCam-frameR),(0,255,0),3)

        if fingers[1] == 1 and fingers[2] == 0 :
            x3 = np.interp(x1,(frameR,wCam-frameR),(0,wScreen))
            y3 = np.interp(y1,(frameR,hCam-frameR),(0,hScreen))
            clocX = x3 + (x3 - plocX)/smoothing
            clocY = y3 + (y3 - plocY)/smoothing
            autopy.mouse.move(wScreen-clocX,clocY)
            plocX,plocY = clocX,clocY

        if fingers[1] == 1 and fingers[2] == 1 :
            lenght,img,lineInfo = detector.findDistance(img,8,12)
            if lenght < 40 :
                cv2.circle(img,(lineInfo[4],lineInfo[5]),15,(0,255,0),cv2.FILLED)
                autopy.mouse.click()

    #fps
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,f'FPS:{int(fps)}',(20,50),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),3)
    cv2.imshow("Videos",img)
    if cv2.waitKey(1) == ord('q'):
        break
