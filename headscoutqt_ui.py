# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'headscoutqt.ui'
#
# Created: Sun Feb	1 00:30:05 2015
#	   by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from queue import Queue
from threading import Thread
from time import sleep
import bluetooth
import sys
import random
import csv
#import pandas as pd

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
		
		QPushButton  {
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
		#add point button
		self.addpoint_btn = QtGui.QPushButton(Form)
		self.addpoint_btn.setObjectName(_fromUtf8("addpoint_btn"))
		self.verticalLayout.addWidget(self.addpoint_btn)
		#readcsv
		self.readcsv_btn = QtGui.QPushButton(Form)
		self.readcsv_btn.setObjectName(_fromUtf8("readcsv_btn"))
		self.verticalLayout.addWidget(self.readcsv_btn)
		#csv input form line
		self.textcsvin = QtGui.QLineEdit(Form)
		self.textcsvin.setObjectName(_fromUtf8("text"))
		self.verticalLayout.addWidget(self.textcsvin)
		#csv input button
		self.buttonsubmit = QtGui.QPushButton(Form)
		self.buttonsubmit.setObjectName(_fromUtf8("buttonsubmit"))
		self.verticalLayout.addWidget(self.buttonsubmit)

		self.verticalLayout_2.addLayout(self.verticalLayout)

		self.retranslateUi(Form)
		QtCore.QMetaObject.connectSlotsByName(Form)

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
		#add point button
		self.addpoint_btn.setText(_translate("Form", "Add point", None))
		self.addpoint_btn.clicked.connect(self.addpoint)
		#read csv
		self.readcsv_btn.setText(_translate("Form", "Read points.csv", None))
		self.readcsv_btn.clicked.connect(self.readcsv)
		#input button
		self.buttonsubmit.setText(_translate("Form", "put text", None))
		self.buttonsubmit.clicked.connect(self.submitcsv)

		
	def kill_server(self):
		self.kill = True
		while self.step > 0:
			sleep(.01)
			self.timer.start(100, self)
			self.step = self.step - 1
			self.progressBar.setProperty("value", self.step)

	def start_bluetooth_server(self):
		if not self.kill:
			return

		self.kill = False
		Thread(target = self.bluetooth_server).start()
		while self.step < 100:
			sleep(.01)
			self.timer.start(100, self)
			self.step = self.step + 1
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
		
		while self.kill == False:
			try:
				client_socket, client_info = server_socket.accept();
				name = bluetooth.lookup_name(client_info[0], 4)
				print('accepted connection from', name);
				Thread(target = self.client_handler, args = [client_socket, name]).start()		
			except: #will throw exceptions constantly until client is found (i hope)
				sleep(0.2)
			
			#in server main loop, also process the data from the clients
			if not self.queue.empty():
				print('reading data from queue')
				self.process(self.queue.get())
				
		print('closing server')
		#what to heck is this trash
		#data = client_socket.recv(1024);
		#print("received:", data)
		#client_socket.close()
	
		server_socket.close()
	
	def client_handler(self, client_socket, name):
		print('started new thread for client', name)
		while True:
			data = client_socket.recv(1024)
			if len(data) > 1:
				print('%s: %s' % (name, data))
				
				if data == 'close':
					client_socket.close()
					print('disconnected from', name)
					break
				
				self.queue.put(data)
				print('data added to queue')
	
	
	def process(self, data):
		print('processing data: ', data)
	
	#points system block thing
	def addpoint(self):
		pass
	
	def submitcsv(self):
		with open('points.csv', 'at') as csvfile:
			writecsv = csv.DictWriter(csvfile)
			csvinput = self.textcsvin.text()
			writecsv.writeheader()
			writecsv.writerow([csvinput])
			
	def readcsv(self):
		with open('points.csv', 'r') as csvfile:
			pointscsv = csv.DictReader(csvfile)
			for row in pointscsv:
				print(row['Match'],row['Team Number'],row['Points'])
			print('--------')
			csvfile.close()
			#experimental pandas stuff ignoreplz
			#pointscsv = pd.read_csv(csvfile)
			#names = df.Names
			#print(names)


if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	ex = Ui_Form()
	ex.show()
	sys.exit(app.exec_())
