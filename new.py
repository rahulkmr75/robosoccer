from PIL import Image
from numpy import *
from pylab import *
import cv2
def nothing(x):
	pass

nothing


cap=cv2.VideoCapture(0)

cv2.namedWindow("track")
cv2.createTrackbar('H_MIN',"track",0,255,nothing)
cv2.createTrackbar('H_MAX',"track",0,180,nothing)
cv2.createTrackbar('S_MIN',"track",0,255,nothing)
cv2.createTrackbar('S_MAX',"track",0,255,nothing)
cv2.createTrackbar('V_MIN',"track",0,255,nothing)
cv2.createTrackbar('V_MAX',"track",0,255,nothing)

'''H_MIN=0
H_MAX=180
S_MIN=0
S_MAX=255
V_MIN=0
V_MAX=255'''

img=np.zeros([100,512,3])


while (cap.isOpened()):

	cv2.imshow("track",img)

	ret, bgr=cap.read()
	
	gray=cv2.cvtColor(bgr,cv2.COLOR_BGR2GRAY)
	hsv=cv2.cvtColor(bgr,cv2.COLOR_BGR2HSV)

	#getting the tracjbar positions
	H_MIN=cv2.getTrackbarPos('H_MIN',"track")
	H_MAX=cv2.getTrackbarPos('H_MAX',"track")
	S_MIN=cv2.getTrackbarPos('S_MIN',"track")
	S_MAX=cv2.getTrackbarPos('S_MAX',"track")
	V_MIN=cv2.getTrackbarPos('V_MIN',"track")
	V_MAX=cv2.getTrackbarPos('V_MAX',"track")

	#setting up range matrix for thresholding
	LOW=np.array([H_MIN,S_MIN,V_MIN])
	UP=np.array([H_MAX,S_MAX,V_MAX])

	#thresholding the hsv image
	mask = cv2.inRange(hsv, LOW,UP)

	#applying gaussian blur
	bot=cv2.GaussianBlur(mask,(5,5),0)
	bot=cv2.GaussianBlur(mask,(5,5),0)
	bot=cv2.GaussianBlur(mask,(5,5),0)
	# ret, gline = cv2.threshold(gline,100,255,cv2.THRESH_BINARY)
	ret, bot = cv2.threshold(bot,-1,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)


	#eroded image
	kernel=np.ones((5,5),np.uint8)
	eroded=cv2.erode(mask,kernel,iterations=1)

	#dilated image
	kernel1=np.ones((3,3),np.uint8)
	dilated=cv2.dilate(mask,kernel1,iterations=1)
	
	moments = cv2.moments(eroded)
	m00 = moments['m00']
	centroid_x, centroid_y = None, None
	if m00 != 0:
		centroid_x = int(moments['m10']/m00)
		centroid_y = int(moments['m01']/m00)
		cv2.circle(bgr,(centroid_x,centroid_y),5,(0,0,255),3)
	print centroid_x,centroid_y
	
	#finding contours and drawing contours
	#coimg,contours,hier=cv2.findContours(eroded,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	#dimg=cv2.drawContours(eroded,contours,-1,(0,0,255),3)

	cv2.imshow("bgr",bgr)
	cv2.imshow("masked_image",mask)
	cv2.imshow("eroded_image",eroded)
	cv2.imshow("dilated_image",dilated)
	#cv2.imshow("bgr",bgr)
	



	k = cv2.waitKey(25) & 0xFF
	if k == 27:
		break

cap.release()
cv2.destroyAllWindows()

	
