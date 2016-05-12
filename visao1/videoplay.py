from __future__ import print_function

import cv2
import sys
import math
import numpy as np


cap = cv2.VideoCapture('hall_box_battery.mp4') 

while(True):
    

    dst = cv2.Canny(src, 50, 200)
    cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)

    if True: # HoughLinesP
        lines = cv2.HoughLinesP(dst, 1, math.pi/180.0, 40, np.array([]), 50, 10)
        a,b,c = lines.shape
        for i in range(a):
            cv2.line(cdst, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 3, cv2.CV_AA)
       

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

    cv2.imshow("detected lines", cdst)
    cv2.waitKey(0)

    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()