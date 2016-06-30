import sys
import os.path
import vlc
from PyQt4 import QtGui, QtCore
import os
import random
import time
import pandas as pd
from random import shuffle
import time
import threading

#export VLC_PLUGIN_PATH=/Applications/VLC.app/Contents/MacOS/plugins/

dir=None
mvidir=None
counter=None
files=None
fileIndex=0

trainingListFile="training.txt"
trainingScoreFile="Training.csv"

session1Part1ListFile="session1part1.txt"
session1Part1ScoreFile="Session1Part1.csv"
session1Part2ListFile="session1part2.txt"
session1Part2ScoreFile="Session1Part2.csv"
session1Part3ListFile="session1part1.txt"
session1Part3ScoreFile="Session1Part3.csv"
session1Part4ListFile="session1part2.txt"
session1Part4ScoreFile="Session1Part4.csv"

session2Part1ListFile="session2part1.txt"
session2Part1ScoreFile="Session2Part1.csv"
session2Part2ListFile="session2part2.txt"
session2Part2ScoreFile="Session2Part2.csv"
session2Part3ListFile="session2part1.txt"
session2Part3ScoreFile="Session2Part3.csv"
session2Part4ListFile="session2part2.txt"
session2Part4ScoreFile="Session2Part4.csv"

class Player(QtGui.QMainWindow):
    """A simple Media Player using VLC and Qt
    """
    
    filename = None
    rated=False
    
    
    def __init__(self, master=None):
        QtGui.QMainWindow.__init__(self, master)
        self.title="INRS Perceived Quality Modelling Experiment"
        self.setWindowTitle(self.title)

        # creating a basic vlc instance
        self.instance = vlc.Instance()
        # creating an empty vlc media player
        self.mediaplayer = self.instance.media_player_new()

        self.createUI()
        self.isPaused = False
        self.counter=0
        
        seed = time.time()
        random.seed(seed)
        
        if sys.platform.startswith('win'):
            self.rootdir="<RootDirectory>"
            self.acrscoresdir=self.rootdir+"<ACRScoresDirectory>"
            self.videostoratedir=self.rootdir+"<VideosToRateDirectory>"
            self.filelistdir=self.rootdir+"<RandomizedFileListDirectory>"
            
        elif sys.platform.startswith('darwin'):
            self.rootdir="<RootDirectory>"
            self.acrscoresdir=self.rootdir+"<ACRScoresDirectory>"
            self.videostoratedir=self.rootdir+"<VideosToRateDirectory>"
            self.filelistdir=self.rootdir+"<RandomizedFileListDirectory>"

    def createUI(self):
        """Set up the user interface, signals & slots
        """
        self.widget = QtGui.QWidget(self)
        self.setCentralWidget(self.widget)

        # In this widget, the video will be drawn
        if sys.platform == "darwin": # for MacOS
            self.videoframe = QtGui.QMacCocoaViewContainer(0)
        else:
            self.videoframe = QtGui.QFrame()
        self.palette = self.videoframe.palette()
        self.palette.setColor (QtGui.QPalette.Window,
                               QtGui.QColor(0,0,0))
        self.videoframe.setPalette(self.palette)
        self.videoframe.setAutoFillBackground(True)

        self.positionslider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.positionslider.setToolTip("Position")
        self.positionslider.setMaximum(1000)
        self.connect(self.positionslider,
                     QtCore.SIGNAL("sliderMoved(int)"), self.setPosition)

        self.hbuttonbox = QtGui.QHBoxLayout()
                     
        self.playbutton = QtGui.QPushButton("Play")
        self.hbuttonbox.addWidget(self.playbutton)
        self.connect(self.playbutton, QtCore.SIGNAL("clicked()"),
                     self.PlayPause)
                     
        self.number_group=QtGui.QButtonGroup(self.widget) # Number group
                     
        self.label=QtGui.QLabel("")
        self.hbuttonbox.addWidget(self.label)
        self.label.hide()
                
        self.r5=QtGui.QRadioButton("(5) Excellent")
        self.number_group.addButton(self.r5)  
        self.hbuttonbox.addWidget(self.r5)
        self.r5.hide()
        
        self.r4=QtGui.QRadioButton("(4) Good")
        self.number_group.addButton(self.r4) 
        self.hbuttonbox.addWidget(self.r4)
        self.r4.hide()
        
        self.r3=QtGui.QRadioButton("(3) Fair")
        self.number_group.addButton(self.r3)
        self.hbuttonbox.addWidget(self.r3)
        self.r3.hide()
        
        self.r2=QtGui.QRadioButton("(2) Poor")
        self.number_group.addButton(self.r2)
        self.hbuttonbox.addWidget(self.r2)
        self.r2.hide()
        
        self.r1=QtGui.QRadioButton("(1) Bad       ")
        self.number_group.addButton(self.r1)
        self.hbuttonbox.addWidget(self.r1)
        self.r1.hide()
                     
        self.ratebutton = QtGui.QPushButton("Rate")
        self.hbuttonbox.addWidget(self.ratebutton)
        self.connect(self.ratebutton, QtCore.SIGNAL("clicked()"),
                     self.Rate)
        self.ratebutton.hide()

        self.hbuttonbox.addStretch(1)
        self.volumeslider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.volumeslider.setMaximum(100)
        self.volumeslider.setValue(self.mediaplayer.audio_get_volume())
        self.volumeslider.setToolTip("Volume")
        self.hbuttonbox.addWidget(self.volumeslider)
        self.connect(self.volumeslider,
                     QtCore.SIGNAL("valueChanged(int)"),
                     self.setVolume)

        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.addWidget(self.videoframe)
        self.vboxlayout.addWidget(self.positionslider)
        self.vboxlayout.addLayout(self.hbuttonbox)

        self.widget.setLayout(self.vboxlayout)
        
        resolution = QtGui.QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - 540,
                  (resolution.height() / 2) - 360)

        exit = QtGui.QAction("&Exit", self)
        self.connect(exit, QtCore.SIGNAL("triggered()"), sys.exit)
        menubar = self.menuBar()
        filemenu = menubar.addMenu("&File")
        
        training = QtGui.QAction("&Training", self)
        self.connect(training, QtCore.SIGNAL("triggered()"), self.StartTraining)
        
        session11 = QtGui.QAction("&Session 1: Part 1", self)
        self.connect(session11, QtCore.SIGNAL("triggered()"), self.StartSession1Part1)
        
        session12 = QtGui.QAction("&Session 1: Part 2", self)
        self.connect(session12, QtCore.SIGNAL("triggered()"), self.StartSession1Part2)
        
        session13 = QtGui.QAction("&Session 1: Part 3", self)
        self.connect(session13, QtCore.SIGNAL("triggered()"), self.StartSession1Part3)
        
        session14 = QtGui.QAction("&Session 1: Part 4", self)
        self.connect(session14, QtCore.SIGNAL("triggered()"), self.StartSession1Part4)
        
        session21 = QtGui.QAction("&Session 2: Part 1", self)
        self.connect(session21, QtCore.SIGNAL("triggered()"), self.StartSession2Part1)
        
        session22 = QtGui.QAction("&Session 2: Part 2", self)
        self.connect(session22, QtCore.SIGNAL("triggered()"), self.StartSession2Part2)
        
        session23 = QtGui.QAction("&Session 2: Part 3", self)
        self.connect(session23, QtCore.SIGNAL("triggered()"), self.StartSession2Part3)
        
        session24 = QtGui.QAction("&Session 2: Part 4", self)
        self.connect(session24, QtCore.SIGNAL("triggered()"), self.StartSession2Part4)
        
        filemenu.addAction(exit)
        filemenu.addAction(training)
        filemenu.addAction(session11)
        filemenu.addAction(session12)
        filemenu.addAction(session13)
        filemenu.addAction(session14)
        filemenu.addAction(session21)
        filemenu.addAction(session22)
        filemenu.addAction(session23)
        filemenu.addAction(session24)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(200)
        self.connect(self.timer, QtCore.SIGNAL("timeout()"),
                     self.updateUI)
     
    def ContinueFileIfExist(self, fullFileName):
        if os.path.isfile(fullFileName):
            existingScores = pd.read_csv(fullFileName)
            existingScoreslen=len(existingScores)
            print ("ExistingScores len: " + str(existingScoreslen))
            if existingScoreslen > 0:
                self.fileIndex=existingScoreslen+1
                self.counter=existingScoreslen+1
                print ("New FileIndex: "+str(self.fileIndex))
                print ("New Counter: "+str(self.counter))
            else:
                self.fileIndex=0
                self.counter=0
        else:
            print ("File does not exist. Continue as usual.")
            self.fileIndex=0
            self.counter=0
               
    def StartTraining(self):
        self.files = [line.strip() for line in open(self.filelistdir+trainingListFile, 'r')]
        self.videoCount=len(self.files)
        self.fileIndex=0
        self.acrScoresFileName=trainingScoreFile
        self.counter=0
        
        msgBox = QtGui.QMessageBox()
        msgBox.setText("Training mode: "+str(self.videoCount)+" videos to rate.")
        msgBox.setInformativeText("Press OK when you are ready.")
        msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
        ret = msgBox.exec_()
        self.title="Training mode: "+str(self.videoCount)+" videos to rate."
        self.setWindowTitle(self.title)

    def StartSession1Part1(self):
        self.files = [line.strip() for line in open(self.filelistdir+session1Part1ListFile, 'r')]
        self.videoCount=len(self.files)
        self.acrScoresFileName=session1Part1ScoreFile
        self.ContinueFileIfExist(self.acrscoresdir+self.acrScoresFileName)
        
        msgBox = QtGui.QMessageBox()
        msgBox.setText("Session1, part1: "+str(self.videoCount)+" videos to rate.")
        msgBox.setInformativeText("Press OK when you are ready.")
        msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
        ret = msgBox.exec_()
        self.title="Session1, part1: "+str(self.videoCount)+" videos to rate."
        self.setWindowTitle(self.title)
        
    def StartSession1Part2(self):
        self.files = [line.strip() for line in open(self.filelistdir+session1Part2ListFile, 'r')]
        self.videoCount=len(self.files)
        self.acrScoresFileName=session1Part2ScoreFile
        self.ContinueFileIfExist(self.acrscoresdir+self.acrScoresFileName)
        
        
        msgBox = QtGui.QMessageBox()
        msgBox.setText("Session1, part2: "+str(self.videoCount)+" videos to rate.")
        msgBox.setInformativeText("Press OK when you are ready.")
        msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
        ret = msgBox.exec_()
        self.title="Session1, part2: "+str(self.videoCount)+" videos to rate."
        self.setWindowTitle(self.title)
        
    def StartSession1Part3(self):
        self.files = [line.strip() for line in open(self.filelistdir+session1Part3ListFile, 'r')]
        self.videoCount=len(self.files)
        self.acrScoresFileName=session1Part3ScoreFile
        self.ContinueFileIfExist(self.acrscoresdir+self.acrScoresFileName)
        
        msgBox = QtGui.QMessageBox()
        msgBox.setText("Session1, part3: "+str(self.videoCount)+" videos to rate.")
        msgBox.setInformativeText("Press OK when you are ready.")
        msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
        ret = msgBox.exec_()
        self.title="Session1, part3: "+str(self.videoCount)+" videos to rate."
        self.setWindowTitle(self.title)
        
    def StartSession1Part4(self):
        self.files = [line.strip() for line in open(self.filelistdir+session1Part4ListFile, 'r')]
        self.videoCount=len(self.files)
        self.acrScoresFileName=session1Part4ScoreFile
        self.ContinueFileIfExist(self.acrscoresdir+self.acrScoresFileName)
        
        msgBox = QtGui.QMessageBox()
        msgBox.setText("Session1, part4: "+str(self.videoCount)+" videos to rate.")
        msgBox.setInformativeText("Press OK when you are ready.")
        msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
        ret = msgBox.exec_()
        self.title="Session1, part4: "+str(self.videoCount)+" videos to rate."
        self.setWindowTitle(self.title)
        
    def StartSession2Part1(self):   
        self.files = [line.strip() for line in open(self.filelistdir+session2Part1ListFile, 'r')]
        self.videoCount=len(self.files)
        self.acrScoresFileName=session2Part1ScoreFile
        self.ContinueFileIfExist(self.acrscoresdir+self.acrScoresFileName)
        
        msgBox = QtGui.QMessageBox()
        msgBox.setText("Session2, part1: "+str(self.videoCount)+" videos to rate.")
        msgBox.setInformativeText("Press OK when you are ready.")
        msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
        ret = msgBox.exec_()
        self.title="Session2, part1: "+str(self.videoCount)+" videos to rate."
        self.setWindowTitle(self.title)
        
    def StartSession2Part2(self):  
        self.files = [line.strip() for line in open(self.filelistdir+session2Part2ListFile, 'r')]
        self.videoCount=len(self.files)
        self.acrScoresFileName=session2Part2ScoreFile
        self.ContinueFileIfExist(self.acrscoresdir+self.acrScoresFileName)
        
        msgBox = QtGui.QMessageBox()
        msgBox.setText("Session2, part2: "+str(self.videoCount)+" videos to rate.")
        msgBox.setInformativeText("Press OK when you are ready.")
        msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
        ret = msgBox.exec_()
        self.title="Session2, part2: "+str(self.videoCount)+" videos to rate."
        self.setWindowTitle(self.title)

    def StartSession2Part3(self):   
        self.files = [line.strip() for line in open(self.filelistdir+session2Part3ListFile, 'r')]
        self.videoCount=len(self.files)
        self.acrScoresFileName=session2Part3ScoreFile
        self.ContinueFileIfExist(self.acrscoresdir+self.acrScoresFileName)
        
        msgBox = QtGui.QMessageBox()
        msgBox.setText("Session2, part3: "+str(self.videoCount)+" videos to rate.")
        msgBox.setInformativeText("Press OK when you are ready.")
        msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
        ret = msgBox.exec_()
        self.title="Session2, part3: "+str(self.videoCount)+" videos to rate."
        self.setWindowTitle(self.title)

    def StartSession2Part4(self):  
        self.files = [line.strip() for line in open(self.filelistdir+session2Part4ListFile, 'r')]
        self.videoCount=len(self.files)
        self.acrScoresFileName=session2Part4ScoreFile
        self.ContinueFileIfExist(self.acrscoresdir+self.acrScoresFileName)
        
        msgBox = QtGui.QMessageBox()
        msgBox.setText("Session2, part4: "+str(self.videoCount)+" videos to rate.")
        msgBox.setInformativeText("Press OK when you are ready.")
        msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
        ret = msgBox.exec_()
        self.title="Session2, part4: "+str(self.videoCount)+" videos to rate."
        self.setWindowTitle(self.title)
        
    def ShowRateButtons(self):
        time.sleep(10)
        self.ratebutton.show()
        self.r5.show()
        self.r4.show()
        self.r3.show()
        self.r2.show()
        self.r1.show()
        self.label.show()
        
    def PlayPause(self):
        """Toggle play/pause status
        """
        if self.mediaplayer.is_playing():
            #print "Media Player is playing."
            self.mediaplayer.pause()
            self.playbutton.setText("Play")
            self.isPaused = True
        else:
            #print "Media Player is not playing."
            if self.rated == True:
                #print "Media already rated. Openning file and return."
                self.OpenFile()
                return
            if self.mediaplayer.play() == -1:
                #print "Medi player play status is -1. Openning File and return."
                self.OpenFile()
                return
            #print "Playing media and starting the timer. Filename: "+self.filename
            #print "Media: " +str(self.mediaplayer.get_media())
            self.mediaplayer.play()
            self.playbutton.setText("Pause")
            self.timer.start()
            self.isPaused = False
        
        t = threading.Thread(target=self.ShowRateButtons)
        t.start()
        #self.ShowRateButtons()
        

    def Rate(self):
        """Rate
        """
        rating=0
        fd = open(self.acrscoresdir+self.acrScoresFileName,'a')

        if self.r1.isChecked():
            rating=1
        if self.r2.isChecked():
            rating=2
        if self.r3.isChecked():
            rating=3
        if self.r4.isChecked():
            rating=4
        if self.r5.isChecked():
            rating=5

        myCsvRow=os.path.splitext(self.filename)[0]+","+str(rating)+","+str(self.mediaplayer.get_time())+"\n"
        fd.write(myCsvRow)
        fd.close()
            
        self.mediaplayer.stop()
        self.playbutton.setText("Play Next Video")
        self.ratebutton.hide()
        self.r5.hide()
        self.r4.hide()
        self.r3.hide()
        self.r2.hide()
        self.r1.hide()
        self.label.hide()
        self.rated=True

    def Stop(self):
        """Stop player
        """
        self.mediaplayer.stop()
        self.playbutton.setText("Play Next Video")
        self.ratebutton.hide()
        self.r5.hide()
        self.r4.hide()
        self.r3.hide()
        self.r2.hide()
        self.r1.hide()
        self.label.hide()
        
    def OpenNextFile(self):    
        localFileName=self.files[self.fileIndex]
        self.fileIndex=self.fileIndex+1
        return localFileName
    
	#This function is not being used
    def LeastScoredFile(self):
        randomScores = pd.read_csv(self.acrscoresdir+"RandomScores.csv")
        matchFile = randomScores .groupby('General FileName').agg(['count']).reset_index().sort([('MOS','count')]).iloc[:1][[('General FileName','')]].to_csv(index = False, header=False, line_terminator="")
        return matchFile+".ts"


    def AllFilesPlayed(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setText("All Files in this session are played.")
        msgBox.setInformativeText("Click OK to end.")
        msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
        ret = msgBox.exec_()
        
    def OpenFile(self, filename=None):
        """Open a media file in a MediaPlayer
        """
        if self.counter >= self.videoCount:
            #print "All Files Played."
            self.AllFilesPlayed()
            return
            
        self.counter+=1
        self.rated=False        
        self.filename=self.OpenNextFile()
        
        self.media = self.instance.media_new(self.videostoratedir+self.filename)
        # put the media in the media player
        self.mediaplayer.set_media(self.media)

        # parse the metadata of the file
        self.media.parse()
        # set the title of the track as window title
        #self.setWindowTitle(self.media.get_meta(0))
        self.setWindowTitle(self.title+" Videos rated: "+str(self.counter))

        # the media player has to be 'connected' to the QFrame
        # (otherwise a video would be displayed in it's own window)
        # this is platform specific!
        # you have to give the id of the QFrame (or similar object) to
        # vlc, different platforms have different functions for this
        if sys.platform.startswith('linux'): # for Linux using the X Server
            self.mediaplayer.set_xwindow(self.videoframe.winId())
        elif sys.platform == "win32": # for Windows
            self.mediaplayer.set_hwnd(self.videoframe.winId())
        elif sys.platform == "darwin": # for MacOS
            self.mediaplayer.set_nsobject(self.videoframe.winId())
        self.PlayPause()

    def setVolume(self, Volume):
        """Set the volume
        """
        self.mediaplayer.audio_set_volume(Volume)

    def setPosition(self, position):
        """Set the position
        """
        # setting the position to where the slider was dragged
        self.mediaplayer.set_position(position / 1000.0)
        # the vlc MediaPlayer needs a float value between 0 and 1, Qt
        # uses integer variables, so you need a factor; the higher the
        # factor, the more precise are the results
        # (1000 should be enough)

    def updateUI(self):
        """updates the user interface"""
        # setting the slider to the desired position
        self.positionslider.setValue(self.mediaplayer.get_position() * 1000)

        if not self.mediaplayer.is_playing():
            # no need to call this function if nothing is played
            self.timer.stop()
            if not self.isPaused:
                # after the video finished, the play button stills shows
                # "Pause", not the desired behavior of a media player
                # this will fix it
                self.Stop()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    player = Player()
    player.show()
    player.resize(1080, 720)
    if sys.argv[1:]:
        player.OpenFile(sys.argv[1])
    sys.exit(app.exec_())