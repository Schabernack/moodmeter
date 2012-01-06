import cv
import math
import numpy as np
from logger import Logger


class MatchingUnit:
		
	def run(self,image):
		ori = self.getOrientation(image)
		angle = self.getAngle(image)
		
		print ori,angle
		
		if ori == "up" and angle > 90:
			angle = 180 - angle
		elif ori == "down" and angle < 90:
			angle = 180 + angle
		elif ori == "right" and angle > 180:
			angle = 360 - angle
				
			
		return angle
		
	
	def getOrientation(self,image):
		vertical,upper,lower = self.getRectangles(image)
	
		upMat = cv.GetSubRect(image,upper)
		upMatSize = upMat.rows*upMat.cols
		upCountNonZero = cv.CountNonZero(upMat)
		upCountZero = upMatSize - upCountNonZero
		
		lowMat = cv.GetSubRect(image,lower)
		lowMatSize = lowMat.rows*lowMat.cols
		lowCountNonZero = cv.CountNonZero(lowMat)
		upCountZero = lowMatSize - upCountNonZero
						
		#print "Percentage of White pixels in upper mat",upCountNonZero,100*float(upCountNonZero)/float(upMatSize),"%"
		#print "Percentage of White pixels in lower mat",lowCountNonZero,100*float(lowCountNonZero)/float(lowMatSize),"%"
		
		if vertical:
			if upCountNonZero<lowCountNonZero:
				return "up"
			else:
				return "down"
		else:
			if upCountNonZero<lowCountNonZero:
				return "left"
			else:
				return "right"

	## Returns upper and lower half of bounding rect (upper & lower) and if vertical or not
	def getRectangles(self,image):		
		img_tmp = cv.CreateMat(image.height,image.width,cv.CV_8UC1)
		cv.Copy(image,img_tmp)
		cont = cv.FindContours(img_tmp,cv.CreateMemStorage(),mode=cv.CV_RETR_EXTERNAL,method=cv.CV_CHAIN_APPROX_NONE)
		x,y,width,height = cv.BoundingRect(cont)		
		if height >= width:
			upper = (x,y,width,int(height/2))
			lower = (x,y+int(height/2),width,int(height/2))
			vertical = True
		else:
			upper = (x,y,int(width/2),height)
			lower = (x+int(width/2),y,int(width/2),height)
			vertical = False
		
		return vertical, upper, lower	
		
		
	def getAngle(self,image):
		img_tmp = cv.CreateMat(image.height,image.width,cv.CV_8UC1)
		cv.Copy(image,img_tmp)
		img_cont = cv.CreateMat(image.height,image.width,cv.CV_8UC3)
		img_hull = cv.CreateMat(image.height,image.width,cv.CV_8UC3)
		
		cv.Zero(img_hull)
		
		cv.CvtColor(image,img_cont,cv.CV_GRAY2BGR)
		contour = cv.FindContours(img_tmp,cv.CreateMemStorage(),mode=cv.CV_RETR_EXTERNAL,method=cv.CV_CHAIN_APPROX_NONE)
		cv.DrawContours(img_cont,contour,(255,0,0),(0,255,0),0,thickness=2)
		rect = cv.BoundingRect(contour)
		cv.Rectangle(img_cont,(int(rect[0]),int(rect[1])),(int(rect[0]+rect[2]),int(rect[1]+rect[3])),(0,255,0))	
		#hull = cv.ConvexHull2(contour,cv.CreateMemStorage(),return_points=1)
		#cv.PolyLine(img_cont, [hull], 1, (255,0,0),thickness=2)
			
		line = cv.FitLine(contour,cv.CV_DIST_L2,0,0.01,0.01)
		
		v0,v1,x0,x1 = line
		pt0 = int(x0+200*v0),int(x1+200*v1)
		pt1 = int(x0-200*v0),int(x1-200*v1)
		
		u0 = 0
		u1 = 1
		u = (u0,u1)
		
		pt2 = int(x0+200*u0),int(x1+200*u1)
		pt3 = int(x0-200*u0),int(x1-200*u1)
		
		
		v = (v0,v1)
		c	= np.dot(u,v)/np.linalg.norm(u)/np.linalg.norm(v)
		angle = np.arccos(c)
		angle *= 180/np.pi
				
		cv.Line(img_cont, pt0, pt1, (0,0,255), thickness=2, lineType=8, shift=0)
		cv.Line(img_cont, pt2, pt3, (0,140,255), thickness=2, lineType=8, shift=0)

		
		
		font = cv.InitFont(cv.CV_FONT_HERSHEY_COMPLEX_SMALL,1.0,1.0,thickness=1)
		cv.PutText(img_cont, "Legend:", (10,20) , font, (255,255,255))
			
		font = cv.InitFont(cv.CV_FONT_HERSHEY_COMPLEX_SMALL,0.7,0.7,thickness=1)
		cv.PutText(img_cont, "Contour", (10,50) , font, (255,0,0))
		cv.PutText(img_cont, "Bounding Rectangle", (10,70) , font, (0,255,0))
		cv.PutText(img_cont, "Fitted Line", (10,90) , font, (0,0,255))
		cv.PutText(img_cont, "Reference Line", (10,110) , font, (0,140,255))

		
		cv.ShowImage("Geometry Magic",img_cont)
		Logger.addImage(img_cont, "Geometry")

		
		return angle
		
		