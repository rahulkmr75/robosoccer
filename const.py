import numpy as np
#stores the value of constants
'''the first index is low_val the next is 
high_val'''

#colours of the arena
arenablue=np.array([[85,41,33],[120,165,125]])
arenayellow=np.array([[0,180,130],[35,255,255]])

#frequently used colours
#light green ,ribbon red,sepia blue
lgreen=np.array([[34,56,151],[78,165,255]])
rred=np.array([[0,185,140],[15,255,189]])
sblue=np.array([[98,100,141],[121,191,253])

bothead=np.array([[0,0,0],[180,255,255]])
bottail=np.array([[0,0,0],[180,255,255]])

opbotcol1=np.array([[0,0,0],[180,255,255]])
opbotcol2=np.array([[0,0,0],[180,255,255]])

myarena=np.array([[0,0,0],[180,255,255]])
oparena=np.array([[0,0,0],[180,255,255]])

ball=np.array([[0,0,0],[180,255,255]])

myarena=np.array([100,220,220],[140,255,255])

#the pid constants
klinear=0
kangular=0

start_dist=10
opp_line_dist=10
ball_motion_thresh=10

#qualifying criteria for the peak velocity aftr the 
#bot has reached the ball
qual_dist=10
