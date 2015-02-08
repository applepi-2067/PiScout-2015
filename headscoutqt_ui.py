# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'headscoutqt.ui'
#
# Created: Sun Feb	1 00:30:05 2015
#	   by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from os.path import isfile
from queue import Queue
from threading import Thread
from time import sleep
import bluetooth
import sys
import csv

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
		self.kill = True
		self.queue = Queue() #queue for incoming client data
		self.FIELDNAMES = ['Match', 'Team Number', 'Points']

	def setupUi(self, Form):
		Form.setObjectName(_fromUtf8("Form"))
		Form.resize(400, 300)
		Form.setStyleSheet(_fromUtf8('''
		#Form {
			background: grey;
		}
		#verticalLayout {
			border: 3px solid gray; border-radius: 40px; background: white;
		}

		QPushButton	 {
			background-color:#599bb3;
			border-radius:8px;
			color:#ffffff;
			font-family:arial;
			font-size:20px;
			font-weight:bold;
			padding:13px 32px;
			text-decoration:none;
			}
			QPushButton :hover {
				background-color:#408c99;
			}

			QPushButton :active {
				position:relative;
				top:1px;
			}

		'''

		))

		self.verticalLayout_2 = QtGui.QVBoxLayout(Form)
		self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
		self.verticalLayout = QtGui.QVBoxLayout()
		self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))

		#server start button
		self.startserver_btn = QtGui.QPushButton(Form)
		self.startserver_btn.setAutoDefault(True)
		self.startserver_btn.setDefault(True)
		self.startserver_btn.setObjectName(_fromUtf8("startserver_btn"))
		self.verticalLayout.addWidget(self.startserver_btn)

		#server stop button
		self.stopserver_btn = QtGui.QPushButton(Form)
		self.stopserver_btn.setObjectName(_fromUtf8("stopserver_btn"))
		self.verticalLayout.addWidget(self.stopserver_btn)

		#readcsv
		self.readcsv_btn = QtGui.QPushButton(Form)
		self.readcsv_btn.setObjectName(_fromUtf8("readcsv_btn"))
		self.verticalLayout.addWidget(self.readcsv_btn)

		#csv entry forms
		self.horizontalLayout = QtGui.QHBoxLayout()
		self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
		self.matchedit = QtGui.QLineEdit(Form)
		self.matchedit.setObjectName(_fromUtf8("matchedit"))
		self.horizontalLayout.addWidget(self.matchedit)
		self.matchspin = QtGui.QSpinBox(Form)
		self.matchspin.setObjectName(_fromUtf8("matchspin"))
		self.horizontalLayout.addWidget(self.matchspin)
		self.teamedit = QtGui.QLineEdit(Form)
		self.teamedit.setObjectName(_fromUtf8("teamedit"))
		self.horizontalLayout.addWidget(self.teamedit)
		self.teamspin = QtGui.QSpinBox(Form)
		self.teamspin.setObjectName(_fromUtf8("teamspin"))
		self.horizontalLayout.addWidget(self.teamspin)
		self.pointsedit = QtGui.QLineEdit(Form)
		self.pointsedit.setObjectName(_fromUtf8("pointsedit"))
		self.horizontalLayout.addWidget(self.pointsedit)
		self.pointspin = QtGui.QSpinBox(Form)
		self.pointspin.setObjectName(_fromUtf8("pointspin"))
		self.horizontalLayout.addWidget(self.pointspin)
		self.verticalLayout.addLayout(self.horizontalLayout)

		#csv input button
		self.buttonsubmit = QtGui.QPushButton(Form)
		self.buttonsubmit.setObjectName(_fromUtf8("buttonsubmit"))
		self.verticalLayout.addWidget(self.buttonsubmit)

		self.verticalLayout_2.addLayout(self.verticalLayout)

		self.retranslateUi(Form)
		QtCore.QMetaObject.connectSlotsByName(Form)
		#PyCharm thinks something is whack with the above line (Parameter 'QObject' unfilled

	def retranslateUi(self, Form):
		#window title
		Form.setWindowTitle(_translate("Form", "PiScout BT Server", None))

		#start server humaization thing
		self.startserver_btn.setToolTip(_translate("Form", "Click to start the bluetooth server", None))
		self.startserver_btn.setText(_translate("Form", "Start PiScout Server", None))
		self.startserver_btn.clicked.connect(self.start_bluetooth_server)

		#stop server humanizing text
		self.stopserver_btn.setToolTip(_translate("Form", "Click to stop the bluetooth server", None))
		self.stopserver_btn.setText(_translate("Form", "Stop PiScout Server", None))
		self.stopserver_btn.clicked.connect(self.kill_server)

		#baller progress bar
		self.progressBar = QtGui.QProgressBar(self)
		self.progressBar.setMaximum(100)
		self.progressBar.setProperty("value", 0)
		self.progressBar.setObjectName(_fromUtf8("progressBar"))
		self.verticalLayout.addWidget(self.progressBar)

		#pleb timer for pbar
		self.timer = QtCore.QBasicTimer()
		self.step = 0

		#read csv
		self.readcsv_btn.setText(_translate("Form", "Read points.csv", None))
		self.readcsv_btn.clicked.connect(self.readcsv)

		#csv text entry lines
		self.matchedit.setPlaceholderText(_translate("Form", "Match number", None))
		self.teamedit.setPlaceholderText(_translate("Form", "Team Number", None))
		self.pointsedit.setPlaceholderText(_translate("Form", "Points", None))

		#input button
		self.buttonsubmit.setText(_translate("Form", "put text", None))
		self.buttonsubmit.clicked.connect(self.submitcsv)

	def kill_server(self):
		self.kill = True
		while self.step > 0:
			sleep(.01)
			self.timer.start(100, self)
			self.step -= 1
			self.progressBar.setProperty("value", self.step)

	def start_bluetooth_server(self):
		if not self.kill:
			return

		self.kill = False
		Thread(target = self.bluetooth_server).start()
		while self.step < 100:
			sleep(.01)
			self.timer.start(100, self)
			self.step += 1
			self.progressBar.setProperty("value", self.step)

	def bluetooth_server(self):
		self.kill = False

		print('started new thread for server')
		server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
		server_socket.bind(("", 27))
		print('server started')
		server_socket.listen(2)
		print('listening for clients')

		server_socket.setblocking(0) #hopefully it can still connect to clients in non-blocking mode

		while not self.kill:
			try:
				client_socket, client_info = server_socket.accept()
				name = bluetooth.lookup_name(client_info[0], 4)
				print('accepted connection from', name)
				Thread(target = self.client_handler, args = [client_socket, name]).start()
			except: #will throw exceptions constantly until client is found (i hope)
				sleep(0.2)
			#in server main loop, also process the data from the clients
			if self.queue.empty():
				continue

			print('writing data to file')
			self.writecsv(self.queue.get())
			# a queue is used here to ensure that two clients on different
			# threads cannot attempt to modify points.csv at the same time

		print('closing server')
		#what to heck is this trash
		#data = client_socket.recv(1024);
		#print("received:", data)
		#client_socket.close()

		server_socket.close()

	def client_handler(self, client_socket, name):
		print('started new thread for client', name)
		while True:
			raw = client_socket.recv(1024)
			if len(raw) > 1:
				print('%s: %s' % (name, raw))
				if raw == 'close':
					client_socket.close()
					print('disconnected from', name)
					break
				data = str(raw).split("'")[1]
				proc = {}
                                for i in range(0, len(data)):
                                    proc[self.FIELDNAMES[i]] = data[i]
				self.queue.put(proc)
				print('data added to queue')

	def readcsv(self):
		if not isfile('points.csv'):
			self.errmessage(4)
			return
		with open('points.csv', 'r') as csvfile:
			pointscsv = csv.DictReader(csvfile)
			for row in pointscsv:
				print(row['Match'],row['Team Number'],row['Points'])
			print('--------')
			csvfile.close()

	#warning box
	#errors: 0 = success
	# 1 = bad match
	# 2 = bad team
	# 3 = bad points
	# 4 = doesn't exist
	# any other value: unknown
	def errmessage(self, errno):
			msgBox = QtGui.QMessageBox()
			if errno == 0:
				msgBox.setText('Write success.')
			elif errno == 1:
				msgBox.setText('Error: You entered non-numeric input for "Match"')
			elif errno == 2:
				msgBox.setText('Error: You entered non-numeric input for "Team Number"')
			elif errno == 3:
				msgBox.setText('Error: You entered non-numeric input for "Points"')
			elif errno == 4:
				msgBox.setText('Error: file does not exist\nSubmit some data to create a new file')
			else:
				msgBox.setText('Error: Unknown error')
			msgBox.addButton(QtGui.QPushButton('OK'), QtGui.QMessageBox.YesRole)
			ret = msgBox.exec_()
			#what does that variable do?

	#3x box grabbing functions
	#will optimize these functions later
	def pointsedit_fn(self):
		csvinput = self.pointsedit.text()
		if csvinput.isnumeric():
			return csvinput
		else:
			self.errmessage(3)
			return False

	def teamedit_fn(self):
		csvinput = self.teamedit.text()
		if csvinput.isnumeric():
			return csvinput
		else:
			self.errmessage(2)
			return False

	def matchedit_fn(self):
		csvinput = self.matchedit.text()
		if csvinput.isnumeric():
			return csvinput
		else:
			self.errmessage(1)
			return False

	#converts csv fields to dict and sends to writecsv
	def submitcsv(self):
		csvpoints = self.pointsedit_fn()
		csvteam = self.teamedit_fn()
		csvmatch = self.matchedit_fn()
		if csvpoints and csvteam and csvmatch:
			fcsvinput = {'Match': csvmatch, 'Team Number': csvteam, 'Points': csvpoints}
			self.writecsv(fcsvinput)

	#writes a csv to file
	def writecsv(self, csvinput):
		created = not isfile('points.csv')
		with open('points.csv', 'at') as csvfile:
			writecsv = csv.DictWriter(csvfile, self.FIELDNAMES) #fieldnames is defined in __init__
			if created: #only write the header if file has been newly created
				writecsv.writeheader()
			writecsv.writerow(csvinput)
			self.errmessage(0)


if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	ex = Ui_Form()
	ex.show()
	sys.exit(app.exec_())
