import cv2
import pid
import opr
import numpy as np
import const

#cap=cv2.VideoCapture(1)
bot=[[-1,-1],[-1,-1]]
u=0
center=(-1,-1)
radius=-1
line=[]
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
    global center,radius,line
    if(u==0):
	center,radius,line=opr.getArena(hsv,const.myarena[0],const.myarena[1])
    u=u+1
    u=u%50
    
    #get opponents goal centroid as opgoal

    #get ball position
    ball=bp.findMoment(hsv,const.ball[0],const.ball[1])
    dst=ball
    
    #get
    #find whether to go after the ball or the imaginary point
    pdis1=opr.pdistance(line[0][0],line[0][1],lin[1][0])
    pdis2=opr.pdistance(line[0][0],line[0][1],ball)

    #get angular error and linear error
    angerr=opr.getTheta(bot[1],bot[0],ball)
    linerr=opr.distance(bot[0],ball)
    
    #get the motor velocities
    motorvel=pid.getVelocity(angerr,linerr)
    
    if(linerr<=qual_dist):
	motorvel=(const.maxvelocity,const.maxvelocity)

    k=cv2.waitKey(20) & 0xFF
    if k==27:
	break

cap.release()
cv2.destroyAllWindows()

