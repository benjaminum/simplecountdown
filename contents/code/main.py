# GPL
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript
#from PyKDE4 import KConfigGroup
import ConfigParser
import os
from configDialog import *
 
class SimpleCountdown(plasmascript.Applet):
    def __init__(self,parent,args=None):
        plasmascript.Applet.__init__(self,parent)
 
    def init(self):
        # General stuff
        self.setHasConfigurationInterface(True)
        #self.setAspectRatioMode(Plasma.KeepAspectRatio)
        self.setAspectRatioMode(Plasma.IgnoreAspectRatio)
        self.theme = Plasma.Svg(self)
        self.setBackgroundHints(Plasma.Applet.DefaultBackground)

        # Add labels to the layout
        self.layout = QGraphicsLinearLayout(Qt.Vertical, self.applet)
        self.eventLabel = Plasma.Label(self.applet)
        self.eventLabel.setAlignment(Qt.AlignHCenter)
        self.eventLabel.setText('Event');
        self.eventLabel.setStyleSheet('font-size:18px')
        self.timeLabel = Plasma.Label(self.applet)
        self.timeLabel.setAlignment(Qt.AlignHCenter)
        self.timeLabel.setText('Time remaining')
        self.timeLabel.setStyleSheet('font-size:24px; font-weight:bold')

        self.layout.addItem(self.eventLabel)
        self.layout.addItem(self.timeLabel)
        self.applet.setLayout(self.layout)
        self.resize(300, 85)

        # Setup timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateLabel)

        self.readConfig()


        #dialog = ConfigDialog()
        #dialog.exec_()


    def paintInterface(self, painter, option, rect):
        painter.save()
        #painter.setPen(Qt.white)
        #painter.drawText(rect, Qt.AlignVCenter | Qt.AlignHCenter, "Hello Pyt    hon!")
        painter.restore()


    def showConfigurationInterface(self):
        dialog = ConfigDialog()
        if dialog.exec_() == 1:
           self.eventLabel.setText( dialog.eventEdit.text() )
           self.startCountDown( dialog.dateTimeEdit.dateTime() )
           self.saveConfig()
        


    def readConfig(self):
        cfg = self.config()
        cfg.readEntry('event',QString('event'))
        cfg.readEntry('dateTime', QDateTime() )

           
    def saveConfig(self):
        cfg = self.config()
        cfg.writeEntry('event',self.eventLabel.text())
        cfg.writeEntry('dateTime', self.dateTime )
        cfg.sync()



    def startCountDown(self, eventDateTime):
        self.timer.stop()
        self.dateTime = eventDateTime
        now = QDateTime.currentDateTime()
        seconds = now.secsTo(self.dateTime)

        if eventDateTime.isValid() and seconds > 0:
           self.setTimerInterval(seconds)

        self.timer.start()
        self.updateLabel()

           
    def setTimerInterval(self, secsToGo):
        if secsToGo > 60*60*24:
           self.timer.setInterval(1000*60)
        elif secsToGo > 60*60:
           self.timer.setInterval(1000*60*60)
        else:
           self.timer.setInterval(1000)
        #self.timer.setInterval(1000)


    def updateLabel(self):
        if self.dateTime.isValid():
           # Compute numbers for the string
           now = QDateTime.currentDateTime()
           seconds = now.secsTo(self.dateTime)

           if seconds < 0:
              self.timeLabel.setText('Time is up!')
              self.timer.stop()
              return
           else:
              self.setTimerInterval(seconds)

           days = seconds // (60*60*24)
           seconds -= days*60*60*24
           hours = seconds // (60*60)
           minutes = (seconds // 60) % 60
           seconds = seconds % 60

           time_string = ' '
           if days > 1:
              time_string += str(days) + ' days '
           elif days > 0:
              time_string += str(days) + ' day '

           if days > 0 or hours > 0:
              if hours > 1:
                 time_string += str(hours) + ' hours '
              else:
                 time_string += str(hours) + ' hour '

           if days == 0:
              if minutes > 1:
                 time_string += str(minutes) + ' minutes '
              else:
                 time_string += str(minutes) + ' minute '

           if days == 0 and hours == 0:
              if seconds > 1:
                 time_string += str(seconds) + ' secs '
              else:
                 time_string += str(seconds) + ' sec '

           self.timeLabel.setText(time_string)     

        

 
def CreateApplet(parent):
    return SimpleCountdown(parent)
