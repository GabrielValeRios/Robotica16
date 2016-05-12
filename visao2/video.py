import cv2
import sys
import math
import numpy as np
import time


cap = cv2.VideoCapture('video_corredor_novo.mp4') 


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Display the resulting frame
    
    #cv2.imshow('frame',frame)

    #time.sleep(5)

    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

    # try:
    #     fn = sys.argv[1]
    # except IndexError:
    #     fn = "hall_box_battery.mp4"
 
    src = frame
    dst = cv2.Canny(src, 50, 200)
    cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)

    

    if True: # HoughLinesP
        lines = cv2.HoughLinesP(dst, 1, math.pi/180.0, 40, np.array([]), 50, 10)
        a,b,c = lines.shape
        for i in range(a):
            cv2.line(cdst, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 3, cv2.CV_AA)
      


            if (lines[i][0][3]-lines[i][0][1])/(lines[i][0][2] - lines[i][0][0]) > 0.01 and (lines[i][0][3]-lines[i][0][1])/(lines[i][0][2] - lines[i][0][0]) < -0.01:
                verticalF = True
            else:
                verticalF = False

            if (lines[i][1][3] - lines[i][1][1])/(lines[i][1][2] - lines[i][1][0]) > 0.01 and (lines[i][1][3] - lines[i][1][1])/(lines[i][1][2] - lines[i][1][0]) < -0.01:
                verticalS = True
            else:
                verticalS = False

            if verticalF == False and verticalS == False:

                cv2.line(cdst, ((lines[i][0][0] + lines[i][1][0])/2, 0), ((lines[i][0][2] + lines[i][1][2])/2, 1800), (0, 255, 0), 3, cv2.CV_AA)
            
            
    else:    # HoughLines
        lines = cv2.HoughLines(dst, 1, math.pi/180.0, 50, np.array([]), 0, 0)
        a,b,c = lines.shape
        for i in range(a):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0, y0 = a*rho, b*rhos
            pt1 = ( int(x0+1000*(-b)), int(y0+1000*(a)) )
            pt2 = ( int(x0-1000*(-b)), int(y0-1000*(a)) )
            cv2.line(cdst, pt1, pt2, (0, 0, 255), 3, cv2.CV_AA)

    #cv2.imshow("source", src)
    cv2.imshow("detected lines", cdst)
    cv2.waitKey(1)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()