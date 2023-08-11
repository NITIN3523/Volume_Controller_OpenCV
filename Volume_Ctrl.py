import cv2
import time
import HandTracking as ht
import math
import numpy as np
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
# volume.GetMute()
# volume.GetMasterVolumeLevel()
range = volume.GetVolumeRange()
minRange = range[0]
maxRange = range[1]
volumeBar = 350
volumePer = 0

cap = cv2.VideoCapture(0)
detector = ht.handDetector()
cap.set(3,640)
cap.set(4,480)

cTime = 0
pTime = 0 

while True:
    success,img = cap.read()

    img = detector.detectHand(img)
    lmList = detector.findPosition(img,draw=False)

    if(len(lmList)!=0):
        # print(lmList[4] , lmList[8])

        x1,y1 = lmList[4][1],lmList[4][2]
        x2,y2 = lmList[8][1],lmList[8][2]
        c1,c2 = (x1+x2)//2,(y2+y1)//2
        cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),15,(255,0,255),cv2.FILLED)
        cv2.circle(img,(c1,c2),15,(255,0,255),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        length = math.hypot((x2-x1),(y2-y1))
        # print(length)

        # Hand Range 50 - 300 
        # Volume Range -65 - 0 
        volumeVal = np.interp(length,[20,250],[minRange,maxRange])
        volumeBar = np.interp(length,[20,250],[350,150])
        volumePer = np.interp(length,[20,250],[0,100])
        volume.SetMasterVolumeLevel(volumeVal, None)


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,"FPS : "+str(int(fps)),(10,70),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,0),2)
    cv2.rectangle(img,(50,150),(85,350),(0,255,0),2)
    cv2.rectangle(img,(50,int(volumeBar)),(85,350),(0,255,0),cv2.FILLED)
    cv2.putText(img,str(int(volumePer))+"%",(50,380),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)

    cv2.imshow("result",img)
    if cv2.waitKey(1) & 0xFF == ord('s'):
        break