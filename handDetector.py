import mediapipe as mp
import cv2

## mediapipe는 hand detect를 먼저하고, 이후에 track을 함.

# mediapipe 모듈 초기화
mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils

class HandDetector:
    def __init__(self, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5):  # max_num_hands = 2
        self.hands = mpHands.Hands(max_num_hands=max_num_hands, min_detection_confidence=min_detection_confidence,
                                   min_tracking_confidence=min_tracking_confidence)


    def findHandLandMarks(self, image, draw=False):
        originalImage = image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image)

        landMarkList = []
        label = [[], []]

        if results.multi_handedness:            
            for hand_cnt in range(len(results.multi_handedness)):
                tmp_label = results.multi_handedness[hand_cnt].classification[0].label  # left/right hand labeling
                if tmp_label == "Left":  # 웹캠 반대로 labeling
                    label[hand_cnt] = "Right"
                elif tmp_label == "Right":
                    label[hand_cnt] = "Left"
            

        if results.multi_hand_landmarks:  # 손 검출 안되면, None return
            hand_flag = True    
            for hand in results.multi_hand_landmarks:
                for id, landMark in enumerate(hand.landmark):
                    imgH, imgW, imgC = originalImage.shape  # imgH: height, imgW: width, imgC: channel
                    xPos, yPos = int(landMark.x * imgW), int(landMark.y * imgH)
                    
                    hand_cnt = len(results.multi_handedness)
                    if hand_flag == True: 
                        landMarkList.append([id, xPos, yPos, label[0], hand_cnt])  # [id: 0~20, Xpos, yPos, label: Left, Right, hand_cnt: 0~1]
                    else:
                        landMarkList.append([id, xPos, yPos, label[1], hand_cnt])
                    if id >= 20:  # 양손 따로 체크
                        hand_flag = False

                if draw:
                    mpDraw.draw_landmarks(originalImage, hand, mpHands.HAND_CONNECTIONS)

        return landMarkList