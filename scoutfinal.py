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
		self.FIELDNAMES = [
		'match',
		'team',
		'auto totes',
		'auto rc',
		'auto rc from step',
		'auto stack?',
		'auto moved?',
		'auto comments',
		'litter in rc',
		'litter in landfill',
		'totes from step',
		'rc from step',
		'tote locations',
		'coop totes',
		'coop stack?',
		'teleop comments'
		]

	def setupUi(self, Form):
		Form.setObjectName(_fromUtf8("Form"))
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
		Form.resize(708, 740)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
		Form.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setPointSize(8)
		Form.setFont(font)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(_fromUtf8("piscoutlogo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		Form.setWindowIcon(icon)
		Form.setLayoutDirection(QtCore.Qt.LeftToRight)
		self.gridLayout_2 = QtGui.QGridLayout(Form)
		self.gridLayout_2.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
		self.gridLayout_2.setContentsMargins(-1, -1, 9, -1)
		self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
		self.horizontalLayout_11 = QtGui.QHBoxLayout()
		self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))
		self.teamnumfield_f = QtGui.QLineEdit(Form)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.teamnumfield_f.sizePolicy().hasHeightForWidth())
		self.teamnumfield_f.setSizePolicy(sizePolicy)
		self.teamnumfield_f.setObjectName(_fromUtf8("teamnumfield_f"))
		self.horizontalLayout_11.addWidget(self.teamnumfield_f)
		self.matchnumfield_f = QtGui.QLineEdit(Form)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.matchnumfield_f.sizePolicy().hasHeightForWidth())
		self.matchnumfield_f.setSizePolicy(sizePolicy)
		self.matchnumfield_f.setObjectName(_fromUtf8("matchnumfield_f"))
		self.horizontalLayout_11.addWidget(self.matchnumfield_f)
		self.gridLayout_2.addLayout(self.horizontalLayout_11, 18, 0, 1, 4)
		self.horizontalLayout_10 = QtGui.QHBoxLayout()
		self.horizontalLayout_10.setSpacing(6)
		self.horizontalLayout_10.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
		self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
		self.submitmatchstack_f = QtGui.QPushButton(Form)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.submitmatchstack_f.sizePolicy().hasHeightForWidth())
		self.submitmatchstack_f.setSizePolicy(sizePolicy)
		self.submitmatchstack_f.setObjectName(_fromUtf8("submitmatchstack_f"))
		self.horizontalLayout_10.addWidget(self.submitmatchstack_f)
		self.gridLayout_2.addLayout(self.horizontalLayout_10, 18, 4, 1, 1)
		self.verticalLayout_2 = QtGui.QVBoxLayout()
		self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
		self.overallrate = QtGui.QLCDNumber(Form)
		self.overallrate.setObjectName(_fromUtf8("overallrate"))
		self.verticalLayout_2.addWidget(self.overallrate)
		self.gridLayout_2.addLayout(self.verticalLayout_2, 16, 4, 1, 1)
		self.horizontalLayout_5 = QtGui.QHBoxLayout()
		self.horizontalLayout_5.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
		self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
		self.label_6 = QtGui.QLabel(Form)
		font = QtGui.QFont()
		font.setPointSize(16)
		self.label_6.setFont(font)
		self.label_6.setAlignment(QtCore.Qt.AlignCenter)
		self.label_6.setObjectName(_fromUtf8("label_6"))
		self.horizontalLayout_5.addWidget(self.label_6)
		spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout_5.addItem(spacerItem)
		self.label_5 = QtGui.QLabel(Form)
		font = QtGui.QFont()
		font.setPointSize(16)
		self.label_5.setFont(font)
		self.label_5.setAlignment(QtCore.Qt.AlignCenter)
		self.label_5.setObjectName(_fromUtf8("label_5"))
		self.horizontalLayout_5.addWidget(self.label_5)
		self.gridLayout_2.addLayout(self.horizontalLayout_5, 8, 1, 1, 4)
		self.horizontalLayout_6 = QtGui.QHBoxLayout()
		self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
		self.steptotes_f = QtGui.QSpinBox(Form)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
		sizePolicy.setHorizontalStretch(1)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.steptotes_f.sizePolicy().hasHeightForWidth())
		self.steptotes_f.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setPointSize(24)
		font.setBold(False)
		font.setItalic(False)
		font.setUnderline(False)
		font.setWeight(50)
		font.setStrikeOut(False)
		font.setKerning(True)
		font.setStyleStrategy(QtGui.QFont.PreferDefault)
		self.steptotes_f.setFont(font)
		self.steptotes_f.setAlignment(QtCore.Qt.AlignCenter)
		self.steptotes_f.setButtonSymbols(QtGui.QAbstractSpinBox.UpDownArrows)
		self.steptotes_f.setAccelerated(True)
		self.steptotes_f.setMaximum(12)
		self.steptotes_f.setObjectName(_fromUtf8("steptotes_f"))
		self.horizontalLayout_6.addWidget(self.steptotes_f)
		spacerItem1 = QtGui.QSpacerItem(250, 20, QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout_6.addItem(spacerItem1)
		self.containertotes_f = QtGui.QSpinBox(Form)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
		sizePolicy.setHorizontalStretch(1)
		sizePolicy.setVerticalStretch(1)
		sizePolicy.setHeightForWidth(self.containertotes_f.sizePolicy().hasHeightForWidth())
		self.containertotes_f.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setPointSize(24)
		font.setBold(False)
		font.setItalic(False)
		font.setUnderline(False)
		font.setWeight(50)
		font.setStrikeOut(False)
		font.setKerning(True)
		font.setStyleStrategy(QtGui.QFont.PreferDefault)
		self.containertotes_f.setFont(font)
		self.containertotes_f.setAlignment(QtCore.Qt.AlignCenter)
		self.containertotes_f.setButtonSymbols(QtGui.QAbstractSpinBox.UpDownArrows)
		self.containertotes_f.setAccelerated(True)
		self.containertotes_f.setMaximum(4)
		self.containertotes_f.setObjectName(_fromUtf8("containertotes_f"))
		self.horizontalLayout_6.addWidget(self.containertotes_f)
		self.gridLayout_2.addLayout(self.horizontalLayout_6, 11, 1, 1, 4)
		self.horizontalLayout_7 = QtGui.QHBoxLayout()
		self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
		self.label_15 = QtGui.QLabel(Form)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
		self.label_15.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setPointSize(16)
		self.label_15.setFont(font)
		self.label_15.setAlignment(QtCore.Qt.AlignCenter)
		self.label_15.setObjectName(_fromUtf8("label_15"))
		self.horizontalLayout_7.addWidget(self.label_15)
		spacerItem2 = QtGui.QSpacerItem(40, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout_7.addItem(spacerItem2)
		self.label_16 = QtGui.QLabel(Form)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
		self.label_16.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setPointSize(16)
		self.label_16.setFont(font)
		self.label_16.setAlignment(QtCore.Qt.AlignCenter)
		self.label_16.setObjectName(_fromUtf8("label_16"))
		self.horizontalLayout_7.addWidget(self.label_16)
		self.gridLayout_2.addLayout(self.horizontalLayout_7, 10, 1, 1, 4)
		self.verticalLayout_6 = QtGui.QVBoxLayout()
		self.verticalLayout_6.setSizeConstraint(QtGui.QLayout.SetFixedSize)
		self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
		self.label_18 = QtGui.QLabel(Form)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_18.sizePolicy().hasHeightForWidth())
		self.label_18.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setPointSize(12)
		self.label_18.setFont(font)
		self.label_18.setAlignment(QtCore.Qt.AlignCenter)
		self.label_18.setObjectName(_fromUtf8("label_18"))
		self.verticalLayout_6.addWidget(self.label_18)
		self.toteloc_f = QtGui.QSlider(Form)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.toteloc_f.sizePolicy().hasHeightForWidth())
		self.toteloc_f.setSizePolicy(sizePolicy)
		self.toteloc_f.setMaximum(10)
		self.toteloc_f.setSliderPosition(5)
		self.toteloc_f.setOrientation(QtCore.Qt.Horizontal)
		self.toteloc_f.setTickPosition(QtGui.QSlider.TicksBothSides)
		self.toteloc_f.setTickInterval(1)
		self.toteloc_f.setObjectName(_fromUtf8("toteloc_f"))
		self.verticalLayout_6.addWidget(self.toteloc_f)
		self.gridLayout_2.addLayout(self.verticalLayout_6, 12, 3, 2, 2)
		self.verticalLayout = QtGui.QVBoxLayout()
		self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
		self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
		self.label_7 = QtGui.QLabel(Form)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
		self.label_7.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setPointSize(20)
		font.setBold(True)
		font.setWeight(75)
		self.label_7.setFont(font)
		self.label_7.setAlignment(QtCore.Qt.AlignCenter)
		self.label_7.setObjectName(_fromUtf8("label_7"))
		self.verticalLayout.addWidget(self.label_7)
		self.can_f = QtGui.QLabel(Form)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.can_f.sizePolicy().hasHeightForWidth())
		self.can_f.setSizePolicy(sizePolicy)
		self.can_f.setMaximumSize(QtCore.QSize(229, 104))
		self.can_f.setText(_fromUtf8(""))
		self.can_f.setPixmap(QtGui.QPixmap(_fromUtf8("can.png")))
		self.can_f.setScaledContents(True)
		self.can_f.setObjectName(_fromUtf8("can_f"))
		self.verticalLayout.addWidget(self.can_f)
		self.tote6_f = QtGui.QLabel(Form)
		self.tote6_f.setMaximumSize(QtCore.QSize(229, 52))
		self.tote6_f.setText(_fromUtf8(""))
		self.tote6_f.setPixmap(QtGui.QPixmap(_fromUtf8("tote.png")))
		self.tote6_f.setScaledContents(True)
		self.tote6_f.setObjectName(_fromUtf8("tote6_f"))
		self.verticalLayout.addWidget(self.tote6_f)
		self.tote5_f = QtGui.QLabel(Form)
		self.tote5_f.setMaximumSize(QtCore.QSize(229, 52))
		self.tote5_f.setText(_fromUtf8(""))
		self.tote5_f.setPixmap(QtGui.QPixmap(_fromUtf8("tote.png")))
		self.tote5_f.setScaledContents(True)
		self.tote5_f.setObjectName(_fromUtf8("tote5_f"))
		self.verticalLayout.addWidget(self.tote5_f)
		self.tote4_f = QtGui.QLabel(Form)
		self.tote4_f.setMaximumSize(QtCore.QSize(229, 51))
		self.tote4_f.setText(_fromUtf8(""))
		self.tote4_f.setPixmap(QtGui.QPixmap(_fromUtf8("tote.png")))
		self.tote4_f.setScaledContents(True)
		self.tote4_f.setObjectName(_fromUtf8("tote4_f"))
		self.verticalLayout.addWidget(self.tote4_f)
		self.tote3_f = QtGui.QLabel(Form)
		self.tote3_f.setMaximumSize(QtCore.QSize(229, 52))
		self.tote3_f.setText(_fromUtf8(""))
		self.tote3_f.setPixmap(QtGui.QPixmap(_fromUtf8("tote.png")))
		self.tote3_f.setScaledContents(True)
		self.tote3_f.setObjectName(_fromUtf8("tote3_f"))
		self.verticalLayout.addWidget(self.tote3_f)
		self.tote2_f = QtGui.QLabel(Form)
		self.tote2_f.setMaximumSize(QtCore.QSize(229, 52))
		self.tote2_f.setText(_fromUtf8(""))
		self.tote2_f.setPixmap(QtGui.QPixmap(_fromUtf8("tote.png")))
		self.tote2_f.setScaledContents(True)
		self.tote2_f.setObjectName(_fromUtf8("tote2_f"))
		self.verticalLayout.addWidget(self.tote2_f)
		self.tote1_f = QtGui.QLabel(Form)
		self.tote1_f.setMaximumSize(QtCore.QSize(229, 52))
		self.tote1_f.setText(_fromUtf8(""))
		self.tote1_f.setPixmap(QtGui.QPixmap(_fromUtf8("tote.png")))
		self.tote1_f.setScaledContents(True)
		self.tote1_f.setObjectName(_fromUtf8("tote1_f"))
		self.verticalLayout.addWidget(self.tote1_f)
		self.submitstack_f = QtGui.QPushButton(Form)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.submitstack_f.sizePolicy().hasHeightForWidth())
		self.submitstack_f.setSizePolicy(sizePolicy)
		self.submitstack_f.setObjectName(_fromUtf8("submitstack_f"))
		self.verticalLayout.addWidget(self.submitstack_f)
		self.gridLayout_2.addLayout(self.verticalLayout, 8, 0, 7, 1)
		self.verticalLayout_8 = QtGui.QVBoxLayout()
		self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
		self.coopstackchkbox_f = QtGui.QCheckBox(Form)
		font = QtGui.QFont()
		font.setPointSize(12)
		self.coopstackchkbox_f.setFont(font)
		self.coopstackchkbox_f.setTristate(False)
		self.coopstackchkbox_f.setObjectName(_fromUtf8("coopstackchkbox_f"))
		self.verticalLayout_8.addWidget(self.coopstackchkbox_f)
		self.gridLayout_2.addLayout(self.verticalLayout_8, 13, 1, 1, 2)
		self.verticalLayout_7 = QtGui.QVBoxLayout()
		self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
		self.label_19 = QtGui.QLabel(Form)
		font = QtGui.QFont()
		font.setPointSize(16)
		self.label_19.setFont(font)
		self.label_19.setAlignment(QtCore.Qt.AlignCenter)
		self.label_19.setObjectName(_fromUtf8("label_19"))
		self.verticalLayout_7.addWidget(self.label_19)
		self.coop_f = QtGui.QSpinBox(Form)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
		sizePolicy.setHorizontalStretch(1)
		sizePolicy.setVerticalStretch(1)
		sizePolicy.setHeightForWidth(self.coop_f.sizePolicy().hasHeightForWidth())
		self.coop_f.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setPointSize(24)
		font.setBold(False)
		font.setItalic(False)
		font.setUnderline(False)
		font.setWeight(50)
		font.setStrikeOut(False)
		font.setKerning(True)
		font.setStyleStrategy(QtGui.QFont.PreferDefault)
		self.coop_f.setFont(font)
		self.coop_f.setAlignment(QtCore.Qt.AlignCenter)
		self.coop_f.setButtonSymbols(QtGui.QAbstractSpinBox.UpDownArrows)
		self.coop_f.setAccelerated(True)
		self.coop_f.setMaximum(4)
		self.coop_f.setObjectName(_fromUtf8("coop_f"))
		self.verticalLayout_7.addWidget(self.coop_f)
		self.gridLayout_2.addLayout(self.verticalLayout_7, 12, 1, 1, 2)
		self.horizontalLayout_4 = QtGui.QHBoxLayout()
		self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
		self.containerlitter_f = QtGui.QSpinBox(Form)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
		sizePolicy.setHorizontalStretch(1)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.containerlitter_f.sizePolicy().hasHeightForWidth())
		self.containerlitter_f.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setPointSize(24)
		font.setBold(False)
		font.setItalic(False)
		font.setUnderline(False)
		font.setWeight(50)
		font.setStrikeOut(False)
		font.setKerning(True)
		font.setStyleStrategy(QtGui.QFont.PreferDefault)
		self.containerlitter_f.setFont(font)
		self.containerlitter_f.setAlignment(QtCore.Qt.AlignCenter)
		self.containerlitter_f.setButtonSymbols(QtGui.QAbstractSpinBox.UpDownArrows)
		self.containerlitter_f.setAccelerated(True)
		self.containerlitter_f.setMaximum(7)
		self.containerlitter_f.setObjectName(_fromUtf8("containerlitter_f"))
		self.horizontalLayout_4.addWidget(self.containerlitter_f)
		spacerItem3 = QtGui.QSpacerItem(250, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout_4.addItem(spacerItem3)
		self.landfilllitter_f = QtGui.QSpinBox(Form)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
		sizePolicy.setHorizontalStretch(1)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.landfilllitter_f.sizePolicy().hasHeightForWidth())
		self.landfilllitter_f.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setPointSize(24)
		font.setBold(False)
		font.setItalic(False)
		font.setUnderline(False)
		font.setWeight(50)
		font.setStrikeOut(False)
		font.setKerning(True)
		font.setStyleStrategy(QtGui.QFont.PreferDefault)
		self.landfilllitter_f.setFont(font)
		self.landfilllitter_f.setAlignment(QtCore.Qt.AlignCenter)
		self.landfilllitter_f.setButtonSymbols(QtGui.QAbstractSpinBox.UpDownArrows)
		self.landfilllitter_f.setAccelerated(True)
		self.landfilllitter_f.setMaximum(20)
		self.landfilllitter_f.setObjectName(_fromUtf8("landfilllitter_f"))
		self.horizontalLayout_4.addWidget(self.landfilllitter_f)
		self.gridLayout_2.addLayout(self.horizontalLayout_4, 9, 1, 1, 4)
		self.horizontalLayout = QtGui.QHBoxLayout()
		self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
		self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
		self.autototes_f = QtGui.QSpinBox(Form)
		self.autototes_f.setEnabled(True)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
		sizePolicy.setHorizontalStretch(1)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.autototes_f.sizePolicy().hasHeightForWidth())
		self.autototes_f.setSizePolicy(sizePolicy)
		self.autototes_f.setMinimumSize(QtCore.QSize(0, 0))
		self.autototes_f.setSizeIncrement(QtCore.QSize(0, 0))
		self.autototes_f.setBaseSize(QtCore.QSize(0, 0))
		font = QtGui.QFont()
		font.setFamily(_fromUtf8("MS Shell Dlg 2"))
		font.setPointSize(24)
		font.setBold(False)
		font.setWeight(50)
		self.autototes_f.setFont(font)
		self.autototes_f.setAutoFillBackground(False)
		self.autototes_f.setStyleSheet(_fromUtf8(""))
		self.autototes_f.setAlignment(QtCore.Qt.AlignCenter)
		self.autototes_f.setAccelerated(True)
		self.autototes_f.setCorrectionMode(QtGui.QAbstractSpinBox.CorrectToPreviousValue)
		self.autototes_f.setMaximum(3)
		self.autototes_f.setObjectName(_fromUtf8("autototes_f"))
		self.horizontalLayout.addWidget(self.autototes_f)
		spacerItem4 = QtGui.QSpacerItem(150, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout.addItem(spacerItem4)
		self.autocontainers_f = QtGui.QSpinBox(Form)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
		sizePolicy.setHorizontalStretch(1)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.autocontainers_f.sizePolicy().hasHeightForWidth())
		self.autocontainers_f.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setPointSize(24)
		font.setBold(False)
		font.setItalic(False)
		font.setUnderline(False)
		font.setWeight(50)
		font.setStrikeOut(False)
		font.setKerning(True)
		font.setStyleStrategy(QtGui.QFont.PreferDefault)
		self.autocontainers_f.setFont(font)
		self.autocontainers_f.setAutoFillBackground(False)
		self.autocontainers_f.setStyleSheet(_fromUtf8(""))
		self.autocontainers_f.setAlignment(QtCore.Qt.AlignCenter)
		self.autocontainers_f.setButtonSymbols(QtGui.QAbstractSpinBox.UpDownArrows)
		self.autocontainers_f.setAccelerated(True)
		self.autocontainers_f.setMaximum(7)
		self.autocontainers_f.setObjectName(_fromUtf8("autocontainers_f"))
		self.horizontalLayout.addWidget(self.autocontainers_f)
		spacerItem5 = QtGui.QSpacerItem(150, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout.addItem(spacerItem5)
		self.autostepcontainers_f = QtGui.QSpinBox(Form)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
		sizePolicy.setHorizontalStretch(1)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.autostepcontainers_f.sizePolicy().hasHeightForWidth())
		self.autostepcontainers_f.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setPointSize(24)
		self.autostepcontainers_f.setFont(font)
		self.autostepcontainers_f.setAutoFillBackground(False)
		self.autostepcontainers_f.setStyleSheet(_fromUtf8(""))
		self.autostepcontainers_f.setAlignment(QtCore.Qt.AlignCenter)
		self.autostepcontainers_f.setAccelerated(True)
		self.autostepcontainers_f.setMaximum(4)
		self.autostepcontainers_f.setObjectName(_fromUtf8("autostepcontainers_f"))
		self.horizontalLayout.addWidget(self.autostepcontainers_f)
		self.gridLayout_2.addLayout(self.horizontalLayout, 2, 0, 1, 5)
		self.verticalLayout_12 = QtGui.QVBoxLayout()
		self.verticalLayout_12.setObjectName(_fromUtf8("verticalLayout_12"))
		self.teleopcomments_f = QtGui.QTextBrowser(Form)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.teleopcomments_f.sizePolicy().hasHeightForWidth())
		self.teleopcomments_f.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setPointSize(12)
		self.teleopcomments_f.setFont(font)
		self.teleopcomments_f.setUndoRedoEnabled(True)
		self.teleopcomments_f.setReadOnly(False)
		self.teleopcomments_f.setObjectName(_fromUtf8("teleopcomments_f"))
		self.verticalLayout_12.addWidget(self.teleopcomments_f)
		self.gridLayout_2.addLayout(self.verticalLayout_12, 14, 1, 1, 4)
		self.horizontalLayout_2 = QtGui.QHBoxLayout()
		self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
		self.label_4 = QtGui.QLabel(Form)
		font = QtGui.QFont()
		font.setPointSize(16)
		self.label_4.setFont(font)
		self.label_4.setAutoFillBackground(False)
		self.label_4.setStyleSheet(_fromUtf8(""))
		self.label_4.setAlignment(QtCore.Qt.AlignCenter)
		self.label_4.setObjectName(_fromUtf8("label_4"))
		self.horizontalLayout_2.addWidget(self.label_4)
		spacerItem6 = QtGui.QSpacerItem(40, 0, QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout_2.addItem(spacerItem6)
		self.label_3 = QtGui.QLabel(Form)
		font = QtGui.QFont()
		font.setPointSize(16)
		self.label_3.setFont(font)
		self.label_3.setAutoFillBackground(False)
		self.label_3.setStyleSheet(_fromUtf8(""))
		self.label_3.setAlignment(QtCore.Qt.AlignCenter)
		self.label_3.setObjectName(_fromUtf8("label_3"))
		self.horizontalLayout_2.addWidget(self.label_3)
		spacerItem7 = QtGui.QSpacerItem(40, 0, QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout_2.addItem(spacerItem7)
		self.label_2 = QtGui.QLabel(Form)
		font = QtGui.QFont()
		font.setPointSize(16)
		self.label_2.setFont(font)
		self.label_2.setAutoFillBackground(False)
		self.label_2.setStyleSheet(_fromUtf8(""))
		self.label_2.setAlignment(QtCore.Qt.AlignCenter)
		self.label_2.setObjectName(_fromUtf8("label_2"))
		self.horizontalLayout_2.addWidget(self.label_2)
		self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 0, 1, 5)
		self.horizontalLayout_3 = QtGui.QHBoxLayout()
		self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
		self.label = QtGui.QLabel(Form)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
		self.label.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setPointSize(24)
		font.setBold(True)
		font.setWeight(75)
		self.label.setFont(font)
		self.label.setAutoFillBackground(False)
		self.label.setStyleSheet(_fromUtf8(""))
		self.label.setAlignment(QtCore.Qt.AlignCenter)
		self.label.setObjectName(_fromUtf8("label"))
		self.horizontalLayout_3.addWidget(self.label)
		self.gridLayout_2.addLayout(self.horizontalLayout_3, 0, 0, 1, 5)
		self.verticalLayout_4 = QtGui.QVBoxLayout()
		self.verticalLayout_4.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
		self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
		self.autostackchkbox_f = QtGui.QCheckBox(Form)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.autostackchkbox_f.sizePolicy().hasHeightForWidth())
		self.autostackchkbox_f.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setPointSize(16)
		self.autostackchkbox_f.setFont(font)
		self.autostackchkbox_f.setAutoFillBackground(False)
		self.autostackchkbox_f.setStyleSheet(_fromUtf8(""))
		self.autostackchkbox_f.setIconSize(QtCore.QSize(16, 16))
		self.autostackchkbox_f.setObjectName(_fromUtf8("autostackchkbox_f"))
		self.verticalLayout_4.addWidget(self.autostackchkbox_f)
		self.autozonechkbox_f = QtGui.QCheckBox(Form)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.autozonechkbox_f.sizePolicy().hasHeightForWidth())
		self.autozonechkbox_f.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setPointSize(16)
		self.autozonechkbox_f.setFont(font)
		self.autozonechkbox_f.setAutoFillBackground(False)
		self.autozonechkbox_f.setStyleSheet(_fromUtf8(""))
		self.autozonechkbox_f.setChecked(False)
		self.autozonechkbox_f.setObjectName(_fromUtf8("autozonechkbox_f"))
		self.verticalLayout_4.addWidget(self.autozonechkbox_f)
		self.autocomments_f = QtGui.QTextEdit(Form)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.autocomments_f.sizePolicy().hasHeightForWidth())
		self.autocomments_f.setSizePolicy(sizePolicy)
		self.autocomments_f.setMaximumSize(QtCore.QSize(16777215, 80))
		font = QtGui.QFont()
		font.setPointSize(12)
		self.autocomments_f.setFont(font)
		self.autocomments_f.setAutoFillBackground(False)
		self.autocomments_f.setStyleSheet(_fromUtf8(""))
		self.autocomments_f.setFrameShape(QtGui.QFrame.StyledPanel)
		self.autocomments_f.setFrameShadow(QtGui.QFrame.Sunken)
		self.autocomments_f.setObjectName(_fromUtf8("autocomments_f"))
		self.verticalLayout_4.addWidget(self.autocomments_f)
		self.gridLayout_2.addLayout(self.verticalLayout_4, 4, 0, 1, 5)
		self.horizontalLayout_12 = QtGui.QHBoxLayout()
		self.horizontalLayout_12.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
		self.horizontalLayout_12.setObjectName(_fromUtf8("horizontalLayout_12"))
		self.label_25 = QtGui.QLabel(Form)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_25.sizePolicy().hasHeightForWidth())
		self.label_25.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setPointSize(12)
		self.label_25.setFont(font)
		self.label_25.setAlignment(QtCore.Qt.AlignCenter)
		self.label_25.setObjectName(_fromUtf8("label_25"))
		self.horizontalLayout_12.addWidget(self.label_25)
		self.label_24 = QtGui.QLabel(Form)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_24.sizePolicy().hasHeightForWidth())
		self.label_24.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setPointSize(12)
		self.label_24.setFont(font)
		self.label_24.setAlignment(QtCore.Qt.AlignCenter)
		self.label_24.setObjectName(_fromUtf8("label_24"))
		self.horizontalLayout_12.addWidget(self.label_24)
		self.gridLayout_2.addLayout(self.horizontalLayout_12, 16, 0, 1, 4)

		self.retranslateUi(Form)
		QtCore.QMetaObject.connectSlotsByName(Form)
		

	def retranslateUi(self, Form):
		Form.setWindowTitle(_translate("Form", "PiScout 2015: Non-release edition", None))
		self.teamnumfield_f.setPlaceholderText(_translate("Form", "Team number", None))
		self.matchnumfield_f.setPlaceholderText(_translate("Form", "Match number", None))
		self.submitmatchstack_f.setText(_translate("Form", "Submit match stats", None))
		self.submitmatchstack_f.clicked.connect(self.submitcsv)
		self.label_6.setText(_translate("Form", "Litter in containers", None))
		self.label_5.setText(_translate("Form", "Litter in landfill", None))
		self.label_15.setText(_translate("Form", "Totes from step", None))
		self.label_16.setText(_translate("Form", "Containers from step", None))
		self.label_18.setText(_translate("Form", "Tote locations\n"
"Left = All totes from human player\n"
"Middle = Equal mix\n"
"Right = All totes from landfill", None))
		self.toteloc_f.setValue(5)
		self.label_7.setText(_translate("Form", "Teleop", None))
		self.submitstack_f.setText(_translate("Form", "Submit stack", None))
		self.coopstackchkbox_f.setText(_translate("Form", "Got stacked set?", None))
		self.label_19.setText(_translate("Form", "Coopertition", None))
		#self.teleopcomments_f.setPlaceholderText(_translate("Form", "Comments on Teleop", None))
		self.label_4.setText(_translate("Form", "Totes in Auto Zone", None))
		self.label_3.setText(_translate("Form", "Containers in Auto Zone", None))
		self.label_2.setText(_translate("Form", "Containers from Step", None))
		self.label.setText(_translate("Form", "Autonomous", None))
		self.autostackchkbox_f.setText(_translate("Form", "Made stacked set?", None))
		self.autozonechkbox_f.setText(_translate("Form", "Moved into auto zone?", None))
		self.autocomments_f.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
		#self.autocomments_f.setPlaceholderText(_translate("Form", "Comments on autonomous", None))
		self.label_25.setText(_translate("Form", "Team number", None))
		self.label_24.setText(_translate("Form", "Match number", None))

		#Begin functions block
			
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
		server_socket.listen(1)
		print('listening for clients')

		server_socket.setblocking(0) #hopefully it can still connect to clients in non-blocking mode

		while not self.kill:
			client_socket = None
			try:
				client_socket, client_info = server_socket.accept()
			except OSError:
				sleep(0.2)
				continue
			name = bluetooth.lookup_name(client_info[0], 4)
			print('accepted connection from', name)
			data = str(client_socket.recv(2048))
			print('received ' + data + ' from ' + name)
			data = data[2:-1]
			proc = {}
			for i in range(0, len(data)):
				proc[self.FIELDNAMES[i]] = data[i]
			self.writecsv(proc)
			#SEND DATA BACK TO CLIENT
			client_socket.close()
			print('disconnected from', name)
			#in server main loop, also process the data from the clients

		print('closing server')
		server_socket.close()

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
	#We should use ands maybe or something to have all the errors in one box
	#i.e. user enters invalid for match, teamno and points so instead of 3 error boxes, have
	# one that just puts out all errors, will need to rewrite error handling 
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
			#idk m8 but without it it doesn't work

	#value grabbing functions
	#will optimize these functions later (?)


	def teamedit_fn(self):
		csvinput = self.teamnumfield_f.text()
		if csvinput.isnumeric():
			return csvinput
		else:
			self.errmessage(2)
			return False

	def matchedit_fn(self):
		csvinput = self.matchnumfield_f.text()
		if csvinput.isnumeric():
			return csvinput
		else:
			self.errmessage(1)
			return False

	#converts csv fields to dict and sends to writecsv
	def submitcsv(self):
		#Autonomous
		autototes = self.autototes_f.value()
		autocontainers = self.autocontainers_f.value()
		autostepcontainers = self.autostepcontainers_f.value()
		
		#checkbox checking functions
		autostackedset = self.autostackchkbox_f.isChecked()
		autozone = self.autozonechkbox_f.isChecked()
		
		autocomments = self.autocomments_f.toPlainText()
		
		#Teleop
		containerlitter = self.containerlitter_f.value()
		landfilllitter = self.landfilllitter_f.value()
		steptotes = self.steptotes_f.value()
		stepcontainers = self.containertotes_f.value()
		cooppoints = self.coop_f.value()
		coopstack = self.coopstackchkbox_f.isChecked()
		teleopcomments = self.teleopcomments_f.toPlainText()
		totelocations = self.toteloc_f.value()
		
		
		csvteam = self.teamedit_fn()
		csvmatch = self.matchedit_fn()
		if csvteam and csvmatch:
			fcsvinput = {
			'match': csvmatch,
			'team': csvteam,
			'auto totes': autototes,
			'auto rc': autocontainers,
			'auto rc from step': autostepcontainers,
			'auto stack?': autostackedset,
			'auto moved?': autozone,
			'auto comments': autocomments,
			'litter in rc': containerlitter,
			'litter in landfill': landfilllitter,
			'totes from step': steptotes,
			'rc from step': stepcontainers,
			'tote locations': totelocations,
			'coop totes': cooppoints,
			'coop stack?': coopstack,
			'teleop comments': teleopcomments
			}
			#overall = int(int(containerlitter) / int(stepcontainers) * int(steptotes) / 10)
			#self.overallrate.display(overall)
			self.writecsv(fcsvinput)

	#writes a csv to file
	def writecsv(self, csvinput):
		created = not isfile('points.csv')
		with open('points.csv', 'at') as csvfile:
			writecsv = csv.DictWriter(csvfile, self.FIELDNAMES, lineterminator = '\n') #fieldnames is defined in __init__
			if created: #only write the header if file has been newly created
				writecsv.writeheader()
			writecsv.writerow(csvinput)
			self.errmessage(0)
			

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	ex = Ui_Form()
	ex.show()
	sys.exit(app.exec_())

