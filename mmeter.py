import cv
import math
import pprint
from processUnit import ProcessUnit
from matchingUnit import MatchingUnit
from logger import Logger
from pictureviewer import Pictureviewer as pv


class Mmeter:
  
  def __init__(self):
    pp = pprint.PrettyPrinter(indent=4)   

  # return unaltered  pic
  def load_pic_from_hd(self):
    frame = cv.LoadImageM("img/test3.jpg",cv.CV_LOAD_IMAGE_UNCHANGED)
    
    image = cv.CreateMat(frame.height,frame.width,cv.CV_8UC3)
    cv.Copy(frame,image)
    
    pt1 = (frame.width/2,frame.height/2-30)
    pt2 = (pt1[0]+60,pt1[1]+60)
    color = (0,0,255)
    cv.Rectangle(frame, pt1,pt2 , color,thickness=2)
    
    return image

  #return unaltered rgb pic
  def get_cam_pic(self):
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
      elif k == 0x20: # Space
        cv.DestroyWindow('Camera')
        image = cv.QueryFrame(capture)
        print 'Space pressed. Image taken'
        cv.Flip(image,None,1)
        break

    returnimage = cv.CreateMat(image.height,image.width,cv.CV_8UC3)
    cv.Copy(image, returnimage)
    return returnimage
    
  def showResult(self,image,angle):
    if angle < 23:
      mood = "Amazing!!!"
    elif angle < 67:
      mood = "Good!"
    elif angle < 112:
      mood = "Meh .."
    elif angle < 155:
      mood = "Bad."
    else:
      mood = "Catastrophic!!"
  
    font = cv.InitFont(cv.CV_FONT_HERSHEY_DUPLEX,1.0,1.0,thickness=2)
  
    cv.PutText(image, mood, (50,50) , font, (0,255,255))
  
    Logger.addImage(image, "Result")
    pv.addColor(image,"result")

    
  def run(self):
    pu = ProcessUnit()
    mu = MatchingUnit()
    
    image = self.get_cam_pic()
    
    img_orig = cv.CreateMat(image.height,image.width,cv.CV_8UC3)
    cv.Copy(image,img_orig)
    Logger.addImage(img_orig, "img_original")

    processed = pu.processImage(image)
  
    angle = mu.run(processed)
    	    
    self.showResult(image,angle)
    pv.showPictures()
    Logger.logImages()
    
  
if __name__ == "__main__":
  mm = Mmeter()
  mm.run()


  while 1:
    k = cv.WaitKey(10)

    if k == 0x1b: # ESC
      print 'ESC pressed. Exiting ...'
      break
    elif k == 0x20: # Space
      cv.DestroyAllWindows()
      mm.run()


