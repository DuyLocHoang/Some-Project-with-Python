import cv2
import mediapipe as mp
import time
cap = cv2.VideoCapture('data/head-pose-face-detection-female.mp4')
cTime = 0
pTime = 0

mpDraw = mp.solutions.drawing_utils
drawSpec = mpDraw.DrawingSpec(thickness=1,circle_radius=1)
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh()

while 1:
    success,img = cap.read()
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = faceMesh.process(imgRGB)
    if results.multi_face_landmarks :
        for faceLms in results.multi_face_landmarks:
            mpDraw.draw_landmarks(img,faceLms,mpFaceMesh.FACE_CONNECTIONS,drawSpec,drawSpec)
            for id,lm in enumerate(faceLms.landmark):
                # print(id,lm)
                h,w,c = img.shape
                cx,cy = int(lm.x*w),int(lm.y*h)
                print(id,cx,cy)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,str(int(fps)),(50,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
    cv2.imshow("FaceMesh",img)
    if cv2.waitKey(1) == ord('q'):
        break
