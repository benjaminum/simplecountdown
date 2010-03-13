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

class ConfigDialog(QDialog):
    def __init__(self, event='Event', dateTime=QDateTime(), parent=None):
        QDialog.__init__(self,parent)

        mainLayout = QVBoxLayout()
        
        self.eventEdit = QLineEdit(event)
        self.dateTimeEdit = QDateTimeEdit()
        if dateTime.isValid():
           self.dateTimeEdit.setDateTime( dateTime ) 
        else:
           self.dateTimeEdit.setDateTime( QDateTime.currentDateTime().addDays(1) )

        self.dateTimeEdit.setCalendarPopup(True)
        buttonBox = QDialogButtonBox( QDialogButtonBox.Save | QDialogButtonBox.Cancel )
        buttonBox.button(QDialogButtonBox.Save).clicked.connect(self.accept)
        buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.reject)

        mainLayout.addWidget(self.eventEdit)
        mainLayout.addWidget(self.dateTimeEdit)
        mainLayout.addWidget(buttonBox)

        self.setLayout(mainLayout)
