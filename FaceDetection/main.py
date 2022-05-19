import cv2
import time
import mediapipe as mp

cap = cv2.VideoCapture('data/head-pose-face-detection-female.mp4')
cTime = 0
pTime = 0

mpFace = mp.solutions.face_detection
face = mpFace.FaceDetection(min_detection_confidence=0.5)
mpDraw = mp.solutions.drawing_utils
while 1 :
    success,img = cap.read()
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = face.process(imgRGB)


    if results.detections :
        for id,detection in enumerate(results.detections):
            print(id,detection)
            print(detection.score)
            print(detection.location_data.relative_bounding_box)
            h,w,c = img.shape
            bboxC = detection.location_data.relative_bounding_box
            bbox = int(bboxC.xmin * w),int(bboxC.ymin * h),\
                    int(bboxC.width * w),int(bboxC.height * h)
            cv2.rectangle(img,bbox,(255,0,255),3)
            cv2.putText(img,f'{int(detection.score[0]*100)}%',(bbox[0],bbox[1]-20),cv2.FONT_HERSHEY_PLAIN,2,(255,0,255),2)


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,str(int(fps)),(50,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
    cv2.imshow("Face",img)
    if cv2.waitKey(10) == ord('q'):
        break
