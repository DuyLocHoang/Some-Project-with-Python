import cv2
import time
import mediapipe as mp

class FaceDetector():
    def __init__(self,detectioncon = 0.5):
        self.min_detection_confidence = detectioncon
        self.mpFace = mp.solutions.face_detection
        self.face = self.mpFace.FaceDetection(self.min_detection_confidence)
        self.mpDraw = mp.solutions.drawing_utils
    def findFace(self,img,draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.face.process(imgRGB)
        bboxs = []
        if self.results.detections:
            for id, detection in enumerate(self.results.detections):
                # print(id, detection)
                # print(detection.score)
                # print(detection.location_data.relative_bounding_box)
                h, w, c = img.shape
                bboxC = detection.location_data.relative_bounding_box
                bbox = int(bboxC.xmin * w), int(bboxC.ymin * h), \
                       int(bboxC.width * w), int(bboxC.height * h)
                bboxs.append([id,bbox,detection.score])

                img = self.fancyDraw(img,bbox)
                cv2.putText(img, f'{int(detection.score[0] * 100)}%', (bbox[0], bbox[1] - 20), cv2.FONT_HERSHEY_PLAIN,
                            2, (255, 0, 255), 2)
        return img,bboxs
    def fancyDraw(self,img,bbox):
        x,y,w,h =bbox
        x1,y1 = (x+w),(y+w)
        # cv2.rectangle(img, bbox, (255, 0, 255), 3)
        #Top-Left
        cv2.line(img,(x,y),(x+20,y),(255,255,0),3)
        cv2.line(img, (x, y), (x, y+20), (255, 255, 0), 3)
        #Top-Right
        cv2.line(img,(x1,y),(x1-20,y),(255,255,0),3)
        cv2.line(img, (x1, y), (x1, y+20), (255, 255, 0), 3)
        #Bottom-Left
        cv2.line(img,(x,y1),(x+20,y1),(255,255,0),3)
        cv2.line(img, (x, y1), (x, y1-20), (255, 255, 0), 3)
        #Bottom-Right
        cv2.line(img,(x1,y1),(x1-20,y1),(255,255,0),3)
        cv2.line(img, (x1, y1), (x1, y1-20), (255, 255, 0), 3)
        return img
def main():
    cap = cv2.VideoCapture('data/head-pose-face-detection-female.mp4')
    cTime = 0
    pTime = 0
    detector = FaceDetector()
    while 1:
        success, img = cap.read()
        img,bbox = detector.findFace(img)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (50, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.imshow("Face", img)
        if cv2.waitKey(10) == ord('q'):
            break




if __name__ == '__main__':
    main()
