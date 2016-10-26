import numpy as np 
import cv2
from sys import time
import opr
import const

#assumptions ----------------------------
'''x=c is the thresh line, opponents arena is near x axis'''

ballPositions = deque(maxlen=20)
centre_time=time.time()
mode_switch=0

def modes(mode,ballpos,circle_centre,opp_thresh_line,centre_diameter,my_goal_edge):
	# returns --- -1 for Null, 1 for start, 2 for defence, 3 for attack
	#assuming line of the form x=c or y=c, i.e, line parallel to camera

	if(ballpos!=None):
		ballPositions.append(ballpos)

	if(len(ballPositions)<20 or ballpos==None):
		return -1

	#check for mode start
	if(opr.distance(ballpos,circle_centre)<const.start_dist):
		centre_time=time.time()
		if((time.time()-centre_time)>1.5):
			mode_switch=1

	#check for mode defence
	#assuming line of form x=c
	elif(opr.distance(ballpos,(opp_thresh_line,0))<const.opp_line_dist):
		i=0
		dirctn=0
		while(i<4):
			dirctn+=ballPositions[19-i][1]-ballPositions[16-i][1]
			i++
		if(dirctn<0):
			mode_switch=2

	#check for mode attack
	elif(opr.Check_Arena(ballpos,centre_diameter,my_goal_edge)==0):
		while():
			check_motion


	if(mode_switch==1):
		return 1
	elif(mode_switch==2):
		return 2
	elif(mode_switch==3 & mode=2):
		return 3
	else:
		return mode

	
