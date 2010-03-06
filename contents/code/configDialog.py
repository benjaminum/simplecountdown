# GPL
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class ConfigDialog(QDialog):
    def __init__(self,parent=None):
        QDialog.__init__(self,parent)

        mainLayout = QVBoxLayout()
        
        self.eventEdit = QLineEdit('Event')
        self.dateTimeEdit = QDateTimeEdit(QDateTime.currentDateTime().addDays(1))
        self.dateTimeEdit.setCalendarPopup(True)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttonBox.button(QDialogButtonBox.Save).clicked.connect(self.accept)
        buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.reject)

        mainLayout.addWidget(self.eventEdit)
        mainLayout.addWidget(self.dateTimeEdit)
        mainLayout.addWidget(buttonBox)


        self.setLayout(mainLayout)
