import cv
import numpy as np

test = False

class CaptureUnit:
	
	def run(self):
		# create capture device
		device = 0 # assume we want first device
		capture = cv.CreateCameraCapture(0)
		
		# check if capture device is OK
		if not capture:
			print "Error opening capture device"
			sys.exit(1)
		 
		## Video processing
		while 1: 		 
			# capture the current frame
			frame = cv.QueryFrame(capture)
			if frame is None:
				break
						
			pt1 = (frame.width/2-30,frame.height/2-30)
			pt2 = (pt1[0]+60,pt1[1]+60)
			color = (0,0,255)
			cv.Rectangle(frame, pt1,pt2 , color,thickness=2)
		
			cv.Flip(frame,None,1)
		
			# display webcam image
			cv.ShowImage('Camera', frame)
			# handle events
			k = cv.WaitKey(10)
		 
			if k == 0x1b: # ESC
				print 'ESC pressed. Exiting ...'
				break
			elif k == 0x20: # Enter
				print 'Enter pressed. Image taken'
				image = cv.QueryFrame(capture)
				cv.Flip(image,None,1)

				break
				
		## Image Processing
		roi = (pt1[0],pt1[1],60,60)
		image_roi = cv.GetSubRect(image,roi)
		
		img_hsv = cv.CreateMat(frame.height,frame.width,cv.CV_8UC3)

		cv.CvtColor(image,img_hsv,cv.CV_BGR2HSV)
		cv.ShowImage("HSV",img_hsv)
		
		hist = self.hs_histogram(image_roi)

		img_skin = self.applyModelToImage(image,hist,"ROI Proj",pt1)

		img_out = self.fillHand(img_skin,pt1)
		cv.ShowImage('Output', img_out)			

		while 1:		
			k = cv.WaitKey(10)

			if k == 0x1b: # ESC
				print 'ESC pressed. Exiting ...'
				break

		
	def test(self):
		frame = cv.LoadImageM("img/test2.jpg",cv.CV_LOAD_IMAGE_UNCHANGED)
		image = cv.CreateMat(frame.height,frame.width,cv.CV_8UC3)
		img_hsv = cv.CreateMat(frame.height,frame.width,cv.CV_8UC3)

		cv.Copy(frame,image)
		
		pt1 = (frame.width/2,frame.height/2-30)
		pt2 = (pt1[0]+60,pt1[1]+60)
		color = (0,0,255)
		cv.Rectangle(frame, pt1,pt2 , color,thickness=2)
		
		cv.ShowImage('Frame', frame)
		
		## Image Processing
		roi = (pt1[0],pt1[1],60,60)
		image_roi = cv.GetSubRect(image,roi)
		
		cv.CvtColor(image,img_hsv,cv.CV_BGR2HSV)
		cv.ShowImage("HSV",img_hsv)
		
		hist = self.hs_histogram(image_roi)

		img_skin = self.applyModelToImage(image,hist,"ROI Proj",pt1)

		img_out = self.fillHand(img_skin,pt1)
		cv.ShowImage('Output', img_out)			

		while 1:		
			k = cv.WaitKey(10)

			if k == 0x1b: # ESC
				print 'ESC pressed. Exiting ...'
				break
		
		
	def applyModelToImage(self,img,model,title,point):
		img_hsv = cv.CreateMat(img.height, img.width, cv.CV_8UC3)
		img_out = cv.CreateMat(img.height, img.width, cv.CV_8UC1)
		img_bin = cv.CreateMat(img.height, img.width, cv.CV_8UC1)
		img_fill = cv.CreateMat(img.height, img.width, cv.CV_8UC1)

		cv.CvtColor(img,img_hsv,cv.CV_BGR2HSV)

		h_plane=cv.CreateMat(img.height, img.width, cv.CV_8UC1)
		s_plane=cv.CreateMat(img.height, img.width, cv.CV_8UC1)
		
		cv.Split(img_hsv, h_plane, s_plane,None, None)
		planes = [h_plane,s_plane]

		cv.CalcBackProject([cv.GetImage(i) for i in planes],img_out,model)
		
		cv.ShowImage(title,img_out)
		cv.Threshold(img_out, img_bin, 100, 255.0 , cv.CV_THRESH_BINARY)
		cv.ShowImage("Binary",img_bin)
		
		cv.Copy(img_bin,img_fill)
		

		cv.FloodFill(img_fill,point,(120))
		
		
		cv.Threshold(img_fill, img_fill, 130, 255.0 , cv.CV_THRESH_TOZERO_INV)
		cv.Threshold(img_fill, img_fill, 100, 255.0 , cv.CV_THRESH_BINARY)
	
		cv.ShowImage("Flooded Bin",img_fill)

		
		return img_bin
				
	def fillHand(self,img,point):
		img_tmp = cv.CreateMat(img.height, img.width, cv.CV_8UC1)
		img_fill = cv.CreateMat(img.height, img.width, cv.CV_8UC1)
		kernel5=cv.CreateStructuringElementEx(2,1,1,0, cv.CV_SHAPE_RECT)
		kernell=cv.CreateStructuringElementEx(3,3,1,1, cv.CV_SHAPE_RECT)
	 
		open_img = cv.CreateMat(img.height, img.width, cv.CV_8UC1)
		cv.MorphologyEx(img,open_img, img_tmp, kernell, cv.CV_MOP_CLOSE, 1 )
		cv.ShowImage("Opened",open_img)
		cv.Copy(open_img,img_fill)
				
		cv.FloodFill(img_fill,point,(120))
		
		cv.ShowImage("Flooded",img_fill)
		
		cv.Threshold(img_fill, img_fill, 130, 255.0 , cv.CV_THRESH_TOZERO_INV)
		cv.Threshold(img_fill, img_fill, 100, 255.0 , cv.CV_THRESH_BINARY)
		
		return img_fill
	
	
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
	
		for h in range(h_bins):
			for s in range(s_bins):
				bin_val = cv.QueryHistValue_2D(hist, h, s)
				intensity = cv.Round(bin_val * 255 / max_value)
				cv.Rectangle(hist_img,
							 (h*scale, s*scale),
							 ((h+1)*scale - 1, (s+1)*scale - 1),
							 cv.RGB(intensity, intensity, intensity), 
							 cv.CV_FILLED)
		return hist
	
	
if __name__ == "__main__":
	cu = CaptureUnit()
	if test:
		cu.test()
	else:
		cu.run()	
	
	
	
	