import Image

import cv




class Mmeter:
	
	def __init__(self):
		img = cv.LoadImage("img/2.jpg")
		
		openimg=self.fg_disc(img)

		cv.ShowImage("opened img", openimg)
		cv.MoveWindow("opened img", 20,20)
		
		skeletor=self.skeletonization(openimg)
		cv.ShowImage("skelett",skeletor)
		
		while cv.WaitKey(10)!=27:
			x=1	
			
			
			
	def skeletonization(self, image):
		skel = cv.CreateMat(image.height, image.width, cv.CV_8UC1)
		cv.Rectangle(skel, (0,0), (image.height, image.width), (0), cv.CV_FILLED, )
		tmp = cv.CreateMat(image.height, image.width, cv.CV_8UC1)
		cross_kernel = cv.CreateStructuringElementEx(3,3,1,1, cv.CV_SHAPE_CROSS)
		
		while True:
			cv.MorphologyEx(image, tmp, tmp, operation=cv.CV_MOP_OPEN, element=cross_kernel)
			cv.Not(tmp, tmp)
			cv.And(image, tmp, tmp)
			cv.Or(skel, tmp, skel)
			cv.Erode(image, image, cross_kernel)
			max=cv.MinMaxLoc(image)[1]			
			
			#erode until no white pixel in image is left
			if max==0:
				break
		
		opened = cv.CreateMat(image.height, image.width, cv.CV_8UC1)
		closed = cv.CreateMat(image.height, image.width, cv.CV_8UC1)
		
		#cv.MorphologyEx(skel, opened, tmp, operation=cv.CV_MOP_OPEN, element=cv.CreateStructuringElementEx(3,3,1,1,cv.CV_SHAPE_RECT))
		#cv.MorphologyEx(skel, closed, tmp, operation=cv.CV_MOP_CLOSE, element=cv.CreateStructuringElementEx(3,3,1,1,cv.CV_SHAPE_RECT))
		
		
		
		cv.ShowImage("opened", opened)
		cv.ShowImage("closed", closed)
		
		return skel
		
	
	#returns new, opened image
	def morph_open(self, image, it=1, kernel=None):	
		img=cv.CreateMat(image.height, image.width, cv.CV_8UC1)
		cv.Erode(img, img, kernel, it)
		cv.Dilate(image, img, kernel , it)		
		return img
		
	#returns new, closed image
	def morph_close(self, image, it=1, kernel=None):
		img=cv.CreateMat(image.height, image.width, cv.CV_8UC1)
		cv.Dilate(image, img, kernel, it)		
		cv.Erode(img, img, kernel,  it)
		return img
	
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
		openimg=self.morph_close(img_and, 30, kernel=kernell)
		
		return openimg
	

	
	
if __name__ == "__main__":
	mm = Mmeter()
	
