import cv2
import time
import mediapipe as mp
import math





class HandTrackingModule():
    def __init__(self,mode = False,Maxhands = 2,mdc = 0.5, mtc = 0.5):
        self.static_image_mode = mode
        self.max_num_hands = Maxhands
        self.min_detection_confidence = mdc
        self.min_tracking_confidence = mtc
        self.mpHands = mp.solutions.hands
        self.mpDraw = mp.solutions.drawing_utils
        self.hands = self.mpHands.Hands(self.static_image_mode,self.max_num_hands,
                                        self.min_detection_confidence,self.min_tracking_confidence) # use RGB
        self.tipIds = [4, 8, 12, 16, 20]
    def findHands(self,img,draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self,img,handNo = 0,draw = True):
        self.lmList = []
        xList = []
        yList = []
        bbox = []
        if self.results.multi_hand_landmarks :
            myhand = self.results.multi_hand_landmarks[handNo]
            for id,lm in enumerate(myhand.landmark):
                # print(id,lm)
                h,w,c = img.shape
                cx,cy = int(w*lm.x),int(h*lm.y)
                xList.append(cx)
                yList.append(cy)
                # print(id,cx,cy)
                self.lmList.append([id,cx,cy])
                if draw :
                    cv2.circle(img,(cx,cy),5,(255,0,255),cv2.FILLED)
            xmin,xmax = min(xList),max(xList)
            ymin,ymax = min(yList),max(yList)
            bbox = xmin,ymin,xmax,ymax
            if draw :
                cv2.rectangle(img,(xmin-20,ymin-20),(xmax+20,ymax+20),(0,255,0),2)

        return self.lmList,bbox

    def findDistance(self,img,p1,p2,draw = True,r = 15, t = 3 ):

        x1,y1 = self.lmList[p1][1:]
        x2,y2 = self.lmList[p2][1:]
        cx,cy = (x1+x2)//2, (y1+y2)//2

        if draw :
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (cx, cy), r, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x1, y2), r, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 0), cv2.FILLED)
        lenght = math.hypot(x2-x1,y2-y1)
        return lenght,img,[x1,y1,x2,y2,cx,cy]

    def fingerUp(self):
        fingers = []
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0]-1][1] :
            fingers.append(1)
        else:
            fingers.append(0)
        for i in range(1,5):
            if self.lmList[self.tipIds[i]][2] < self.lmList[self.tipIds[i]-2][2]:
                fingers.append(1)
            else :
                fingers.append(0)
        return fingers

def main():
    cap = cv2.VideoCapture(0)
    pTime = 0
    cTime = 0
    detector = HandTrackingModule()

    while True:
        success,img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img,0)
        if lmList :
            print(lmList[1])
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),2)
        cv2.imshow("Video",img)
        if cv2.waitKey(1) == ord('q') :
            break

if __name__ == "__main__" :
    main()