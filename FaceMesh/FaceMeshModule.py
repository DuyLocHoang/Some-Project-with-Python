import cv2
import mediapipe as mp
import time

class FaceMeshDetector():
    def __init__(self,mode = False,maxFace = 1,detectionCon = 0.5,trackingCon = 0.5):
        self.static_image_mode = False
        self.max_num_faces = 1
        self.min_detection_confidence = 0.5
        self.min_tracking_confidence = 0.5
        self.mpDraw = mp.solutions.drawing_utils
        self.drawSpec = self.mpDraw.DrawingSpec(thickness=1, circle_radius=1)
        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh()
    def findFaceMesh(self,img,draw = False):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceMesh.process(imgRGB)
        if self.results.multi_face_landmarks:
            faces = []
            for faceLms in self.results.multi_face_landmarks:
                if draw :
                    self.mpDraw.draw_landmarks(img, faceLms, self.mpFaceMesh.FACE_CONNECTIONS, self.drawSpec, self.drawSpec)
                face = []
                for id, lm in enumerate(faceLms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cv2.putText(img,str(id),(cx,cy),cv2.FONT_HERSHEY_PLAIN,0.7,(0,255,0),1)
                    # print(id, cx, cy)
                    face.append([id,cx,cy])
                faces.append(face)
        return img,faces

def main():
    cap = cv2.VideoCapture('data/head-pose-face-detection-female.mp4')
    cTime = 0
    pTime = 0
    detector = FaceMeshDetector()
    while 1:
        success, img = cap.read()
        img,faces = detector.findFaceMesh(img)
        print(len(faces))
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (50, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.imshow("FaceMesh", img)
        if cv2.waitKey(1) == ord('q'):
            break
if __name__ == "__main__":
    main()