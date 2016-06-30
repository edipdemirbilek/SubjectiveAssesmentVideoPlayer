import os
from random import shuffle

videodir="<Video File Directory>"
filelistdir="<File List Directory>"
files = [f for f in os.listdir(videodir)]
shuffle(files)

filelist = open(filelistdir+'filelist.txt', 'w')
for item in files:
  filelist.write("%s\n" % item) 
 
filelist.close()