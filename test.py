import cv2
import numpy as np

img=cv2.imread("arena.jpg")
hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
cv2.imshow("arena",hsv)
print hsv[300][150]
low=np.array([100,220,220])
up=np.array([140,255,255])
mask=cv2.inRange(hsv,low,up)
bot=cv2.GaussianBlur(mask,(5,5),0)
bot=cv2.GaussianBlur(mask,(5,5),0)
bot=cv2.GaussianBlur(mask,(5,5),0)
ret, bot = cv2.threshold(bot,-1,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
bot=cv2.GaussianBlur(mask,(5,5),0)
bot=cv2.GaussianBlur(mask,(5,5),0)
bot=cv2.GaussianBlur(mask,(5,5),0)
ret, bot = cv2.threshold(bot,-1,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

im2, contours, hierarchy = cv2.findContours(bot,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cnt=contours[0]
(x,y),radius = cv2.minEnclosingCircle(cnt)
center = (int(x),int(y))
radius = int(radius)
cv2.circle(bot,center,radius,(255,255,255),2)

cv2.imshow("asdf",bot)

cv2.waitKey(0)
cv2.destroyAllWindows()

