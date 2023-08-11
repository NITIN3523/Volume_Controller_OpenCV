import cv2
import mediapipe as mp


class handDetector:
    def __init__(self, mode=False, maxHands=2, modelComplex = 1,detectionCon=0.5, trackingCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplex = modelComplex
        self.detectionCon = detectionCon
        self.trackingCon = trackingCon
        self.mphands = mp.solutions.hands
        self.hands = self.mphands.Hands(self.mode,self.maxHands,self.modelComplex,self.detectionCon,self.trackingCon)
        self.mpDraw = mp.solutions.drawing_utils         

    def detectHand(self,img,draw = True):
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                     self.mpDraw.draw_landmarks(img,handLms,self.mphands.HAND_CONNECTIONS)

        return img
    
    def findPosition(self,img,handNo=0,draw=True):
        
        lmList = []
        if self.results.multi_hand_landmarks:
            myhand = self.results.multi_hand_landmarks[handNo]
            for id,lm in enumerate(myhand.landmark):
                h,w,c = img.shape
                cx,cy = int(lm.x * w),int(lm.y * h)
                lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)
        return lmList

