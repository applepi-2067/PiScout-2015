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
		Form.resize(274, 227)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
		Form.setSizePolicy(sizePolicy)
		self.verticalLayoutWidget = QtGui.QWidget(Form)
		self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 271, 224))
		self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
		self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
		self.verticalLayout.setMargin(0)
		self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
		self.serverstart = QtGui.QPushButton(self.verticalLayoutWidget)
		self.serverstart.setObjectName(_fromUtf8("serverstart"))
		self.verticalLayout.addWidget(self.serverstart)
		self.stopserver = QtGui.QPushButton(self.verticalLayoutWidget)
		self.stopserver.setObjectName(_fromUtf8("stopserver"))
		self.verticalLayout.addWidget(self.stopserver)
		self.name = QtGui.QPushButton(self.verticalLayoutWidget)
		self.name.setObjectName(_fromUtf8("name"))
		self.verticalLayout.addWidget(self.name)
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
		self.serverstart.setText(_translate("Form", "Start Server", None))
		self.stopserver.setText(_translate("Form", "Stop Server", None))
		self.name.setText(_translate("Form", "Show Computer Name", None))
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