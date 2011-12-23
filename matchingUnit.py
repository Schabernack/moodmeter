import cv
import math

class MatchingUnit:

	def __init__(self):
		self.tempDir = "templates2/"
		#self.tempList = ("0.png","22.png","45.png","67.png","90.png","112.png","135.png","157.png","180.png")
		self.tempList = ("0.png","45.png","90.png","135.png","180.png")

		test = cv.LoadImage(self.tempDir+"180.png",0)

		#self.test(test)
		
	def getBestMatch2(self,img):
		match = dict()
		cv.ShowImage("test",img)
		for temp in self.tempList:
			template = cv.LoadImage(self.tempDir+temp,0)
			template = self.scaleTemplate(img,template,temp)
			result = cv.CreateMat(img.height-template.height+1, img.width-template.width+1, cv.CV_32FC1)
			#print template.width,template.height
			cv.MatchTemplate(img,template,result,cv.CV_TM_CCOEFF)
			match[cv.MinMaxLoc(result)[0]] = temp

			print temp, cv.MinMaxLoc(result)[0]

		res = match[max(match.keys())]
		print res
	    
		return res
		
	def getBestMatch(self,img):
		match = dict()
		tmp = cv.CreateMat(img.height,img.width,cv.CV_8UC1)
		cv.Copy(img,tmp)
		contour_img = cv.FindContours(tmp,cv.CreateMemStorage(),mode=cv.CV_RETR_EXTERNAL,method=cv.CV_CHAIN_APPROX_NONE)

		cv.ShowImage("test",img)
		for temp in self.tempList:
			template = cv.LoadImage(self.tempDir+temp,0)
			template = self.scaleTemplate(img,template,temp)
			contour_tmp = cv.FindContours(template,cv.CreateMemStorage(),mode=cv.CV_RETR_EXTERNAL,method=cv.CV_CHAIN_APPROX_NONE)

			result = cv.MatchShapes(contour_img,contour_tmp,method=cv.CV_CONTOURS_MATCH_I3)
			match[result] = temp

			print temp, result

		res = match[min(match.keys())]
		print res
	    
		return res
		
	def scaleTemplate(self,img,temp,title):		
		contour = cv.FindContours(img,cv.CreateMemStorage(),mode=cv.CV_RETR_EXTERNAL,method=cv.CV_CHAIN_APPROX_NONE)
		rect = cv.BoundingRect(contour)
			
		temp_ratio = temp.width/temp.height
		img_ratio = img.width/img.height
		
		print "rect",rect[2],rect[3]

		if (temp_ratio > 0 and img_ratio > 0 or temp_ratio < 0 and img_ratio < 0):
			if rect[2] < rect[3]:
				scale = float(rect[2])/float(temp.width)
			else: 
				scale = float(rect[3])/float(temp.height)
		elif (temp_ratio > 0 and img_ratio < 0):
			scale = float(rect[2])/float(temp.width) 	
		else: 
			scale = float(rect[3])/float(temp.height)
		
		#print title,temp.width,temp.height
		#print title,scale
		template = self.scaleImage(temp,scale)
		#print title,template.width,template.height
		cv.ShowImage(title,template)
		return template
		
	def scaleImage(self,img,factor):
		destination = cv.CreateMat(int(img.height*factor),int(img.width*factor),cv.CV_8UC1)
		cv.Resize(img,destination)
		return destination
		
		
	def test(self,img):		
		match = dict()

		for temp in self.tempList:
			template = cv.LoadImage(self.tempDir+temp,0)
			#template = self.scaleTemplate(img,template,temp)
			result = cv.CreateMat(img.height-template.height+1, img.width-template.width+1, cv.CV_32FC1)
			cv.MatchTemplate(img,template,result,cv.CV_TM_SQDIFF_NORM)
			match[cv.MinMaxLoc(result)[0]] = temp
			print temp, cv.MinMaxLoc(result)[0]
		res = match[min(match.keys())]
		print res
