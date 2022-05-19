import cv2
import mediapipe as mp # this famework use rgb
import time
import math
class PoseModule():
    def __init__(self,mode = False,UpBody = False,smooth = True,detectionCon = 0.5,trackingCon = 0.5):
        self.static_image_mode = False
        self.upper_body_only = False
        self.smooth_landmarks = True
        self.min_detection_confidence = 0.5
        self.min_tracking_confidence = 0.5
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose()
        self.mpDraw = mp.solutions.drawing_utils
    def findPose(self,img,draw = True):
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks :
            self.mpDraw.draw_landmarks(img,self.results.pose_landmarks,self.mpPose.POSE_CONNECTIONS)
        return img
    def findPosition(self,img,draw = True):
        self.lmList = []
        if self.results.pose_landmarks:
            for id,lm in enumerate(self.results.pose_landmarks.landmark):
                h,w,c = img.shape
                cx,cy = int(lm.x*w),int(lm.y*h)
                self.lmList.append([id,cx,cy])
                if draw :
                    cv2.circle(img,(cx,cy),3,(255,0,255),cv2.FILLED)
        return self.lmList
    def findAngle(self,img,pt1,pt2,pt3,draw = True):

        #Get the landmark
        x1, y1 = self.lmList[pt1][1:]
        x2, y2 = self.lmList[pt2][1:]
        x3, y3 = self.lmList[pt3][1:]

        #Calculate the Angle
        angle = math.degrees(math.atan2(y3-y2,x3-x2)-math.atan2(y1-y2,x1-x2))
        if angle < 0 :
            angle = 360 + angle

        # Draw
        cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
        cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
        cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
        cv2.line(img, (x2, y2), (x3, y3), (255, 255, 255), 3)
        cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)

        return angle

def main():
    cap = cv2.VideoCapture('videos/a.mp4')
    cTime = 0
    pTime = 0
    detector = PoseModule()
    while True:
        success, img = cap.read()
        img = detector.findPose(img)
        lmList = detector.findPosition(img)
        if lmList :
            print(lmList[1])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 5)
        cv2.imshow("Video", img)
        if cv2.waitKey(5) == ord('q'):
            break
if __name__ == "__main__":
    main()