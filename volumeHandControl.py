import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam, hCam = 1280, 720

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.7)
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
# print(volume.GetVolumeRange())
minVol = volRange[0]
maxVol = volRange[1]

while True:
  success, img = cap.read()
  img = detector.findHands(img)
  lmList = detector.findPosition(img, draw=False)
  if lmList:
    # print(lmList[2])
    x1, y1 = lmList[4][1], lmList[4][2]
    x2, y2 = lmList[8][1], lmList[8][2]
    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

    cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
    cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
    cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

    length = math.hypot(x2 - x1, y2 - y1)
    # print(length)
    #hand range: 50 -> 300
    vol = np.interp(length, [50, 300], [minVol, maxVol])
    bar = np.interp(length, [50, 300], [400, 150])
    percentage = np.interp(length, [50, 300], [0, 100])
    print(vol)
    volume.SetMasterVolumeLevel(vol, None)

    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
    cv2.rectangle(img, (50, int(bar)), (85, 400), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, f'{int(percentage)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 3)

    if length < 50:
      cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

    


  cTime = time.time()
  fps = 1/(cTime - pTime)
  pTime = cTime

  cv2.putText(img, f'FPS: {int(fps)}', (20, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2 )
  
  cv2.imshow("Volume Control", img)
  cv2.waitKey(1)
  if cv2.getWindowProperty('Volume Control', cv2.WND_PROP_VISIBLE) < 1:
    print("Exiting application")
    break