import cv

class MatchingUnit:

	def __init__(self):
		self.tempDir = "templates/"
		self.tempList = ("0.png","22.png","45.png","67.png","90.png","112.png","135.png","157.png","180.png")
	
	def getBestMatch(self,img):
		match = dict()
		for temp in self.tempList:
			template = cv.LoadImage(self.tempDir+temp,0)

			result = cv.CreateMat(img.height-template.height+1, img.width-template.width+1, cv.CV_32FC1)

			cv.MatchTemplate(img,template,result,cv.CV_TM_SQDIFF)
			match[cv.MinMaxLoc(result)[0]] = temp
			print temp, cv.MinMaxLoc(result)[0]
		res = match[min(match.keys())]
	    
		return res
		


