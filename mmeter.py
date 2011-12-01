import Image

import cv




class Mmeter:
	
	def __init__(self):
		img = cv.LoadImage("img/4.jpg")
		
		openimg=self.fg_disc(img)

		cv.ShowImage("opened img", openimg)
		#cv.MoveWindow("opened img", 20,20)
		
		skeletor=self.skeletonization(openimg)
		cv.ShowImage("skelett",skeletor)
		

		
		while cv.WaitKey(10)!=27:
			x=1	
			
			
			
		
	def skeleletonization(self, image):
		img = cv.CreateMat (image.height, image.width, cv.CV_8UC1)
		cv.Copy(image, img)
		skel = cv.CreateMat(img.height, img.width, cv.CV_8UC1)	
		eroded = cv.CreateMat(img.height, img.width, cv.CV_8UC1)
		tmp = cv.CreateMat(img.height, img.width, cv.CV_8UC1)
		element = cv.CreateStructuringElementEx(3,3,1,1,cv.CV_SHAPE_CROSS)
		done=False
		while (done==False):
			cv.Erode(img, eroded, element)
			cv.Dilate(eroded, tmp, element)
			cv.Sub(img, tmp, tmp)
			cv.Or(skel, tmp, skel)
			cv.Copy(eroded, img)	
			done = (cv.Norm(img, None)==0)

		
		return skel
		
		

	
	#foreground/background discrimination		
	def fg_disc(self, image):
		img_hsv= cv.CreateMat(image.height, image.width, cv.CV_8UC3)
		cv.CvtColor(image, img_hsv, cv.CV_BGR2HSV)
		img_tmp = cv.CreateMat(image.height, image.width, cv.CV_8UC3)
		img_thresh = cv.CreateMat(image.height, image.width, cv.CV_8UC3)

		h_plane=cv.CreateMat(image.height, image.width, cv.CV_8UC1)
		s_plane=cv.CreateMat(image.height, image.width, cv.CV_8UC1)
		v_plane=cv.CreateMat(image.height, image.width, cv.CV_8UC1)
		cv.Split(img_hsv, h_plane, s_plane, v_plane, None)

		cv.Threshold(h_plane, h_plane, 18.0, 255.0 , cv.CV_THRESH_BINARY_INV)
		cv.Threshold(s_plane, s_plane, 50.0, 255.0 , cv.CV_THRESH_BINARY)
		cv.Threshold(v_plane, v_plane, 80.0, 255.0 , cv.CV_THRESH_BINARY)
	
		img_and=cv.CreateMat(image.height, image.width, cv.CV_8UC1)
		cv.And(h_plane, s_plane, img_and)
		cv.And(img_and, v_plane, img_and)
	
	
		kernel5=cv.CreateStructuringElementEx(2,1,1,0, cv.CV_SHAPE_RECT)
		kernell=cv.CreateStructuringElementEx(5,5,2,2, cv.CV_SHAPE_RECT)
		
		cv.Erode(img_and, img_and, iterations=2)	
		cv.Erode(img_and, img_and, iterations=1, element=kernel5)	
		open_img = cv.CreateMat(image.height, image.width, cv.CV_8UC1)
		cv.MorphologyEx(img_and,open_img, img_tmp, kernell, cv.CV_MOP_CLOSE, 30	)
		
		openimg = open_img
		return openimg
	

	
	
if __name__ == "__main__":
	mm = Mmeter()
	
