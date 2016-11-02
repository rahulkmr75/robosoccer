import cv2
import numpy as np
import opr
img=cv2.imread("arena.jpg")
hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
cv2.imshow("arena",hsv)
low=np.array([100,220,220])
up=np.array([140,255,255])

center,radius,line=opr.getArena(hsv,low,up)
#print center

print line
#opr.getCentralLine(hsv,low,up,center)
opr.getArena(hsv,low,up)
cv2.circle(img,center,radius,(0,0,255),2)
cv2.line(img,line[0][0],line[0][1],(0,0,255),3)

cv2.line(img,line[1][0],line[1][1],(0,0,255),3)

cv2.imshow("asdf",img)

cv2.waitKey(0)
cv2.destroyAllWindows()
