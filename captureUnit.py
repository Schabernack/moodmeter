import cv
import numpy as np

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
			# do forever
		 
			# capture the current frame
			frame = cv.QueryFrame(capture)
			if frame is None:
				break
						
			pt1 = (frame.width/2-30,frame.height/2-30)
			pt2 = (pt1[0]+60,pt1[1]+60)
			color = (0,0,255)
			cv.Rectangle(frame, pt1,pt2 , color,thickness=2)
		
		
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
				break
				
		## Image Processing
		roi = (pt1[0],pt1[1],60,60)
		image_roi = cv.GetSubRect(image,roi)
		
		filter = self.getSkinColor(image_roi)
		img_out = self.filterImage(frame,filter)
		cv.ShowImage('Filtered', img_out)			

		while 1:		
			k = cv.WaitKey(10)

			if k == 0x1b: # ESC
				print 'ESC pressed. Exiting ...'
				break
		
		
	## toDo: remove extreme values
	def getSkinColor(self,img):
		img_skin = cv.CreateMat(img.height, img.width, cv.CV_8UC3)
		cv.CvtColor(img,img_skin,cv.CV_BGR2HSV)

		mean = cv.Avg(img_skin)
		
		return (mean[0],mean[1],mean[2])
		
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
	
		cv.Threshold(h_plane, h_plane, filter[0]+0.2*filter[0], 255.0 , cv.CV_THRESH_BINARY_INV)
		cv.Threshold(s_plane, s_plane, filter[1]-0.2*filter[1], 255.0 , cv.CV_THRESH_BINARY)
		cv.Threshold(v_plane, v_plane, filter[2]-0.2*filter[2], 255.0 , cv.CV_THRESH_BINARY)
				
		img_and=cv.CreateMat(image.height, image.width, cv.CV_8UC1)
		cv.And(h_plane, s_plane, img_and)
		cv.And(img_and, v_plane, img_and)
		
		return img_and

		
				
if __name__ == "__main__":
	cu = CaptureUnit()
	cu.run()
	

	
	
	
	
	
	