import mediapipe as mp
import numpy as np
import time
import PoseModule as pm
import cv2
import math
cap = cv2.VideoCapture(0)
cTime = 0
pTime = 0
bar = 0
detector = pm.PoseModule(detectionCon=0.75)
per = 0
count = 0

dir = 0
while 1:
    success,img = cap.read()
    img = cv2.resize(img,(1280,720))
    # 1. Find Pose estimation
    img = detector.findPose(img)
    # 2. Get landmarks
    lmList = detector.findPosition(img,draw = False)
    if lmList :
        # print(lmList)
    # 3. Tim goc giua 2 diem
    #Right-Arm
        angle = detector.findAngle(img,12,14,16)
        # print(angle)
    #Left Arm
        # angle = detector.findAngle(img, 11, 13, 15)
    # 4. Convert angle to percent
        per = np.interp(angle,[190,300],[0,100])
        bar = np.interp(angle,[190,300],[650,100])
        print(per)

        # Count
        if per == 100 :
            if dir == 0 :
                count += 0.5
                print('aaaa')
                dir = 1
        if per == 0 :
            if dir == 1 :
                count += 0.5
                dir = 0
        print(count)
        # 5. Display
        #Display percent
        cv2.putText(img,f'{int(per)}%',(1100, 75),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
        #Display bar curls
        cv2.rectangle(img,(1100, 100), (1175, 650),(255,0,0),3)
        cv2.rectangle(img,(1100,int(bar)),(1175,650),(255,0,0),cv2.FILLED)
        # Display count
        cv2.rectangle(img,(0, 450), (250, 720),(255,0,0),cv2.FILLED)
        cv2.putText(img,str(int(count)),(45, 670),cv2.FONT_HERSHEY_PLAIN,20,(255,255,255),20)
    #fps
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,f'FPS{int(fps)}',(20,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)

    cv2.imshow("Video",img)
    if cv2.waitKey(1) == ord('q') :
        break
