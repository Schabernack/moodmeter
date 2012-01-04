import cv
import math
import pprint
from processUnit import ProcessUnit
from matchingUnit import MatchingUnit

class Mmeter:
  
  def __init__(self):
    pp = pprint.PrettyPrinter(indent=4)
    img = cv.LoadImageM("img/1.jpg",cv.CV_LOAD_IMAGE_UNCHANGED)
#   img = cv.LoadImageM("/home/nico/Dropbox/ComputerVision/Code/1_small.jpg",cv.CV_LOAD_IMAGE_UNCHANGED)   
    self.tempDir = "templates/"
    self.tempList = ("0.png","22.png","45.png","67.png","90.png","112.png","135.png","157.png","180.png")
   
  

  #convert one channel img to 3 channel image 
  def one_c_to_3_c(self,img):
    mat = cv.CreateMat(img.height, img.width, cv.CV_8UC3)
    cv.Cvt(img, mat, cv.CV_GRAY2BGR)


  #2x2 images with same size
  def show_multiple_images(self, images):
    
    cv.NamedWindow("FOOBAR", cv.CV_WINDOW_AUTOSIZE)
    DispImg = cv.CreateImage((2* images[0].width +10, 2*images[0].height + 10), 8,3)

    img = images[0]
    cv.SetImageROI(DispImg, (0,0,img.width,img.height))
    cv.Resize(img,DispImg)

    img=images[1]
    cv.SetImageROI(DispImg, (img.width,img.height,img.width,img.height))
    cv.Resize(img,DispImg)     
    cv.ResetImageROI(DispImg)

    cv.ShowImage("FOOBAR", DispImg)
    
    #usw..... complete this method when program finished

  # return unaltered  pic
  def load_pic_from_hd(self):
    frame = cv.LoadImageM("img/test3.jpg",cv.CV_LOAD_IMAGE_UNCHANGED)
    
    image = cv.CreateMat(frame.height,frame.width,cv.CV_8UC3)
    cv.Copy(frame,image)
    
    pt1 = (frame.width/2,frame.height/2-30)
    pt2 = (pt1[0]+60,pt1[1]+60)
    color = (0,0,255)
    cv.Rectangle(frame, pt1,pt2 , color,thickness=2)
    
    cv.ShowImage("Image", frame)
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
        image = cv.QueryFrame(capture)
        print 'Space pressed. Image taken'
        cv.Flip(image,None,1)
        break

    returnimage = cv.CreateMat(image.height,image.width,cv.CV_8UC3)
    cv.Copy(image, returnimage)
    return returnimage
    
  
if __name__ == "__main__":
  mm = Mmeter()

  image = mm.get_cam_pic()
  cv.ShowImage("Original", image)
  
  cu = ProcessUnit()
  mu = MatchingUnit()
  processed = cu.processImage(image)

  cv.ShowImage("Processed", processed)
  mu.testRect(processed)
  	

  while cv.WaitKey(10)!=27:
    x=1
  
  
  
