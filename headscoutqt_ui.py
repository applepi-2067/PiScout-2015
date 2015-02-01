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
		self.startserver_btn = QtGui.QPushButton(Form)
		self.startserver_btn.setAutoDefault(True)
		self.startserver_btn.setDefault(True)
		self.startserver_btn.setObjectName(_fromUtf8("startserver_btn"))
		self.verticalLayout.addWidget(self.startserver_btn)
		
		self.stopserver_btn = QtGui.QPushButton(Form)
		self.stopserver_btn.setObjectName(_fromUtf8("stopserver_btn"))
		self.verticalLayout.addWidget(self.stopserver_btn)
		
		self.verticalLayout_2.addLayout(self.verticalLayout)

		self.retranslateUi(Form)
		QtCore.QMetaObject.connectSlotsByName(Form)

	def retranslateUi(self, Form):
		Form.setWindowTitle(_translate("Form", "PiScout BT Server", None))
		self.startserver_btn.setToolTip(_translate("Form", "Click to start the bluetooth server", None))
		self.startserver_btn.setText(_translate("Form", "Start PiScout Server", None))
		self.startserver_btn.clicked.connect(self.start_bluetooth_server)
		self.stopserver_btn.clicked.connect(self.kill_server)
		global kill #can i do this
		kill = False

	def kill_server(self):
		global kill
		kill = True
                
	def start_bluetooth_server(self):
		Thread(target = self.bluetooth_server).start()
		
	queue = Queue() #suspicious as heck, not sure if this will get called ever (idk how to python)
	def bluetooth_server(self):
		global kill
		kill = False
		
		print('started new thread for server')
		server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
		server_socket.bind(("", 27))
		print('server started')
		server_socket.listen(2)
		print('listening for clients')
	
		#figure out how to add a button to break from this loop
		#also make it so that this doesnt cause the GUI to hang
		server_socket.setblocking(0) #hopefully it can still connect to clients in non-blocking mode
		
		global queue #make a queue for incoming client data
		queue = Queue()
		
		while kill == False:
			try:
				client_socket, client_info = server_socket.accept();
				name = bluetooth.lookup_name(client_info[0], 4)
				print('accepted connection from', name);
				Thread(target = self.client_handler, args = [client_socket, name]).start()		
			except: #will throw exceptions constantly until client is found (i hope)
				sleep(0.2)
			
			#in server main loop, also process the data from the clients
			if not queue.empty():
				print('reading data from queue')
				self.process(queue.get())
				
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
				
				global queue
				queue.put(data)
				print('data added to queue')
	
	
	def process(self, data):
		print('processing data: ', data)

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	ex = Ui_Form()
	ex.show()
	sys.exit(app.exec_())
