import Image
import cv
import math
import pprint

class Mmeter:
  
  def __init__(self):
    pp = pprint.PrettyPrinter(indent=4)
    img = cv.LoadImageM("img/10.jpg",cv.CV_LOAD_IMAGE_UNCHANGED)
    
    self.tempDir = "templates/"
    self.tempList = ("0.png","22.png","45.png","67.png","90.png","112.png","135.png","157.png","180.png")
  

    self.openimg=self.fgdisc_rgb(img)
#    self.openimg = self.fill_hand(self.openimg)

    canny = cv.CreateMat(img.height, img.width, cv.CV_8UC1)

    cv.Canny(self.openimg, canny, 50.0,210.0)
    cv.ShowImage("canny",canny)
    contours =  cv.FindContours(canny,  cv.CreateMemStorage(),  cv.CV_RETR_LIST, cv.CV_CHAIN_APPROX_NONE, (0,0))
    
    
    for sequence in self.contour_iterator(contours):          
      for seqpoints in sequence:
        cv.Circle(img, seqpoints, 1, (0,0,255))
    
    self.getBestMatch(img)
    cv.ShowImage("bild", img)
    cv.MoveWindow("bild", 20,20)  

    while cv.WaitKey(10)!=27:
      x=1 
      
  def contour_iterator(self,contour):
    while contour:
      yield contour
      contour = contour.h_next()

  
  def getBestMatch(self,img):
    match = dict()
    for temp in self.tempList:
      template = cv.LoadImage(self.tempDir+temp,0)
      
      result = cv.CreateMat(img.height-template.height+1, img.width-template.width+1, cv.CV_32FC1)    
      cv.MatchTemplate(self.openimg,template,result,cv.CV_TM_SQDIFF)
      match[cv.MinMaxLoc(result)[0]] = temp
      
    res = match[min(match.keys())]
    
    font = cv.InitFont(cv.CV_FONT_HERSHEY_COMPLEX,1,1,0.0,1,cv.CV_AA)
    cv.PutText(img,res,(30,30),font,(255,255,0)) 
      
 
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

  def fgdisc_rgb(self, image):
    r_plane = cv.CreateMat(image.height, image.width, cv.CV_8UC1)
    g_plane = cv.CreateMat(image.height, image.width, cv.CV_8UC1)
    b_plane = cv.CreateMat(image.height, image.width, cv.CV_8UC1)

    cv.Split(image, b_plane, g_plane, r_plane, None)
    
    img_skin = cv.CreateMat(image.height, image.width, cv.CV_8UC1)

    for row in xrange(image.rows):
      for col in xrange(image.cols):
        b,g,r = image[row,col]
        #see paper a survey on pixel based skin color detection techniques (vezhnevets et. al.)
        if((r > 95 and g > 40 and b > 20) and 
            (max(r, b, g)-min(r,b,g) > 15) and 
            (abs(r-g) > 15 and r>b and r>g)):
              cv.Set2D(img_skin, row, col, (255))
        else: 
          cv.Set2D(img_skin, row, col, (0))
    cv.ShowImage("fgdiscrgb",img_skin)

    return img_skin


  def fill_hand(self,img):
    img_tmp = cv.CreateMat(img.height, img.width, cv.CV_8UC1)
    img_fill = cv.CreateMat(img.height, img.width, cv.CV_8UC1)
    kernel5=cv.CreateStructuringElementEx(2,1,1,0, cv.CV_SHAPE_RECT)
    kernell=cv.CreateStructuringElementEx(5,5,2,2, cv.CV_SHAPE_RECT)
 
    cv.Erode(img, img_fill, iterations=2)  
    cv.Erode(img_fill, img_fill, iterations=1, element=kernel5) 
    open_img = cv.CreateMat(img.height, img.width, cv.CV_8UC1)
    cv.MorphologyEx(img_fill,open_img, img_tmp, kernell, cv.CV_MOP_CLOSE, 30 )
   
    cv.ShowImage("fillhand",open_img)
    return open_img

  #foreground/background discrimination   
  def fg_disc(self, image):
    img_hsv= cv.CreateMat(image.height, image.width, cv.CV_8UC3)
    cv.CvtColor(image, img_hsv, cv.CV_BGR2HSV)
    
    cv.ShowImage("HSV",img_hsv)
    cv.MoveWindow("HSV",500,500)
    
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
  
