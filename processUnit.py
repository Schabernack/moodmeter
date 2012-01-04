import cv
import numpy as np
from matchingUnit import MatchingUnit

test = False

class ProcessUnit:
	
	def run(self):

				
		## Image Processing
		roi = (pt1[0],pt1[1],60,60)
		image_roi = cv.GetSubRect(image,roi)
		
		img_hsv = cv.CreateMat(frame.height,frame.width,cv.CV_8UC3)

		cv.CvtColor(image,img_hsv,cv.CV_BGR2HSV)
		#cv.ShowImage("HSV",img_hsv)
		
		hist = self.hs_histogram(image_roi)

		img_skin = self.applyModelToImage(image,hist,pt1)

		img_out = self.fillHand(img_skin,pt1)
		#cv.ShowImage('Output', img_out)			
				
		return img_out

	## Test Modus (load image instead of webcam

	## returns completely processed image
	## ideally this is just the white silhouette of the hand on a black sheet
	def processImage(self, image):
		
		pt1 = (image.width/2,image.height/2-30)
	   	pt2 = (pt1[0]+60,pt1[1]+60)
		
		roi = (pt1[0],pt1[1],60,60)
		image_roi = cv.GetSubRect(image,roi)
		
		img_hsv = cv.CreateMat(image.height,image.width,cv.CV_8UC3)
		
		#cv.ShowImage("bgr", image)		
		cv.CvtColor(image,img_hsv,cv.CV_BGR2HSV)

		cv.ShowImage("HSV",img_hsv)
		

		hist = self.hs_histogram(image_roi)

		img_skin = self.applyModelToImage(image,hist,pt1)

		img_out = self.fillHand(img_skin,pt1)
		#cv.ShowImage('Output', img_out)			
				
		return img_out


	def test(self):
		
		## Image Processing
		roi = (pt1[0],pt1[1],60,60)
		image_roi = cv.GetSubRect(image,roi)
		
		cv.CvtColor(image,img_hsv,cv.CV_BGR2HSV)
		#cv.ShowImage("HSV",img_hsv)
	
		hist = self.hs_histogram(image_roi)

		img_skin = self.applyModelToImage(image,hist,pt1)

		img_out = self.fillHand(img_skin,pt1)
		#cv.ShowImage('Output', img_out)			
		return img_out
		
	## Calculate Skin probability with hist model
	def applyModelToImage(self,img,model,point):
		img_hsv = cv.CreateMat(img.height, img.width, cv.CV_8UC3)
		img_out = cv.CreateMat(img.height, img.width, cv.CV_8UC1)
		img_bin = cv.CreateMat(img.height, img.width, cv.CV_8UC1)
		img_fill = cv.CreateMat(img.height, img.width, cv.CV_8UC1)
		img_smooth = cv.CreateMat(img.height, img.width, cv.CV_8UC1)

		cv.CvtColor(img,img_hsv,cv.CV_BGR2HSV)

		h_plane=cv.CreateMat(img.height, img.width, cv.CV_8UC1)
		s_plane=cv.CreateMat(img.height, img.width, cv.CV_8UC1)
		
		cv.Split(img_hsv, h_plane, s_plane,None, None)
		planes = [h_plane,s_plane]

		cv.CalcBackProject([cv.GetImage(i) for i in planes],img_out,model)
				
		cv.Threshold(img_out, img_bin, 10, 255.0 , cv.CV_THRESH_BINARY)
		cv.ShowImage("Binary",img_bin)
		
		cv.Erode(img_bin,img_bin,iterations=2)
		
		cv.Smooth(img_bin,img_smooth,smoothtype=cv.CV_MEDIAN,param1=7)
		cv.ShowImage("Median Filter Binary",img_smooth)
		
		return img_smooth
			
		
	## Floodfill img from starting point	
	def fillHand(self,img,point):
		img_tmp = cv.CreateMat(img.height, img.width, cv.CV_8UC1)
		img_fill = cv.CreateMat(img.height, img.width, cv.CV_8UC1)
		kernell=cv.CreateStructuringElementEx(7,7,3,3, cv.CV_SHAPE_RECT)
	 
		open_img = cv.CreateMat(img.height, img.width, cv.CV_8UC1)
		cv.MorphologyEx(img,open_img, img_tmp, kernell, cv.CV_MOP_CLOSE, 2 )
		#cv.ShowImage("Opened",open_img)
		cv.Copy(open_img,img_fill)
				
		cv.FloodFill(img_fill,point,(120))
		
		cv.ShowImage("Flooded",img_fill)
		
		cv.Threshold(img_fill, img_fill, 130, 255.0 , cv.CV_THRESH_TOZERO_INV)
		cv.Threshold(img_fill, img_fill, 100, 255.0 , cv.CV_THRESH_BINARY)
		
		return img_fill
	
	## Calculate Hue/Saturation Histogram for src image. src image is bgr
	def hs_histogram(self,src):
		# Convert to HSV
		hsv = cv.CreateImage(cv.GetSize(src), 8, 3)
		cv.CvtColor(src, hsv, cv.CV_BGR2HSV)
	
		# Extract the H and S planes
		h_plane = cv.CreateMat(src.rows, src.cols, cv.CV_8UC1)
		s_plane = cv.CreateMat(src.rows, src.cols, cv.CV_8UC1)
		cv.Split(hsv, h_plane, s_plane, None, None)
		planes = [h_plane, s_plane]
	
		h_bins = 15
		s_bins = 16
		hist_size = [h_bins, s_bins]
		# hue varies from 0 (~0 deg red) to 180 (~360 deg red again */
		h_ranges = [0, 180]
		# saturation varies from 0 (black-gray-white) to
		# 255 (pure spectrum color)
		s_ranges = [0, 255]
		ranges = [h_ranges, s_ranges]
		scale = 10
		hist = cv.CreateHist([h_bins, s_bins], cv.CV_HIST_ARRAY, ranges, 1)
		cv.CalcHist([cv.GetImage(i) for i in planes], hist)
		(_, max_value, _, _) = cv.GetMinMaxHistValue(hist)
	
		hist_img = cv.CreateImage((h_bins*scale, s_bins*scale), 8, 3)

		return hist
			
	
if __name__ == "__main__":
	cu = CaptureUnit()
	mu = MatchingUnit()
	img = cu.run()
	result = mu.getBestMatch(img)
	
	print "Angle\t",result	
	
	while 1:		
		k = cv.WaitKey(10)

		if k == 0x1b: # ESC
			print 'ESC pressed. Exiting ...'
			break

	