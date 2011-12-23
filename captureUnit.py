import cv
import numpy as np

test = True

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
		
		filter = self.getSkinColor(image_roi)
		#model = self.getSkinColorModel(image_roi)
		
		#self.applyModelToFrame(frame,model)
		
		img_out = self.filterImage(image,filter)
		cv.ShowImage('Output before', img_out)			

		img_out = self.fillHand(img_out,pt1)
		cv.ShowImage('Output after', img_out)			

		while 1:		
			k = cv.WaitKey(10)

			if k == 0x1b: # ESC
				print 'ESC pressed. Exiting ...'
				break
		
		return img_out
		
	def test(self):
		frame = cv.LoadImageM("img/1.jpg",cv.CV_LOAD_IMAGE_UNCHANGED)
		image = cv.CreateMat(frame.height,frame.width,cv.CV_8UC3)
		cv.Copy(frame,image)
		
		pt1 = (frame.width/2-60,frame.height/2+30)
		pt2 = (pt1[0]+60,pt1[1]+60)
		color = (0,0,255)
		cv.Rectangle(frame, pt1,pt2 , color,thickness=2)
		
		cv.ShowImage('Frame', frame)
		
		## Image Processing
		roi = (pt1[0],pt1[1],60,60)
		image_roi = cv.GetSubRect(image,roi)
		
		filter = self.getSkinColor(image_roi)
		#model = self.getSkinColorModel(image_roi)
		
		#self.applyModelToFrame(frame,model)
		
		img_out = self.filterImage(image,filter)
		cv.ShowImage('Output before', img_out)			

		img_out = self.fillHand(img_out,pt1)
		cv.ShowImage('Output after', img_out)			

		while 1:		
			k = cv.WaitKey(10)

			if k == 0x1b: # ESC
				print 'ESC pressed. Exiting ...'
				break
		
		return img_out

		
		
	## toDo: remove extreme values
	def getSkinColor(self,img):
		img_skin = cv.CreateMat(img.height, img.width, cv.CV_8UC3)
		cv.CvtColor(img,img_skin,cv.CV_BGR2HSV)
		mean = cv.Avg(img_skin)
		
		return (mean[0],mean[1],mean[2])
	
	def getSkinColorModel(self,img):
		img_skin = cv.CreateMat(img.height, img.width, cv.CV_8UC3)
		cv.CvtColor(img,img_skin,cv.CV_BGR2HSV)
		# Extract the H and S planes
			
		h_bins = 181
		s_bins = 256
		hist_size = [h_bins, s_bins]
		# hue varies from 0 (~0 deg red) to 180 (~360 deg red again */
		h_ranges = [0, 180]
		# saturation varies from 0 (black-gray-white) to
		# 255 (pure spectrum color)
		s_ranges = [0, 255]
		ranges = [h_ranges, s_ranges]
		hist = cv.CreateHist((181,256,256), cv.CV_HIST_ARRAY, [(0,180),(0,255),(0,255)], 1)
		cv.CalcHist([cv.GetImage(img_skin)], hist)		
		
		return hist
		
	def applyModelToFrame(self,img,model):
		img_skin = cv.CreateMat(img.height, img.width, cv.CV_8UC1)
		
		h_plane = cv.CreateMat(img_skin.rows, img_skin.cols, cv.CV_8UC1)
		s_plane = cv.CreateMat(img_skin.rows, img_skin.cols, cv.CV_8UC1)
		
		planes = [h_plane,s_plane]
		
		cv.Split(img,h_plane,s_plane,None,None)
		
		cv.CalcBackProject([cv.GetImage(i) for i in planes],img_skin,model)
		
		cv.ShowImage("backprof",img_skin)
				
		
	def filterImage(self,image,filter):
		img_skin = cv.CreateMat(image.height, image.width, cv.CV_8UC3)
		img_tmp = cv.CreateMat(image.height, image.width, cv.CV_8UC3)
		img_hsv = cv.CreateMat(image.height, image.width, cv.CV_8UC3)
		
		cv.CvtColor(image,img_hsv,cv.CV_BGR2HSV)
		cv.Set(img_skin,filter)
		
		img_out = cv.CreateMat(image.height, image.width, cv.CV_8UC3)
		cv.AbsDiff(img_skin,image,img_tmp)
		
		h_plane=cv.CreateMat(image.height, image.width, cv.CV_8UC1)
		s_plane=cv.CreateMat(image.height, image.width, cv.CV_8UC1)
		v_plane=cv.CreateMat(image.height, image.width, cv.CV_8UC1)
		cv.Split(img_hsv, h_plane, s_plane, v_plane, None)
	
	
		#### Rahmen um den template wert statt einfachen threshhold
		
		### Scaling?!?
		
		### Smoothing?!?
	
		cv.Threshold(h_plane, h_plane, filter[0]+0.2*filter[0], 255.0 , cv.CV_THRESH_BINARY_INV)
		cv.Threshold(s_plane, s_plane, filter[1]-0.3*filter[1], 255.0 , cv.CV_THRESH_BINARY)
		cv.Threshold(v_plane, v_plane, filter[2]-0.5*filter[2], 255.0 , cv.CV_THRESH_BINARY)
				
		img_and=cv.CreateMat(image.height, image.width, cv.CV_8UC1)
		cv.And(h_plane, s_plane, img_and)
		cv.And(img_and, v_plane, img_and)
		
		return img_and
		
	def fillHand(self,img,point):
		img_tmp = cv.CreateMat(img.height, img.width, cv.CV_8UC1)
		img_fill = cv.CreateMat(img.height, img.width, cv.CV_8UC1)
		kernel5=cv.CreateStructuringElementEx(2,1,1,0, cv.CV_SHAPE_RECT)
		kernell=cv.CreateStructuringElementEx(5,5,2,2, cv.CV_SHAPE_RECT)
	 
		open_img = cv.CreateMat(img.height, img.width, cv.CV_8UC1)
		cv.MorphologyEx(img,open_img, img_tmp, kernell, cv.CV_MOP_CLOSE, 1 )
		
		cv.Copy(open_img,img_fill)
				
		cv.FloodFill(img_fill,point,(120))
		
		cv.Threshold(img_fill, img_fill, 130, 255.0 , cv.CV_THRESH_TOZERO_INV)
		cv.Threshold(img_fill, img_fill, 100, 255.0 , cv.CV_THRESH_BINARY)
		
		cv.ShowImage("Filled",img_fill)

		return open_img
	
				
if __name__ == "__main__":
	cu = CaptureUnit()
	if test:
		cu.test()
	else:
		cu.run()	
	
	
	
	