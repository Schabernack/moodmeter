import Image;
import cv;
 
class Mmeter:

	#returns new, opened image
	def morph_open(image, it=1):
		img=cv.CreateMat(img.height, img.width, cv.CV_8UC1)
		cv.Dilate(image, img, iterations=it)		
		cv.Erode(img, img, iterations=it)
		img
		
	#returns new, closed image
	def morph_close(image, it=1):
		img=cv.CreateMat(img.height, img.width, cv.CV_8UC1)
		cv.Erode(img, img, iterations=it)
		cv.Dilate(image, img, iterations=it)		
		img
	
	def __init__(self):
		run()
	
	def run():

		img = cv.LoadImage("img/1.jpg")
		img_hsv= cv.CreateMat(img.height, img.width, cv.CV_8UC3)
		cv.CvtColor(img, img_hsv, cv.CV_BGR2HSV)
		img_tmp = cv.CreateMat(img.height, img.width, cv.CV_8UC3)
		img_thresh = cv.CreateMat(img.height, img.width, cv.CV_8UC3)

		h_plane=cv.CreateMat(img.height, img.width, cv.CV_8UC1)
		s_plane=cv.CreateMat(img.height, img.width, cv.CV_8UC1)
		v_plane=cv.CreateMat(img.height, img.width, cv.CV_8UC1)
		cv.Split(img_hsv, h_plane, s_plane, v_plane, None)

		cv.Threshold(h_plane, h_plane, 18.0, 255.0 , cv.CV_THRESH_BINARY_INV)
		cv.Threshold(s_plane, s_plane, 50.0, 255.0 , cv.CV_THRESH_BINARY)
		cv.Threshold(v_plane, v_plane, 80.0, 255.0 , cv.CV_THRESH_BINARY)
		
		img_and=cv.CreateMat(img.height, img.width, cv.CV_8UC1)
		cv.And(h_plane, s_plane, img_and)
		cv.And(img_and, v_plane, img_and)
		
		
		openimg=morph_open(img_and)		
		closeimg=morph_close(img_and)
		closeopenimg=morph_close(openimg)


		#cv.ShowImage("win1", img)
		#cv.ShowImage("hue", h_plane)
		#cv.ShowImage("saturation", s_plane)
		#cv.ShowImage("value", v_plane)
		#cv.ShowImage("win4", img_thresh)
		
		cv.ShowImage("opened img", openimg)
		cv.ShowImage("closed image", closeimg)
		cv.ShowImage("opened then closed", closeopenimg)

		

		while cv.WaitKey(10)!=27:
			x=1	

	
	
if __name__ == "__main__":
	mm = Mmeter()
	
