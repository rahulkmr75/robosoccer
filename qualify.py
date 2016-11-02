import cv2
import pid
import opr
import numpy as np
import botpos as bp
import const

#cap=cv2.VideoCapture(1)
bot=[[-1,-1],[-1,-1]]
u=0
while not rospy.is_shutdown():
    global u
    #get bot position bot[0]-head bot[1]-tail
    #ret,bgr=cap.read()
    bgr=cv2.imread("arena.png")
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    global bot
    bot[0]=bp.findMoment(hsv,const.bothead[0],const.bothead[1])
    bot[1]=bp.findMoment(hsv,const.bottail[0],const.bottail[1])
    
    #getting arena in every 50 frame
    if(u==0):
	center,radius,line=opr.getArena(hsv,const.myarena[0],const.myarena[1])
    u=u+1
    u=u%50
    
    #get opponents goal centroid as opgoal

    

    #get ball position
    ball=bp.findMoment(hsv,const.ball[0],const.ball[1])

    #get angular error and linear error
    angerr=opr.getTheta(bot[1],bot[0],ball)
    linerr=opr.distance(bot[0],ball)
    
    #get the motor velocities
    motorvel=pid.getVelocity(angerr,linerr)
    
    if(linerr<=qual_dist):
	motorvel=(peakvelocity,peakvelocity)

    k=cv2.waitKey(20) & 0xFF
    if k==27:
	break

cap.release()
cv2.destroyAllWindows()

