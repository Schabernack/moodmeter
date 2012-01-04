import cv
import math

class MatchingUnit:

	def __init__(self):
		self.tempDir = "templates2/"
		#self.tempList = ("0.png","22.png","45.png","67.png","90.png","112.png","135.png","157.png","180.png")
		self.tempList = ("0.png","45.png","90.png","135.png","180.png")
		
	def testRect(self,image):
		img_ipl = cv.GetImage(image)
		vertical,upper,lower = self.getRectangles(image)
		
		cv.SetImageROI(img_ipl,upper)
		upMat = cv.GetMat(img_ipl)
		upCount = cv.CountNonZero(upMat)

		cv.SetImageROI(img_ipl,lower)
		lowMat = cv.GetMat(img_ipl)
		lowCount = cv.CountNonZero(lowMat)
		
		print upCount,lowCount
		
		if vertical:
			if upCount<lowCount:
				print "UP"
			else:
				print "DOWN"
		else:
			if upCount<lowCount:
				print "LEFT"
			else:
				print "RIGHT"

	
	def getRectangles(self,image):		
		cont = cv.FindContours(image,cv.CreateMemStorage(),mode=cv.CV_RETR_EXTERNAL,method=cv.CV_CHAIN_APPROX_NONE)
		x,y,width,height = cv.BoundingRect(cont)
		
		if height >= width:
			upper = (x,y,x+width,y+int(height/2))
			lower = (x,y+int(height/2),x+width,y+height)
			vertical = True
		else:
			upper = (x,y,x+int(width/2),y+height)
			lower = (x+int(width/2),y,x+width,y+height)
			vertical = False
		
		return vertical, upper, lower	
		