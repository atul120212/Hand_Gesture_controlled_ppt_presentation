import os
from cvzone.HandTrackingModule import HandDetector
import cv2
width, height = 1280, 720
folderPath = "Presentation"
#camera
cap = cv2.VideoCapture(0)
cap.set(3,width)
cap.set(4,height)
#get list of slides
pathImages = sorted(os.listdir(folderPath), key=len)
print(pathImages)
#var
imgNum = 0
hs,ws = int(120*1.2), int(213*1)
gestureThreshold = 300

#hand detector
detector = HandDetector(detectionCon=0.8,maxHands=1)
while True:
    #import images

    success, img = cap.read()
    img = cv2.flip(img, 1)
    pathFullImage = os.path.join(folderPath,pathImages[imgNum])
    imgCurent = cv2.imread(pathFullImage)

    hands, img = detector.findHands(img)#, flipType=False
    cv2.line(img,(0, gestureThreshold),(width, gestureThreshold),(0,255,0),10)

    if hands:
        hand = hands[0]
        fingers =detector.fingersUp(hand)
        cx, cy = hand['center']
        #print(fingers)
        if cy <= gestureThreshold: #if hand is at the height of the face
            #gest 1 -left
            if fingers == [1,0,0,0,0]:
                print('left')
            elif fingers == [0, 1, 1, 0, 0]:
                print('draw')
            elif fingers == [0, 0, 0, 0, 1]:
                print('right')
            elif fingers == [0, 1, 0, 0, 0]:
                print('point')

    #add webcam image on the slides
    imgSmall = cv2.resize(img, (ws,hs))
    h,w, _ = imgCurent.shape
    imgCurent[0:hs, w-ws:w] = imgSmall

    cv2.imshow("Image", img)
    cv2.imshow("Slide",imgCurent)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break