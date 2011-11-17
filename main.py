import Image;
import cv;
 
camcapture = cv.CreateCameraCapture(0)
cv.SetCaptureProperty(camcapture,cv.CV_CAP_PROP_FRAME_WIDTH, 640)
cv.SetCaptureProperty(camcapture,cv.CV_CAP_PROP_FRAME_HEIGHT, 480);
 
if not camcapture:
        print "Error opening WebCAM"
        sys.exit(1)
 
while 1:
    frame = cv.QueryFrame(camcapture)
    if frame is None:
        break
    cv.ShowImage('Camera', frame)
    k=cv.WaitKey(10);
