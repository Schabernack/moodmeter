import Image
import cv2
import cv
import numpy as np



class Mmeter:
  
  def __init__(self):
    img = cv.LoadImage("img/2.jpg")

    
    tempDir = "templates/"
    tempList = ("0.png","90.png","180.png")

    #trackbar values
    self.distRes = 1
    self.angleRes = 5.0
    self.threshold = 1
    self.minLine = 0
    self.maxGap = 0
  
    self.openimg=self.fg_disc(img)
    self.display = cv.CreateMat(img.height,img.width,cv.CV_8UC1)

    self.skeletor=self.skeleletonization(self.openimg)

    canny = cv.CreateMat(img.height, img.width, cv.CV_8UC1)
    #cv.ShowImage("skel", self.skeletor)
    cv.Canny(self.openimg, canny, 50.0,210.0)
    seq =  cv.FindContours(canny,  cv.CreateMemStorage(), cv.CV_RETR_EXTERNAL, cv.CV_CHAIN_APPROX_NONE)
    #for item in seq:
    #  cv.Circle(img, item, 1, (0,0,255))
    #cv.ShowImage("harris", canny)
    
    moments = cv.Moments(self.openimg, 1)
    m00 = cv.GetSpatialMoment(moments, 0,0)
    m10 = cv.GetSpatialMoment(moments, 1,0)
    m01 = cv.GetSpatialMoment(moments, 0,1)

    point = (int(m10/m00),int(m01/m00))
    cv.Circle(img, point, 2, (255,0,0))
    
    rect = cv.MinAreaRect2(seq)
    print rect
    
    pt = cv.BoxPoints(rect)
    foo = np.array(pt)
    #cv2.polylines(img, foo , isClosed=True, color=np.array(255,0,0))
    cv.EllipseBox(img, rect, (0,255,0))
    
    testbox = (point ,(50,150), 82)
    cv.EllipseBox(img, testbox, (0,0,255))

    cv.ShowImage("bild", img)
    cv.MoveWindow("bild", 20,20)
    
    
    
    for temp in tempList:
    	template = cv.LoadImage(tempDir+temp,0)
    	
    	result = cv.CreateMat(img.height-template.height+1, img.width-template.width+1, cv.CV_32FC1)
    
    	cv.MatchTemplate(self.openimg,template,result,cv.CV_TM_SQDIFF)
    
    	print temp," :\t",cv.MinMaxLoc(result)
    	
    	
    
    #cv.NamedWinow("Hough", 0)    
    #cv.CreateTrackbar("dist","Hough",1,150,self.update_distResolution)
    #cv.CreateTrackbar("angle","Hough",1,6283,self.update_angle)
    #cv.CreateTrackbar("thresh","Hough",1,150,self.update_threshold)
    #cv.CreateTrackbar("minLine","Hough",1,150,self.update_minLine)
    #cv.CreateTrackbar("maxGap","Hough",1,150,self.update_maxGap)

    #self.updateDisplay()    

    while cv.WaitKey(10)!=27:
      x=1 
      
    
    
      
  def update_distResolution(self,val):
    self.distRes=val+1
    print self.distRes
    self.updateDisplay()
  
  def update_angle(self,val):
    self.angleRes=0.00000001+val/1000.0
    self.updateDisplay()

  def update_threshold(self,val):
    self.threshold=val+1
    self.updateDisplay()  

  def update_minLine(self,val):
    self.minLine=val
    self.updateDisplay()

  def update_maxGap(self,val):
    self.maxGap=val
    self.updateDisplay()

  def updateDisplay(self):
    cv.Copy(self.openimg,self.display)  
    foo = cv.HoughLines2(self.skeletor, cv.CreateMemStorage(), cv.CV_HOUGH_PROBABILISTIC, self.distRes, self.angleRes, self.threshold,self.minLine,self.maxGap)

    for f in foo:
      cv.Line(self.display, f[0], f[1], (0,0,0))
    cv.ShowImage("Hough", self.display) 

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
    cv.MorphologyEx(img_and,open_img, img_tmp, kernell, cv.CV_MOP_CLOSE, 30 )
    
    openimg = open_img
    return openimg
  

  
  
if __name__ == "__main__":
  mm = Mmeter()
  
