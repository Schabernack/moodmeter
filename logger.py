import os
import numpy as np
import  cv

class Logger:

	__imagelist = [] 

	##durchsuche log ordner nach groesster ordner id
	##erstelle neuen ordner und schreibe alle imgs rein
	##anschliessend: reset list		
	@staticmethod
	def logImages():
	
		logfolder = r'./log' 
		if not os.path.exists(logfolder): os.makedirs(logfolder) 
		folderlist = os.listdir(logfolder)
		if ".DS_Store" in folderlist:
				folderlist.remove(".DS_Store")
		if not folderlist:
			id = '1'
		else:
			id = str(max( int(i) for  i in folderlist)   +1)
		
		imgpath = logfolder + '/' + id
		os.makedirs(imgpath)
		
		for image in Logger.__imagelist:
			print "Saving ", image[1]
			cv.SaveImage(imgpath+'/'+image[1]+'.png', image[0])

		Logger.resetList()

	##fuege img zu interner liste hinzu (filename ist name unter dem datei spaeter gespeichert wird)
	@staticmethod
	def addImage(img, filename):	
		Logger.__imagelist.append((img, filename))

	## Liste leeren
	@staticmethod
	def resetList():
		Logger.__imagelist[:] = []