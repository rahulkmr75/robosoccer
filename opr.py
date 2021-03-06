import cv2
import numpy as np
from matplotlib import pyplot as plt
import time
from geometry_msgs.msg import Point
import math

def checkAlignment(bothead,bottail,line,center):
    vecbot=[bothead[0]-bottail[0],bothead[1]-bottail[1]]
    vecline=[line[1][0]-line[0][0],line[1][1]-line[0][1]]
    botcenter=[(bothead[0]+bottail[0])/2,(bothead[1]+bothead[1])/2]
    theta=getTheta(botcenter,bothead,line[0])
    distance=pdistance(line[0],line[1],botcenter)
    return thetha,distance

def getArena(hsv,low,up):
    hsv2=np.copy(hsv)
    mask=cv2.inRange(hsv2,low,up)
    maskblur=cv2.GaussianBlur(mask,(5,5),0)
    maskblur=cv2.GaussianBlur(mask,(5,5),0)
    maskblur=cv2.GaussianBlur(mask,(5,5),0)
    ret, maskblur = cv2.threshold(maskblur,-1,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    cv2.imshow("im2",maskblur)
    im2, contours, hierarchy = cv2.findContours(maskblur,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cnt=contours[0]
    for i in contours:
	if (cv2.contourArea(cnt)<cv2.contourArea(i)):
	    cnt=i

    (x,y),radius = cv2.minEnclosingCircle(cnt)
    center = (int(x),int(y))
    radius = int(radius)

    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(hsv2,[box],0,(0,0,0),2)
    cv2.imshow("try",hsv2)
    line1=[box[0],box[1]]
    dis=pdistance(box[0],box[1],center)
    print dis,line1
    for i in range(1,4):
        temp=pdistance(box[i],box[(i+1)%4],center)
	print temp,box[i],box[(i+1)%4]
        if(temp<dis):
            dis=temp
            line1=[box[i],box[(i+1)%4]]
		#since most of the cv functions require tuple format
    line1=toTuple(line1)

    #getting the second line
    m1=getSlope(line1[0],line1[1])    
    line2=[box[0],box[1]]
    for i in range(0,4):
	line2=[box[i],box[(i+1)%4]]
	m2=getSlope(line2[0],line2[1])
	if(abs(m2[0])==abs(m1[0]) and abs(m2[1])==abs(m1[1])):
	    if(distance(line2[0],line1[0])>0 and distance(line2[1],line1[0])>0):
		break
    line2=toTuple(line2)
    line=[line1,line2]
    return center,radius,line

#get slope returns the cosine and sine value of a line
def getSlope(p1,p2):
    dist=distance(p1,p2)
    costheta=(p2[0]-p1[0])/dist
    sintheta=(p2[1]-p1[1])/dist
    return [costheta,sintheta]

#converts a list of array to a list of tuples
def toTuple(line):
	for i in range(0,len(line)):
		line[i]=(line[i][0],line[i][1])
	return line

		
def pdistance(lp1,lp2,p):
    if(lp1[0]==lp2[0]):
        return abs(lp1[1]-p[1])
    else:
        m=(lp2[1]-lp1[1])*1.0/(lp2[0]-lp1[0])
        c=lp2[1]-(m*lp2[0])
        d=abs((p[1]-m*p[0]-c)/math.sqrt(1+m*m))
        return d
def distance(p1,p2):
    return(math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2))
    
#returns angle between three points p1p0p2 -> [0,2pi]
#in opencv y-axis in opposite to the traditional style
#so theta also goes the other way
def getTheta(p0,p1,p2):
    #just translate the origin to p0
    x2=p2[0]
    y2=p2[1]
    x1=p1[0]
    y1=p1[1]
    vec=[x1-p0[0],y1-p0[1]]
    theta3=0
    try:
        theta1=math.acos(vec[0]/math.sqrt(vec[0]**2+vec[1]**2))
        if (p1[1]>p0[1]):
            theta1=2*math.pi-theta1
    except ZeroDivisionError:
        theta1=0
    #print vec,theta1

    vec=[x2-p0[0],y2-p0[1]]
    try:
        theta2=math.acos(vec[0]/math.sqrt(vec[0]**2+vec[1]**2))
        if (p2[1]>p0[1]):
            theta2=2*math.pi-theta2
    except ZeroDivisionError:
        theta2=0
    #print vec,theta2
    theta3=theta2-theta1

    if theta3>math.pi:
	theta3=theta3-2*math.pi
    elif theta3<(-1*math.pi):
	theta3=theta3+2*math.pi
    #print theta1,theta2,theta3
    return theta3
    
#gives you the centroid of a region after masking and other crap
def getCentroid(img,low_val,up_val):

    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    #masking everything else other than green
    mask=cv2.inRange(hsv,low_val,up_val)

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
    if centroid_x != None and centroid_y != None:
        return (centroid_x, centroid_y)
    else:
        return (-1,-1)

def getImagLine(dm,centre,radius,myArena):
	#assuming an angle of 90 degree subtended at centre by this imaginary line
	width=distance(dm[0],dm[3])
	length=distance(dm[0],dm[1])
	if(width>length):
		temp=length
		length=width
		width=temp
	#print width,length
	m=radius/1.414
	n=width-m
	#print (m,n)
	points_temp=[[(n*dm[0][0]+m*dm[3][0])/(m+n),(n*dm[0][1]+m*dm[3][1])/(m+n)],[(n*dm[1][0]+m*dm[2][0])/(m+n),(n*dm[1][1]+m*dm[2][1])/(m+n)]]
	#print points_temp
	m=(length-radius*1.414)/2
	n=radius*1.414+m
	points=[[(n*points_temp[0][0]+m*points_temp[1][0])/(m+n),(n*points_temp[0][1]+m*points_temp[1][1])/(m+n)],[(m*points_temp[0][0]+n*points_temp[1][0])/(m+n),(m*points_temp[0][1]+n*points_temp[1][1])/(m+n)]]
	if(myArena==1):
		point_temp=points_temp[0]
		points_temp[0]=points_temp[1]
		points_temp[1]=point_temp
	return points

#given two points in the x-y plane it lists the points lying on the line between the
#two points
def listPathPoints1(start,end):
    stx=start[0]
    sty=start[1]
    enx=end[0]
    eny=end[1]
    l=[]
    vx=(enx-stx)
    vy=(eny-sty)
    if (vx==0 and vy==0):
        return start
    d=int(math.sqrt((stx-enx)**2+(sty-eny)**2))
    cos=vx/math.sqrt(vx**2+vy**2)
    sin=vy/math.sqrt(vx**2+vy**2)
    i=1
    while(i<d):
        l.append([int(stx+cos*i),int(sty+sin*i)])
        i=i+1
    return l

#given a binary image if there is a gradient around the pixel it marks them white 
#not a perfect code
def findGradient(gline):
    r,c=gline.shape
    bgr = np.zeros((r,c),np.uint8)
    #print r,c
    t=0
    for i in range(0,r-1):
        for j in range(0,c-1):
            #print gline[i][j]
            if (i<4 or i>r-5 or j<4 or j>c-5):
                pass
            else:
                '''g0=(gline[i+4][j]-gline[i][j])/4
                g45=(gline[i+4][j+4]-gline[i][j])/6.8
                g90=(gline[i][j+4]-gline[i][j])/4.0
                g135=(gline[i-4][j+4]-gline[i][j])/6.8
                g180=(gline[i][j-4]-gline[i][j])/4.0
                g225=(gline[i-4][j-4]-gline[i][j])/6.8
                g270=(gline[i-4][j]-gline[i][j])/4.0
                g315=(gline[i+4][j-4]-gline[i][j])/6.8;
                if (g0>g45 and g0>g90 and g0>g135 and g0>g180 and g0>g225 and g0>270 and g0>g315):
                    bgr=cv2.line(gline,(i,j),(i+4,j),(0,0,255),2)
                    t=t+1'''
                gx=(gline[i+4][j]-gline[i][j])/4
                gy=(gline[i][j+4]-gline[i][j])/4
                g=math.sqrt(gx**2+gy**2)
                #print g
                if(g>0):
                    bgr[i][j]=255
                    t=t+1

    #print t
    return bgr

#given a binary image it tries to find a path avoiding collosion with obstacles
def findPath(obstacle,pp1):
    #obstacle is the binary image where black indicates obstacle
    #pp1 is the list f points on the line

    #stores the intersection point
    l=[]

    #finding the contours
    obstacle1=np.copy(obstacle)
    obstacle1, contours, hierarchy = cv2.findContours(obstacle1,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    obstacle1=cv2.drawContours(obstacle1, contours, -1, (255,255,255), 1)
    cv2.imshow("obstacle1",obstacle1)
    #print len(contours)

    for i in contours:
        #i is the contour ,a set of points
        lc=[]
        intersection=0
        for j in i:
            #j is the point of a particular contours
            #print j[0]
            for k in pp1:
                #print k
                if (np.all(k==j)):
                    l.append(k)
                    intersection+=1
        print intersection
        if (intersection==1):
            print "no possible path"
            return
        elif (intersection>=2):
            #con1 and con2 stores the point of intersection 
            con1=l[len(l)-intersection]
            con2=l[len(l)-1]
            print con1,con2

            #making the two list to choose the shortest path
            l1,l2=seggregate(i,con1,con2)

            #print l1
            #print l2
            #structure of l1 and l2 are array([[el1,el2]])
            l1=rectify(l1)
            l2=rectify(l2)
            #print l1,l2
            

            #sends the shortest path for insertion 
            if (checkContinuity(l1,con1,con2)==1 and checkContinuity(l2,con1,con2)==1):
                if (len(l1)<len(l2)):
                    print "l1 is sent as both are continuos and len l1<l2",len(l1),len(l2)
                    insert(l1,pp1)
                else:
                    print "l2 is sent as both are continuos and len l1>l2",len(l1),len(l2)
                    insert(l2,pp1)
            elif checkContinuity(l1,con1,con2)==1:
                insert(l1,pp1)
            else :
                insert(l2,pp1)
                
    for i in pp1:
        obstacle1=cv2.circle(obstacle1,(i[0],i[1]),3,(127,127,127),-1)
    cv2.imshow("newewrsdaf",obstacle1)


#if elements  in a list are nested unnecessarily i.e. [[a,b]], use rectify
def rectify(l):
    #print len(l)

    for i in range (0,len(l)):
        l[i]=[l[i][0][0],l[i][0][1]]
    return l


#makes two list after breaking it at the intersection point
def seggregate(i,con1,con2):
    l1=[]
    l2=[]
    addtol1=0
    t=0
    while(len(l1)+len(l2)<=len(i)+1):
        if (np.all(con1==i[t]) or np.all(con2==i[t])):
            addtol1+=1
        if addtol1==1:
            l1.append(i[t])
        elif addtol1>=2:
            if (len(l2)==0):
                l1.append(i[t])
            l2.append(i[t])

        t+=1
        t%=len(i)
    return l1,l2

    '''print i,con1,con2
    for j in range(0,len(i)):
        if (np.all(i[j]==con1)):
            p1=j
        elif (np.all(i[j]==con2)):
            p2=j

    if p1>p2:
        p1,p2=p2,p1
    l1=i[p1:p2+1]
    l2=i[p2:]
    l2[len(l2):]=i[0:p1+1]

    return l1,l2'''

#check whether a list is continuos from initial to final point
def checkContinuity(l,con1,con2):
    #as checkContinuity pop the element out
    '''l=[]
    l[:]=ol[:]
    while(len(l)>1):
        print(len(l))
        j=1
        while (j<len(ol)):
            if (distance(l[0],l[j])<3):
                l.pop(0)
                break
            j+=1
        if (j==len(l)):
            return 0
    if (len(l)==1):
        return 1'''

    #1 means continuos and zero discontinuos
    flag=1
    for i in range(0,len(l)-1):
        if (distance(l[i],l[i+1])>3):
            flag=0
            break
    return flag


#the insert thing i.e removes the points in path lyin on the obstacle
#and inserts a new list making a possible path  
def insert(lc,pp1):
    #print lc,"sadklfksldjlkfjsdlkfkl",pp1
    #print "got one"

    first=lc[0]
    last=lc[len(lc)-1]

    for i in range(0,len(pp1)):
        #if (np.all(lc[0]==pp1[i])):
        if (np.all(lc[0]==pp1[i])):
            begin=i
        #elif (np.all(lc[len(lc)-1]==pp1[i])):
        elif(np.all(lc[len(lc)-1]==pp1[i])):
            end=i
    if begin<end:
        pp1[begin-1:end]=lc[:]
    else:
        pp1[end-1:begin]=lc[:]


#wanna compute distance between two points use distance

    

'''these are the backup things,in case...'''
def findPath1(obstacle,pp1):
    r,c=obstacle.shape
    begin=[-1,-1]
    st_begin=0
    end=[-1,-1]
    st_end=0
    for i in range(0,len(pp1)-1):

        if obstacle[pp1[i][0]][pp1[i][1]]==0:
            if st_begin==0:
                begin=pp1[i-1]
                st_begin=1
            pp1.pop(i)
        elif (obstacle[pp1[i][0]][pp1[i][1]]==255 and st_begin==1):
            st_end=1
            end=pp1[i]
        if (st_end==1 and st_begin==1):
            #l is lpp from begin to e to end
            l=getSecondaryPath(obstacle,begin,end)
            try:
                for j in range(0,len(l)):
                    pp1.insert(i,l[len(l)-1-j])
                i+=len(l)-1
            except TypeError:
                pass

    return pp1

def getSecondaryPath(obstacle,begin,end):
    r,c=obstacle.shape
    for i in range(0,r):
        for j in range (0,c):
            #state for continuation
            cnts=0
            l1=listPathPoints1(begin,[i,j])

            for k in l1:
                if (obstacle[k[0]][k[1]]==0):
                    cnts=1
                    break
            if cnts==1:
                #just go for next point 
                #one of the points in the list is black 
                continue
        
            l2=listPathPoints1([i,j],end)
            for k in l2:
                if (obstacle[k[0]][k[1]]==0):
                    cnts=1
                    break
            if cnts==1:
                #just go for the next point 
                #one of the points in the another list was black again
                continue

            try:
                if((len(l1)+len(l2))<(len(pl1)+len(pl2))):
                    pl1=l1
                    pl2=l2
            except NameError:
                pl1=l1
                pl2=l2

    try:
        for i in pl1:
            l.append(i)
        for j in pl2:
            l.append(j)
        return l
    except NameError:
        #no secondary path possible
        return

def check_Arena(ballpos,centre_diameter,my_goal_edge):
    #assuming the centre diameter to be y=c
    if(my_goal_edge==0):
        if(ballpos[1]<centre_diameter):
            return 0
        else:
            return 1
    elif(my_goal_edge==1):
        if(ballpos[1]>centre_diameter):
            return 0
        else:
            return 1
