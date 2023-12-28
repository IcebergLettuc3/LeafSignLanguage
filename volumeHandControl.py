import cv2
import time
import numpy as np

wCam, hCam = 1280, 720

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

while True:
  success, img = cap.read()

  cTime = time.time()
  fps = 1/(cTime - pTime)
  pTime = cTime

  cv2.putText(img, f'FPS: {int(fps)}', (20, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2 )
  
  cv2.imshow("Img", img)
  cv2.waitKey(1)