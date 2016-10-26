import cv2
import numpy as np
import math
import time
from geometry_msgs.msg import Point
from std_msgs.msg import Int16
import rospy
import const

def pack(x):
	if x<0:
		x=abs(x)
		a=x&255
		a<<=8
	else:
		a=x&255
	return a

def main():
	rospy.init_node("main")
	pub1=rospy.Publisher("motor_vel1",Int16,queue_size=10)

	cap=cv2.VideoCapture(1)

	#stores the list of points in the path
	while not rospy.is_shutdown():
		ret,img=cap.read()
		if ret==0:
			cv2.waitKey(32)
			continue
		bckup=np.copy(img)

		gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

		
		cv2.imshow("backup",bckup)
	cv2.destroyAllWindows()
	cap.release()

#IF __main__ RUN THE MAIN FUNCTION. THIS IS THE MAIN THREAD
if __name__ == '__main__':
    main()