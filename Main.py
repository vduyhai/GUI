import cv2 as cv
import numpy as np
import time
import PoseModule as pm
import serial

cap = cv.VideoCapture('squat1.mp4')

ser = serial.Serial()

color = (255, 0, 255)
detector = pm.poseDetector()
set = 0
dir = 0 # 0: up & 1: down
pTime = 0
t = 10
count = 0

while True:
    _, img = cap.read()

    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)
    # print(lmList)
    if len(lmList) != 0:
        angle = detector.findAngle(img, 23, 25, 27)

        per = np.interp(angle, (185, 270), (0, 100))

        bar = np.interp(angle, (185, 270), (650, 100))

        if per == 100:
            if dir == 0:
                count += 0.5
                dir = 1
        if per == 0:
            if dir == 1:
                count += 0.5
                dir = 0
        # print(count)

        # Draw Bar
        cv.rectangle(img, (1100, 100), (1175, 650), color, 3)
        cv.rectangle(img, (1100, int(bar)), (1175, 650), color, cv.FILLED)
        cv.putText(img, f'{int(per)} %', (1100, 75), cv.FONT_HERSHEY_PLAIN, 4,
                    color, 4)

    #     # Draw Curl Count
        cv.putText(img, str(int(count)), (45, 670), cv.FONT_HERSHEY_PLAIN, 15,
                    (255, 0, 0), 25)
    print(count)

    cv.imshow("Image", img)
    cv.waitKey(1)