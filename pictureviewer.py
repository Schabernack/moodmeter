import cv

class	Pictureviewer:
	
	__piclist = {}

	@staticmethod
	def __addPic(pic,name):
		Pictureviewer.__piclist[name] = pic

	@staticmethod
	def addColor(pic, name):
		Pictureviewer.__addPic(pic,name)

	@staticmethod
	def addBinary(pic, name):
		img = cv.CreateMat(pic.height,pic.width,cv.CV_8UC3)
		cv.CvtColor(pic,img,cv.CV_GRAY2BGR)
		Pictureviewer.__addPic(img, name)

	
	@staticmethod
	def resizeAll(factor):
		for k,v in Pictureviewer.__piclist.items():
			smallimg = cv.CreateMat(int(v.height*factor),int(v.width*factor),cv.CV_8UC3)
			cv.Resize(v,smallimg, interpolation=cv.CV_INTER_AREA)
			Pictureviewer.__piclist[k]=smallimg



	@staticmethod
	def showPictures():
	#3x2 (w,h) images with same size

		cv.NamedWindow("MoodMeter", cv.CV_WINDOW_AUTOSIZE)

		picwidth = 3 * Pictureviewer.__piclist['hsv'].width
		picheight = 2*Pictureviewer.__piclist['hsv'].height
		DispImg = cv.CreateImage((picwidth +10,  picheight + 10), 8,3)

		img= Pictureviewer.__piclist['hsv']
		cv.SetImageROI(DispImg, (0,0,img.width,img.height))
		cv.Resize(img,DispImg)

		img= Pictureviewer.__piclist['binary']
		cv.SetImageROI(DispImg, (img.width,0,img.width,img.height))
		cv.Resize(img,DispImg)     

		img= Pictureviewer.__piclist['median']
		cv.SetImageROI(DispImg, (2*img.width,0,img.width,img.height))
		cv.Resize(img,DispImg)     

		img= Pictureviewer.__piclist['opened']
		cv.SetImageROI(DispImg, (0,img.height,img.width,img.height))
		cv.Resize(img,DispImg)     

		img= Pictureviewer.__piclist['geometry']
		cv.SetImageROI(DispImg, (img.width,img.height,img.width,img.height))
		cv.Resize(img,DispImg)     

		img= Pictureviewer.__piclist['result']
		cv.SetImageROI(DispImg, (2*img.width,img.height,img.width,img.height))
		cv.Resize(img,DispImg)     

		cv.ResetImageROI(DispImg)

		screen_width = 1280.0
		screen_height = 800.0

		picratio = float(picwidth)/float(picheight)

		if(picratio>0):
			resizeratio = screen_width / picwidth
		else:
			resizeratio = screen_height / picheight

		resized = cv.CreateImage((int(picwidth*resizeratio), int(picheight*resizeratio)), 8,3)
		cv.Resize(DispImg, resized)

		cv.ShowImage("MoodMeter", resized)
	    
	    