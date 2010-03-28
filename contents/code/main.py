################################################################################
#                                                                              #
#    simple-countdown                                                          #
#    Copyright (C) 2010  Benjamin Ummenhofer                                   #
#                                                                              #
#    This program is free software: you can redistribute it and/or modify      #
#    it under the terms of the GNU General Public License as published by      #
#    the Free Software Foundation, either version 3 of the License, or         #
#    (at your option) any later version.                                       #
#                                                                              #
#    This program is distributed in the hope that it will be useful,           #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             #
#    GNU General Public License for more details.                              #
#                                                                              #
#    You should have received a copy of the GNU General Public License         #
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.     #
#                                                                              #
################################################################################

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

        # Try long strings first
        self.shortStrings = False

        # Add labels to the layout
        self.layout = QGraphicsLinearLayout(Qt.Vertical, self.applet)
        self.eventLabel = Plasma.Label(self.applet)
        self.eventLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.eventLabel.setText('Event');
        self.timeLabel = Plasma.Label(self.applet)
        self.timeLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.timeLabel.setText('Time remaining')
        

        self.layout.addItem(self.eventLabel)
        self.layout.addItem(self.timeLabel)
        self.applet.setLayout(self.layout)

        self.setMinimumSize(150,60)
        #self.resize(375, 100)


        # Setup timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateLabel)

        self.readConfig()

        self.computeFontSizeTable()
        self.setLabelFonts()
        
        self.startCountDown( self.dateTime )


    def sizeHint(self, which, constraint):
        if which == Qt.PreferredSize:
           return QSizeF(375,100)
        else:
           return plasmascript.Applet.sizeHint(self, which, contraint)
       


    def paintInterface(self, painter, option, rect):
        painter.save()
        painter.setPen(Qt.white)
        #painter.drawText(self.eventLabel.geometry(), Qt.AlignVCenter | Qt.AlignHCenter, "Hello Python!")
        #painter.drawRect(self.eventLabel.geometry())
        #painter.drawRect(self.timeLabel.geometry())
        painter.restore()



    def showConfigurationInterface(self):
        dialog = ConfigDialog(self.eventLabel.text(), self.dateTime)
        if dialog.exec_() == 1:
           self.eventLabel.setText( dialog.eventEdit.text() )
           self.startCountDown( dialog.dateTimeEdit.dateTime() )
           self.saveConfig()
        

    def constraintsEvent(self, constraints):
        self.setLabelFonts()
        if int(constraints) == Plasma.SizeConstraint:
           cfg = self.config()
           cfg.writeEntry('geometry', self.geometry() )

        plasmascript.Applet.constraintsEvent(self, constraints)


    def computeFontSizeTable(self):
        self.fontSizeTable = []
        longestString = '   99 hours 99 minutes   '
        
        for pixSize in range(100,11,-1):
            font = QFont()
            font.setPixelSize(pixSize)
            font.setBold(True)
            fontMetric = QFontMetrics(font)
            w = fontMetric.width( longestString )
            h = fontMetric.height()
            self.fontSizeTable.append( (w, h, pixSize) )
        #print self.fontSizeTable



    def setLabelFonts(self):
        i = 0
        width   = self.fontSizeTable[i][0]
        height  = self.fontSizeTable[i][1]
        pixSize = self.fontSizeTable[i][2]
        minPixSize = self.fontSizeTable[len(self.fontSizeTable)-1][2]

        timeLabelWidth  = self.geometry().width() - self.getContentsMargins()[0] - self.getContentsMargins()[2]
        timeLabelHeight = self.geometry().height() // 2 - self.getContentsMargins()[1] - self.getContentsMargins()[3]

        while (width > timeLabelWidth or height > timeLabelHeight) and i < len(self.fontSizeTable):
              width   = self.fontSizeTable[i][0]
              height  = self.fontSizeTable[i][1]
              pixSize = self.fontSizeTable[i][2]
              i = i + 1

        if i == len(self.fontSizeTable) and width > timeLabelWidth:
           self.shortStrings = True
        else:
           self.shortStrings = False
        self.updateLabel()

        self.eventLabel.setStyleSheet('font-size:'+str(pixSize-4)+'px')
        self.timeLabel.setStyleSheet('font-size:'+str(pixSize)+'px; font-weight:bold')



    def readConfig(self):
        cfg = self.config()
        self.eventLabel.setText( cfg.readEntry('event',QString('Event')).toString() )
        self.dateTime = cfg.readEntry('dateTime', QDateTime() ).toDateTime()

        # Setup default geometry
        defaultGeometry = self.geometry()
        defaultGeometry.setSize( self.sizeHint(Qt.PreferredSize, QSizeF()) )
        # load stored geometry
        self.setGeometry( cfg.readEntry('geometry', defaultGeometry ).toRectF() )


           
    def saveConfig(self):
        cfg = self.config()
        cfg.writeEntry('event',self.eventLabel.text())
        cfg.writeEntry('dateTime', self.dateTime )
        cfg.writeEntry('geometry', self.geometry() )
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
        if secsToGo < 60*60:
           self.timer.setInterval(1000) # 1 second
        else:
           self.timer.setInterval(1000*60) # 60 seconds



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

           if self.shortStrings == True:
              days_str_pl = ' d '
              days_str_sg = ' d '
              hour_str_pl = ' h '
              hour_str_sg = ' h '
              min_str_pl  = ' m '
              min_str_sg  = ' m '
              sec_str_pl  = ' s '
              sec_str_sg  = ' s '
           else:
              days_str_pl = ' days '
              days_str_sg = ' day '
              hour_str_pl = ' hours '
              hour_str_sg = ' hour '
              min_str_pl  = ' minutes '
              min_str_sg  = ' minute '
              sec_str_pl  = ' secs '
              sec_str_sg  = ' sec '


           time_string = ' '
           if days > 1:
              time_string += str(days) + days_str_pl
           elif days > 0:
              time_string += str(days) + days_str_sg

           if days > 0 or hours > 0:
              if hours > 1 or hours == 0:
                 time_string += str(hours) + hour_str_pl
              else:
                 time_string += str(hours) + hour_str_sg

           if days == 0:
              if minutes > 1:
                 time_string += str(minutes) + min_str_pl
              elif minutes == 1 or (minutes == 0 and hours > 0):
                 time_string += str(minutes) + min_str_sg
              
           if days == 0 and hours == 0:
              if seconds > 1 or seconds == 0:
                 time_string += str(seconds) + sec_str_pl
              else:
                 time_string += str(seconds) + sec_str_sg


           self.timeLabel.setText(time_string)     
        else:
           self.update()


        

 
def CreateApplet(parent):
    return SimpleCountdown(parent)


