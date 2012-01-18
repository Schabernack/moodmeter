import cv
import numpy as np
from matchingUnit import MatchingUnit
from logger import Logger
from pictureviewer import Pictureviewer as pv

test = False

class ProcessUnit:
	
	
	## returns completely processed image
	## ideally this is just the white silhouette of the hand on a black sheet
	def processImage(self, image):
		
		pt1 = (image.width/2,image.height/2-30)
	   	pt2 = (pt1[0]+60,pt1[1]+60)
		
		roi = (pt1[0],pt1[1],60,60)
		image_roi = cv.GetSubRect(image,roi)
		
		hist = self.hs_histogram(image_roi)

		img_skin = self.applyModelToImage(image,hist,pt1)
		img_out = self.fillHand(img_skin,pt1)		
		

		return img_out
		
	## Calculate Skin probability with hist model
	def applyModelToImage(self,img,model,point):
		img_hsv = cv.CreateMat(img.height, img.width, cv.CV_8UC3)
		img_out = cv.CreateMat(img.height, img.width, cv.CV_8UC1)
		img_bin = cv.CreateMat(img.height, img.width, cv.CV_8UC1)
		img_ero = cv.CreateMat(img.height, img.width, cv.CV_8UC1)
		img_fill = cv.CreateMat(img.height, img.width, cv.CV_8UC1)
		img_smooth = cv.CreateMat(img.height, img.width, cv.CV_8UC1)

		cv.CvtColor(img,img_hsv,cv.CV_BGR2HSV)
		Logger.addImage(img_hsv, "img_hsv")
		pv.addColor(img_hsv,"hsv")
		
		h_plane=cv.CreateMat(img.height, img.width, cv.CV_8UC1)
		s_plane=cv.CreateMat(img.height, img.width, cv.CV_8UC1)
		
		cv.Split(img_hsv, h_plane, s_plane, None, None)
		planes = [h_plane, s_plane]

		cv.CalcBackProject([cv.GetImage(i) for i in planes],img_out,model)
				
		cv.Threshold(img_out, img_bin, 10, 255.0 , cv.CV_THRESH_BINARY)
		Logger.addImage(img_bin, "img_binary")
		pv.addBinary(img_bin,"binary")
		cv.Erode(img_bin,img_ero,iterations=2)
		Logger.addImage(img_ero, "img_eroded")

		cv.Smooth(img_ero,img_smooth,smoothtype=cv.CV_MEDIAN,param1=7)
		Logger.addImage(img_smooth, "img_median")
		pv.addBinary(img_smooth,"median")

		return img_smooth
			
		
	## Floodfill img from starting point	
	def fillHand(self,img,point):
		img_tmp = cv.CreateMat(img.height, img.width, cv.CV_8UC1)
		img_fill = cv.CreateMat(img.height, img.width, cv.CV_8UC1)
		kernell=cv.CreateStructuringElementEx(7,7,3,3, cv.CV_SHAPE_RECT)
	 
		img_open = cv.CreateMat(img.height, img.width, cv.CV_8UC1)
		cv.MorphologyEx(img,img_open, img_tmp, kernell, cv.CV_MOP_CLOSE, 2 )
		
		Logger.addImage(img_open, "img_opened")
		pv.addBinary(img_open,"opened")

		cv.Copy(img_open,img_fill)
				
		cv.FloodFill(img_fill,point,(120))
		Logger.addImage(img_fill, "img_filled")

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
		
			
	