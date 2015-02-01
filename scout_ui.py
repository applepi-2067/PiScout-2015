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
		self.server_address = None
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
		self.addpt_btn = QtGui.QPushButton(Form)
		self.sync_btn.setObjectName(_fromUtf8("sync_btn"))
		self.verticalLayout.addWidget(self.sync_btn)
		self.verticalLayout_2.addLayout(self.verticalLayout)

		self.retranslateUi(Form)
		QtCore.QMetaObject.connectSlotsByName(Form)

	def retranslateUi(self, Form):
		Form.setWindowTitle(_translate("Form", "PiScout", None))
		self.open_btn.setText(_translate("Form", "Open file", None))
		self.open_btn.clicked.connect(self.openfile)
		self.addpt_btn.setText(_translate("Form", "Add point", None))
		self.addpt_btn.clicked.connect(self.addpt)
		self.sync_btn.setText(_translate("Form", "Sync with server", None))
		self.sync_btn.clicked.connect(self.sync)
	
	def openfile(self):
		try:
			f = open('points.txt','rt')
		except FileNotFoundError:
			f = open('points.txt', 'wt')
		print(sys.argv[0])
	
	def addpt(self):
		with open('points.txt','r+', encoding='ASCII') as f:
			buffer = f.read(16) #wot2hek is this point adding stuff
			if buffer.isnumeric():
				f.seek(0)
				points = int(f.read(16)) 
				points += 1 
				f.write(str(points)) 
				print('Added 1 point')
			elif buffer == '':
				print('File is empty. Adding 1 point.')
				f.write('1')
			else:
				print('Invalid characters in file. Replacing with 1 point.')
				f.truncate()
				with open('points.txt','w+', encoding='ASCII') as f:
					f.write('1')
					
	def sync(self):
		print('searching for server')
		nearby_devices = bluetooth.discover_devices()

		for address in nearby_devices:
			if bluetooth.lookup_name(address, 8) == 'APPLEPI-PC': #CHANGE TO SERVER NAME
				server_address = address
				break

		if server_address is not None:
			print('found server with address', server_address)
		else:
			print('could not find server')
			return

		socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
		socket.connect((server_address, 27))
		print('successfully connected to server')

		msg = 'ohai'
		socket.send(msg)
		print('sent: ', msg)

		socket.close()


if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	ex = Ui_Form()
	ex.show()
	sys.exit(app.exec_())
