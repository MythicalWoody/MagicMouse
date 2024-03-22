import cv2
import HandTrackingModule as htm
import numpy as np
import time
import autopy


wCam = 640
hCam = 480
frameR = 100 # frame reduction
smoothening = 3
prevX , prevY = 0,0 # previous location of x and y
curX , curY = 0,0 # current location of x and y
cap = cv2.VideoCapture(0) #0 is for one camera but if i have multiiple cam then it can be 1
cap.set(3, wCam) # prop id for width is 3
cap.set(4, hCam) # prop id for hight is 4
pTime = 0
wScr , hScr = autopy.screen.size() # saving width and hight of the screen 
maxHands = int(1) 
detector = htm.handDetector(maxHands=maxHands) #It is telling that we are going to show max 1 hand so detect that only

while True: # This loop is to open the camera 
    #1 Find Hand
    success, img = cap.read()
    img = detector.findHands(img) # This detects if there is any hand in the image and returns highlighted hand
    lmList, bbox = detector.findPosition(img) # It take that image of highlighted hand and detects the position of fingers and store it in the lmList
                                              # It also finds the vounding box around the hand and stores it in the bBox
    

    #2 Get the tip of the index and middle finger 
    if len(lmList)!= 0: #If the length is zero then that means no hand was detected
        x1, y1 = lmList[8][1:] # 8 is a landmark for index finger
        x2, y2 = lmList[12][1:] # 12 is the landmark for middle finger now they will extract x and y cordinate


    #3 Check which fingers are up
    fingers = detector.fingersUp() # This will detect and count how many fingers are up
    cv2.rectangle(img, (frameR,frameR), (wCam-frameR,hCam-frameR),(255,0,255), 2) #creates a rectangle to show the navigation area
    #4 Only index finger then moving mode 
    if fingers[1] == 1 and fingers[2] == 0:

    #5 Convert coordinates
        x3 = np.interp(x1, (frameR,wCam-frameR),(0,wScr)) # it takes the x and y cordinate and maps it to the screen coordinates
        y3 = np.interp(y1, (frameR,hCam-frameR),(0,hScr))



    #6 Smoothen Values
        curX = prevX +(x3 - prevX) / smoothening
        curY = prevY +(y3 - prevY) / smoothening


    #7 Move Mouse
        # Pointer does not go out of bounds
        if curX < 0:
            curX = 0
        if curX > wScr:
            curX = wScr
        if curY < 0:
            curXY= 0
        if curY > hScr:
            curY = hScr
        autopy.mouse.move(wScr-curX,curY)
        cv2.circle(img, (x1,y1), 15, (255,0,255),cv2.FILLED)
        prevX,prevY = curX,curY



    #8 Both Index and middle fingers are up: Clicking mode
    if fingers[1] == 1 and fingers[2]  == 1:  #if both the fingers are up
        length,img, lineInfo = detector.findDistance(8,12,img)  
        print(length)
        if length < 40: # when both fingers were sticking we were getting length value to be approx 32 so we are taking any value less than 40 to initiate click
            cv2.circle(img , (lineInfo[4],lineInfo[5]), 15, (0,255,0), cv2.FILLED) #and when we are clicking, the circle between the two fingers will turn green.
            autopy.mouse.click()


    #11 Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img,str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN,3,255,0,0)
    #12 Display
    img = cv2.flip(img,1) # This will flip the video along vertical axis
    cv2.imshow("Image", img)
    cv2.waitKey(1)