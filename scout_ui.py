# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'scout.ui'
#
# Created: Sat Jan 31 12:41:13 2015
#	   by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import sys
import os.path

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
		Form.resize(400, 300)
		self.verticalLayout_2 = QtGui.QVBoxLayout(Form)
		self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
		self.verticalLayout = QtGui.QVBoxLayout()
		self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
		self.open_btn = QtGui.QPushButton(Form)
		self.open_btn.setObjectName(_fromUtf8("open_btn"))
		self.verticalLayout.addWidget(self.open_btn)
		self.addpt_btn = QtGui.QPushButton(Form)
		self.addpt_btn.setObjectName(_fromUtf8("addpt_btn"))
		self.verticalLayout.addWidget(self.addpt_btn)
		self.verticalLayout_2.addLayout(self.verticalLayout)

		self.retranslateUi(Form)
		QtCore.QMetaObject.connectSlotsByName(Form)

	def retranslateUi(self, Form):
		Form.setWindowTitle(_translate("Form", "Apple Pi Scouter", None))
		self.open_btn.setText(_translate("Form", "Open file", None))
		self.open_btn.clicked.connect(self.openfile)
		self.addpt_btn.setText(_translate("Form", "Add point", None))
		self.addpt_btn.clicked.connect(self.addpt)
	
	def openfile(self):
		try:
			f = open('points.txt','r+')
		except FileNotFoundError:
			f = open('points.txt', 'w+')
		print(sys.argv[0])
	
	def addpt(self):
		path = sys.argv[1] if len(sys.argv) > 1 else 'points.txt' 
			
		if not os.path.exists(path):
			print('that points file does not exist')
			sys.exit(2)
	 
			file = open(path, 'rt', encoding='ASCII')
			buffer = file.read(16)
			file.close()
			if buffer.isnumeric():
					points = int(buffer)
					print(points)
			elif buffer == '':
					print('points file is empty; putting 1 point in it')
					file = open(path, 'wt', encoding='ASCII')
					file.write('1')
					file.close()
					sys.exit(-1)
			else:
					print('this file does not appear to be a points file')
					sys.exit(3)

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	ex = Ui_Form()
	ex.show()
	sys.exit(app.exec_())
