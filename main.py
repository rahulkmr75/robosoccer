import cv2
import numpy as np
import math
import time
from geometry_msgs.msg import Point
from std_msgs.msg import Int16
import rospy
import const
import opr
import pid

dst=const.head
def main():
    
    #if dst is head then target is 0, 1 if it's tail and 2 if it's center
    global dst
    target=0
    
    #cap=cv2.VideoCapture(1)
    bot=[[-1,-1],[-1,-1]]
    u=0
    center=(-1,-1)
    radius=-1
    line=[]
    head=const.head
    tail=const.tail
    center=const.linecenter
    while not rospy.is_shutdown():
	global u
	 #get bot position bot[0]-head bot[1]-tail
        #ret,bgr=cap.read()
        bgr=cv2.imread("arena.png")
	hsv=cv2.cvtColor(bgr,cv2.COLOR_BGR2HSV)
        global bot
        bot[0]=opr.getCentroid(hsv,const.bothead[0],const.bothead[1])
        bot[1]=opr.getCentroid(hsv,const.bottail[0],const.bottail[1])
    
        #getting arena in every 50 frame
        global center,radius,line
        if(u==0):
		center,radius,line=opr.getArena(hsv,const.myarena[0],const.myarena[1])
        u=u+1
        print "frame= ",u
        u=u%50
    
        #get opponents goal centroid as opgoal

	 #get ball position
        ball=opr.getCentroid(hsv,const.ball[0],const.ball[1])
        dst=ball
    
        #get
        #find whether to go after the ball or the imaginary point
        pdis1=opr.pdistance(line[0][0],line[0][1],line[1][0])
        pdis2=opr.pdistance(line[0][0],line[0][1],ball)
        #call the imaginary lne finding function


	if(pdis1<pdis2):
	    pass

        #get angular error and linear error
        angerr=opr.getTheta(bot[1],bot[0],const.head)
	linerrball=opr.distance(bot[0],ball)
	
	linerr=opr.distance(bot[0],dst)
    
	 #get the motor velocities
        motorvel=pid.getVelocity(angerr,linerr)
	
	#move according to the  distance between ball head,tail,center
	dishead=opr.distance(ball,head)
	distail=opr.distance(ball,tail)
	discenter=opr.distance(ball,center)
	if(dishead<distail and dishead<discenter):
	    dst=head
	    target=0
	elif(distail<discenter):
	    dst=tail
	    target=1
	else:
	    dst=center
	    target=2
	
	#give an impulsive velocity if the bot is very close to the ball
	if(linerr<=const.qual_dist):
	    motorvel=(const.maxvelocity,const.maxvelocity)
	if(target==1 and abs(angerr)<const.angthresh):
	    motorvel=(motorvel[0]*-1,motorvel[1]*-1)
	if(target==2 and opr.distance(bot[0],head)>opr.distance(bot[0],tail)):
	    motorvel=(motorvel[0]*-1,motorvel[1]*-1)

        print line
        cv2.circle(bgr,center,radius,(0,0,255),2)
        cv2.line(bgr,line[0][0],line[0][1],(0,0,255),3)
        cv2.line(bgr,line[1][0],line[1][1],(0,0,255),3)
        cv2.circle(bgr,bot[0],4,(255,0,0),-1)
        cv2.imshow("bgr",bgr)
        k=cv2.waitKey(20) & 0xFF
        if k==27:
	    break

    cap.release()
    cv2.destroyAllWindows()

#IF __main__ RUN THE MAIN FUNCTION. THIS IS THE MAIN THREAD
if __name__ == '__main__':
    main()
