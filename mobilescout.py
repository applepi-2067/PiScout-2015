from PyQt4 import QtCore, QtGui
import sys

try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

try:
	_encoding = QtGui.QApplication.UnicodeUTF8
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(QtGui.QWidget):
	def __init__(self):
		QtGui.QWidget.__init__(self)
		self.setupUi(self)
		
	def setupUi(self, Form):
		Form.setObjectName(_fromUtf8("Form"))
		Form.resize(274, 215)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
		Form.setSizePolicy(sizePolicy)
		self.verticalLayoutWidget = QtGui.QWidget(Form)
		self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 271, 211))
		self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
		self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
		self.verticalLayout.setMargin(0)
		self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
		self.label = QtGui.QLabel(self.verticalLayoutWidget)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
		self.label.setSizePolicy(sizePolicy)
		self.label.setObjectName(_fromUtf8("label"))
		self.verticalLayout.addWidget(self.label)
		self.servername = QtGui.QLineEdit(self.verticalLayoutWidget)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.servername.sizePolicy().hasHeightForWidth())
		self.servername.setSizePolicy(sizePolicy)
		self.servername.setText(_fromUtf8(""))
		self.servername.setObjectName(_fromUtf8("servername"))
		self.verticalLayout.addWidget(self.servername)
		self.getdata = QtGui.QPushButton(self.verticalLayoutWidget)
		self.getdata.setObjectName(_fromUtf8("getdata"))
		self.verticalLayout.addWidget(self.getdata)
		self.horizontalLayout = QtGui.QHBoxLayout()
		self.horizontalLayout.setSpacing(4)
		self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
		self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
		self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
		self.team1 = QtGui.QLineEdit(self.verticalLayoutWidget)
		self.team1.setObjectName(_fromUtf8("team1"))
		self.horizontalLayout.addWidget(self.team1)
		self.team2 = QtGui.QLineEdit(self.verticalLayoutWidget)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.team2.sizePolicy().hasHeightForWidth())
		self.team2.setSizePolicy(sizePolicy)
		self.team2.setObjectName(_fromUtf8("team2"))
		self.horizontalLayout.addWidget(self.team2)
		self.verticalLayout.addLayout(self.horizontalLayout)
		self.processmatch = QtGui.QPushButton(self.verticalLayoutWidget)
		self.processmatch.setObjectName(_fromUtf8("processmatch"))
		self.verticalLayout.addWidget(self.processmatch)
		self.team = QtGui.QLineEdit(self.verticalLayoutWidget)
		self.team.setText(_fromUtf8(""))
		self.team.setObjectName(_fromUtf8("team"))
		self.verticalLayout.addWidget(self.team)
		self.processteam = QtGui.QPushButton(self.verticalLayoutWidget)
		self.processteam.setObjectName(_fromUtf8("processteam"))
		self.verticalLayout.addWidget(self.processteam)
		self.compare = QtGui.QPushButton(self.verticalLayoutWidget)
		self.compare.setObjectName(_fromUtf8("compare"))
		self.verticalLayout.addWidget(self.compare)

		self.retranslateUi(Form)
		QtCore.QMetaObject.connectSlotsByName(Form)

	def retranslateUi(self, Form):
		Form.setWindowTitle(_translate("Form", "Form", None))
		self.label.setText(_translate("Form", "Head Scout computer name:", None))
		self.getdata.setText(_translate("Form", "Sync Scouting Data", None))
		self.team1.setPlaceholderText(_translate("Form", "Alliance Partner 1", None))
		self.team2.setPlaceholderText(_translate("Form", "Alliance Partner 2", None))
		self.processmatch.setText(_translate("Form", "Process Match", None))
		self.team.setPlaceholderText(_translate("Form", "Team Number", None))
		self.processteam.setText(_translate("Form", "Get Data for Specific Team", None))
		self.compare.setText(_translate("Form", "Compare All Teams", None))

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	ex = Ui_Form()
	ex.show()
	sys.exit(app.exec_())