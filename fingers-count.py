from handDetector import HandDetector
import cv2
import math
import numpy as np


handDetector = HandDetector(min_detection_confidence=0.7)
webcamFeed = cv2.VideoCapture(0)


while True:
    status, image = webcamFeed.read()
    handLandmarks = handDetector.findHandLandMarks(image=image, draw=True)
    count = 0

    if(len(handLandmarks) != 0):
        if handLandmarks[4][3] == "Right" and handLandmarks[4][1] > handLandmarks[3][1]:    # 오른쪽 엄지(Right Thumb)
            count = count+1
        elif handLandmarks[4][3] == "Left" and handLandmarks[4][1] < handLandmarks[3][1]:   # 왼쪽 엄지(Left Thumb)
            count = count+1
        if handLandmarks[8][2] < handLandmarks[6][2]:   # 검지(Index finger)
            count = count+1
        if handLandmarks[12][2] < handLandmarks[10][2]: # 중지(Middle finger)
            count = count+1
        if handLandmarks[16][2] < handLandmarks[14][2]: # 약지(Ring finger)
            count = count+1
        if handLandmarks[20][2] < handLandmarks[18][2]: # 새끼(Little finger)
            count = count+1

        if handLandmarks[4][4] == 2:  # 손이 2개 일때 다른 손도 더함
            if handLandmarks[25][3] == "Right" and handLandmarks[25][1] > handLandmarks[24][1]:    # 오른쪽 엄지(Right Thumb)
                count = count+1
            elif handLandmarks[25][3] == "Left" and handLandmarks[25][1] < handLandmarks[24][1]:   # 왼쪽 엄지(Left Thumb)
                count = count+1
            if handLandmarks[29][2] < handLandmarks[27][2]:
                count = count+1
            if handLandmarks[33][2] < handLandmarks[31][2]:
                count = count+1
            if handLandmarks[37][2] < handLandmarks[35][2]:
                count = count+1
            if handLandmarks[41][2] < handLandmarks[39][2]:
                count = count+1

    cv2.putText(image, str(count), (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 0, 0), 25)
    cv2.imshow("Volume", image)
    cv2.waitKey(1)