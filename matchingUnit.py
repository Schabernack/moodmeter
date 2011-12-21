import cv
import math
import pprint

class Mmeter:
  
  def __init__(self,image):
    
      
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
      
    
    
  

  
    
if __name__ == "__main__":
  mm = Mmeter()
  
