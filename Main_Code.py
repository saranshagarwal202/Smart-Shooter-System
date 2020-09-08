 #problem statement: to start a video and select colors based on rgb values. The result will contain a specified color.

import cv2
import numpy as np
def nothing(X):
    pass
def click_event(event,x,y,flag,param):
    if event == cv2.EVENT_RBUTTONDOWN:
        blue = img[y,x,0]
        green = img[y,x,1]
        red = img[y,x,2]

        font = cv2.FONT_HERSHEY_COMPLEX
        StrBGR = str(blue) + ',' + str(green) + ',' + str(red)
        cv2.putText(img,StrBGR,(x,y),font,1,(0,0,255),2)
        cv2.imshow('initial', img)
        print(StrBGR)
cv2.namedWindow('Trackbar',cv2.WINDOW_AUTOSIZE)
cv2.createTrackbar('LB','Trackbar',0,255,nothing)
cv2.createTrackbar('LG','Trackbar',0,255,nothing)
cv2.createTrackbar('LR','Trackbar',0,255,nothing)
cv2.createTrackbar('UB','Trackbar',255,255,nothing)
cv2.createTrackbar('UG','Trackbar',255,255,nothing)
cv2.createTrackbar('UR','Trackbar',255,255,nothing)

cv2.namedWindow('initial',cv2.WINDOW_NORMAL)
cv2.namedWindow('mask',cv2.WINDOW_NORMAL)
cv2.namedWindow('result',cv2.WINDOW_NORMAL)

cap = cv2.VideoCapture(0)
cv2.setMouseCallback('initial',click_event)
while(True):
    ret,img = cap.read()
    #cv2.imshow('initial',img)

    lb=cv2.getTrackbarPos('LB','Trackbar')
    lg=cv2.getTrackbarPos('LG','Trackbar')
    lr=cv2.getTrackbarPos('LR','Trackbar')
    ub=cv2.getTrackbarPos('UB','Trackbar')
    ug=cv2.getTrackbarPos('UG','Trackbar')
    ur=cv2.getTrackbarPos('UR','Trackbar')

    lower_limit=np.array([lb,lg,lr])
    upper_array=np.array([ub,ug,ur])

    mask=cv2.inRange(img,lower_limit,upper_array)
    cv2.imshow('mask',mask)

    result=cv2.bitwise_and(img,img,mask=mask)
    cv2.imshow('result',result)

    cv2.imshow('initial',img)

    k = cv2.waitKey(1)
    if k == 27:
        #cv2.destroyAllWindows()
        break
    #cap.release()

cap.release()
cv2.destroyAllWindows()
