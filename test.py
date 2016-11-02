import cv2
import numpy as np
import opr
import const
img=cv2.imread("arena.png")
hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
cv2.imshow("arena",hsv)

center,radius,line=opr.getArena(hsv,const.myarena[0],const.myarena[1])
print center,radius

print line
#opr.getCentralLine(hsv,low,up,center)
cv2.circle(img,center,radius,(255,0,255),2)
cv2.line(img,line[0][0],line[0][1],(0,0,255),3)

cv2.line(img,line[1][0],line[1][1],(0,0,255),3)

cv2.imshow("asdf",img)

cv2.waitKey(0)
cv2.destroyAllWindows()
