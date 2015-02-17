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
		Form.resize(994, 853)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(_fromUtf8("piscoutlogo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		Form.setWindowIcon(icon)
		Form.setLayoutDirection(QtCore.Qt.LeftToRight)
		self.gridLayout_2 = QtGui.QGridLayout(Form)
		self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
		self.verticalLayout_6 = QtGui.QVBoxLayout()
		self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
		self.label_18 = QtGui.QLabel(Form)
		font = QtGui.QFont()
		font.setPointSize(12)
		self.label_18.setFont(font)
		self.label_18.setAlignment(QtCore.Qt.AlignCenter)
		self.label_18.setObjectName(_fromUtf8("label_18"))
		self.verticalLayout_6.addWidget(self.label_18)
		self.drivingabilit_f = QtGui.QSlider(Form)
		self.drivingabilit_f.setMaximum(10)
		self.drivingabilit_f.setSliderPosition(5)
		self.drivingabilit_f.setOrientation(QtCore.Qt.Horizontal)
		self.drivingabilit_f.setTickPosition(QtGui.QSlider.TicksBothSides)
		self.drivingabilit_f.setTickInterval(1)
		self.drivingabilit_f.setObjectName(_fromUtf8("drivingabilit_f"))
		self.verticalLayout_6.addWidget(self.drivingabilit_f)
		self.label_17 = QtGui.QLabel(Form)
		font = QtGui.QFont()
		font.setPointSize(12)
		self.label_17.setFont(font)
		self.label_17.setAlignment(QtCore.Qt.AlignCenter)
		self.label_17.setObjectName(_fromUtf8("label_17"))
		self.verticalLayout_6.addWidget(self.label_17)
		self.harvestability_f = QtGui.QSlider(Form)
		self.harvestability_f.setMaximum(10)
		self.harvestability_f.setSliderPosition(5)
		self.harvestability_f.setOrientation(QtCore.Qt.Horizontal)
		self.harvestability_f.setInvertedAppearance(False)
		self.harvestability_f.setInvertedControls(False)
		self.harvestability_f.setTickPosition(QtGui.QSlider.TicksBothSides)
		self.harvestability_f.setTickInterval(1)
		self.harvestability_f.setObjectName(_fromUtf8("harvestability_f"))
		self.verticalLayout_6.addWidget(self.harvestability_f)
		self.gridLayout_2.addLayout(self.verticalLayout_6, 12, 3, 2, 2)
		self.verticalLayout_10 = QtGui.QVBoxLayout()
		self.verticalLayout_10.setObjectName(_fromUtf8("verticalLayout_10"))
		self.submitstack_f = QtGui.QPushButton(Form)
		self.submitstack_f.setObjectName(_fromUtf8("submitstack_f"))
		self.verticalLayout_10.addWidget(self.submitstack_f)
		self.gridLayout_2.addLayout(self.verticalLayout_10, 15, 0, 1, 1)
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
		self.verticalLayout_5 = QtGui.QVBoxLayout()
		self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
		self.autocomments_f = QtGui.QTextEdit(Form)
		font = QtGui.QFont()
		font.setPointSize(12)
		self.autocomments_f.setFont(font)
		self.autocomments_f.setAutoFillBackground(False)
		self.autocomments_f.setStyleSheet(_fromUtf8(""))
		self.autocomments_f.setFrameShape(QtGui.QFrame.StyledPanel)
		self.autocomments_f.setFrameShadow(QtGui.QFrame.Sunken)
		self.autocomments_f.setObjectName(_fromUtf8("autocomments_f"))
		self.verticalLayout_5.addWidget(self.autocomments_f)
		self.gridLayout_2.addLayout(self.verticalLayout_5, 3, 2, 1, 3)
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
		spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout_2.addItem(spacerItem)
		self.label_3 = QtGui.QLabel(Form)
		font = QtGui.QFont()
		font.setPointSize(16)
		self.label_3.setFont(font)
		self.label_3.setAutoFillBackground(False)
		self.label_3.setStyleSheet(_fromUtf8(""))
		self.label_3.setAlignment(QtCore.Qt.AlignCenter)
		self.label_3.setObjectName(_fromUtf8("label_3"))
		self.horizontalLayout_2.addWidget(self.label_3)
		spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout_2.addItem(spacerItem1)
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
		self.verticalLayout = QtGui.QVBoxLayout()
		self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
		self.can_f = QtGui.QLabel(Form)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
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
		self.gridLayout_2.addLayout(self.verticalLayout, 9, 0, 6, 1)
		self.horizontalLayout_12 = QtGui.QHBoxLayout()
		self.horizontalLayout_12.setObjectName(_fromUtf8("horizontalLayout_12"))
		self.label_25 = QtGui.QLabel(Form)
		font = QtGui.QFont()
		font.setPointSize(12)
		self.label_25.setFont(font)
		self.label_25.setAlignment(QtCore.Qt.AlignCenter)
		self.label_25.setObjectName(_fromUtf8("label_25"))
		self.horizontalLayout_12.addWidget(self.label_25)
		self.label_24 = QtGui.QLabel(Form)
		font = QtGui.QFont()
		font.setPointSize(12)
		self.label_24.setFont(font)
		self.label_24.setAlignment(QtCore.Qt.AlignCenter)
		self.label_24.setObjectName(_fromUtf8("label_24"))
		self.horizontalLayout_12.addWidget(self.label_24)
		self.gridLayout_2.addLayout(self.horizontalLayout_12, 16, 0, 1, 4)
		self.horizontalLayout_8 = QtGui.QHBoxLayout()
		self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
		self.metricfac1_f = QtGui.QLCDNumber(Form)
		self.metricfac1_f.setObjectName(_fromUtf8("metricfac1_f"))
		self.horizontalLayout_8.addWidget(self.metricfac1_f)
		self.metricfac2_f = QtGui.QLCDNumber(Form)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.metricfac2_f.sizePolicy().hasHeightForWidth())
		self.metricfac2_f.setSizePolicy(sizePolicy)
		self.metricfac2_f.setObjectName(_fromUtf8("metricfac2_f"))
		self.horizontalLayout_8.addWidget(self.metricfac2_f)
		self.overall_f = QtGui.QLCDNumber(Form)
		self.overall_f.setSegmentStyle(QtGui.QLCDNumber.Flat)
		self.overall_f.setObjectName(_fromUtf8("overall_f"))
		self.horizontalLayout_8.addWidget(self.overall_f)
		self.gridLayout_2.addLayout(self.horizontalLayout_8, 19, 0, 1, 5)
		self.horizontalLayout_6 = QtGui.QHBoxLayout()
		self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
		self.steptotes_f = QtGui.QSpinBox(Form)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(1)
		sizePolicy.setVerticalStretch(1)
		sizePolicy.setHeightForWidth(self.steptotes_f.sizePolicy().hasHeightForWidth())
		self.steptotes_f.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setPointSize(48)
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
		self.steptotes_f.setMaximum(20)
		self.steptotes_f.setObjectName(_fromUtf8("steptotes_f"))
		self.horizontalLayout_6.addWidget(self.steptotes_f)
		spacerItem2 = QtGui.QSpacerItem(250, 20, QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout_6.addItem(spacerItem2)
		self.containertotes_f = QtGui.QSpinBox(Form)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(1)
		sizePolicy.setVerticalStretch(1)
		sizePolicy.setHeightForWidth(self.containertotes_f.sizePolicy().hasHeightForWidth())
		self.containertotes_f.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setPointSize(48)
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
		self.horizontalLayout_11 = QtGui.QHBoxLayout()
		self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))
		self.teamnumfield_f = QtGui.QLineEdit(Form)
		self.teamnumfield_f.setObjectName(_fromUtf8("teamnumfield_f"))
		self.horizontalLayout_11.addWidget(self.teamnumfield_f)
		self.matchnumfield_f = QtGui.QLineEdit(Form)
		self.matchnumfield_f.setObjectName(_fromUtf8("matchnumfield_f"))
		self.horizontalLayout_11.addWidget(self.matchnumfield_f)
		self.gridLayout_2.addLayout(self.horizontalLayout_11, 17, 0, 1, 4)
		self.horizontalLayout_5 = QtGui.QHBoxLayout()
		self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
		self.label_6 = QtGui.QLabel(Form)
		font = QtGui.QFont()
		font.setPointSize(16)
		self.label_6.setFont(font)
		self.label_6.setAlignment(QtCore.Qt.AlignCenter)
		self.label_6.setObjectName(_fromUtf8("label_6"))
		self.horizontalLayout_5.addWidget(self.label_6)
		spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout_5.addItem(spacerItem3)
		self.label_5 = QtGui.QLabel(Form)
		font = QtGui.QFont()
		font.setPointSize(16)
		self.label_5.setFont(font)
		self.label_5.setAlignment(QtCore.Qt.AlignCenter)
		self.label_5.setObjectName(_fromUtf8("label_5"))
		self.horizontalLayout_5.addWidget(self.label_5)
		self.gridLayout_2.addLayout(self.horizontalLayout_5, 8, 1, 1, 4)
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
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(1)
		sizePolicy.setVerticalStretch(1)
		sizePolicy.setHeightForWidth(self.coop_f.sizePolicy().hasHeightForWidth())
		self.coop_f.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setPointSize(28)
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
		self.coop_f.setMaximum(20)
		self.coop_f.setObjectName(_fromUtf8("coop_f"))
		self.verticalLayout_7.addWidget(self.coop_f)
		self.gridLayout_2.addLayout(self.verticalLayout_7, 12, 1, 1, 2)
		self.verticalLayout_12 = QtGui.QVBoxLayout()
		self.verticalLayout_12.setObjectName(_fromUtf8("verticalLayout_12"))
		self.teleopcomments_f = QtGui.QTextBrowser(Form)
		font = QtGui.QFont()
		font.setPointSize(12)
		self.teleopcomments_f.setFont(font)
		self.teleopcomments_f.setObjectName(_fromUtf8("teleopcomments_f"))
		self.verticalLayout_12.addWidget(self.teleopcomments_f)
		self.gridLayout_2.addLayout(self.verticalLayout_12, 14, 1, 2, 4)
		self.horizontalLayout_7 = QtGui.QHBoxLayout()
		self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
		self.label_15 = QtGui.QLabel(Form)
		font = QtGui.QFont()
		font.setPointSize(16)
		self.label_15.setFont(font)
		self.label_15.setAlignment(QtCore.Qt.AlignCenter)
		self.label_15.setObjectName(_fromUtf8("label_15"))
		self.horizontalLayout_7.addWidget(self.label_15)
		spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout_7.addItem(spacerItem4)
		self.label_16 = QtGui.QLabel(Form)
		font = QtGui.QFont()
		font.setPointSize(16)
		self.label_16.setFont(font)
		self.label_16.setAlignment(QtCore.Qt.AlignCenter)
		self.label_16.setObjectName(_fromUtf8("label_16"))
		self.horizontalLayout_7.addWidget(self.label_16)
		self.gridLayout_2.addLayout(self.horizontalLayout_7, 10, 1, 1, 4)
		self.horizontalLayout_3 = QtGui.QHBoxLayout()
		self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
		self.label = QtGui.QLabel(Form)
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
		self.horizontalLayout_9 = QtGui.QHBoxLayout()
		self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
		self.label_21 = QtGui.QLabel(Form)
		font = QtGui.QFont()
		font.setPointSize(16)
		self.label_21.setFont(font)
		self.label_21.setAlignment(QtCore.Qt.AlignCenter)
		self.label_21.setObjectName(_fromUtf8("label_21"))
		self.horizontalLayout_9.addWidget(self.label_21)
		spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout_9.addItem(spacerItem5)
		self.label_22 = QtGui.QLabel(Form)
		font = QtGui.QFont()
		font.setPointSize(16)
		self.label_22.setFont(font)
		self.label_22.setAlignment(QtCore.Qt.AlignCenter)
		self.label_22.setObjectName(_fromUtf8("label_22"))
		self.horizontalLayout_9.addWidget(self.label_22)
		spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout_9.addItem(spacerItem6)
		self.label_23 = QtGui.QLabel(Form)
		font = QtGui.QFont()
		font.setPointSize(16)
		self.label_23.setFont(font)
		self.label_23.setAlignment(QtCore.Qt.AlignCenter)
		self.label_23.setObjectName(_fromUtf8("label_23"))
		self.horizontalLayout_9.addWidget(self.label_23)
		self.gridLayout_2.addLayout(self.horizontalLayout_9, 18, 0, 1, 5)
		self.horizontalLayout_10 = QtGui.QHBoxLayout()
		self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
		self.submitmatchstack_f = QtGui.QPushButton(Form)
		self.submitmatchstack_f.setObjectName(_fromUtf8("submitmatchstack_f"))
		self.horizontalLayout_10.addWidget(self.submitmatchstack_f)
		self.gridLayout_2.addLayout(self.horizontalLayout_10, 17, 4, 1, 1)
		self.horizontalLayout_4 = QtGui.QHBoxLayout()
		self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
		self.containerlitter_f = QtGui.QSpinBox(Form)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(1)
		sizePolicy.setVerticalStretch(1)
		sizePolicy.setHeightForWidth(self.containerlitter_f.sizePolicy().hasHeightForWidth())
		self.containerlitter_f.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setPointSize(48)
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
		spacerItem7 = QtGui.QSpacerItem(250, 20, QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout_4.addItem(spacerItem7)
		self.landfilllitter_f = QtGui.QSpinBox(Form)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(1)
		sizePolicy.setVerticalStretch(1)
		sizePolicy.setHeightForWidth(self.landfilllitter_f.sizePolicy().hasHeightForWidth())
		self.landfilllitter_f.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setPointSize(48)
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
		self.verticalLayout_2 = QtGui.QVBoxLayout()
		self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
		self.gridLayout_2.addLayout(self.verticalLayout_2, 6, 1, 1, 1)
		self.horizontalLayout = QtGui.QHBoxLayout()
		self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
		self.autototes_f = QtGui.QSpinBox(Form)
		self.autototes_f.setEnabled(True)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(1)
		sizePolicy.setVerticalStretch(1)
		sizePolicy.setHeightForWidth(self.autototes_f.sizePolicy().hasHeightForWidth())
		self.autototes_f.setSizePolicy(sizePolicy)
		self.autototes_f.setMinimumSize(QtCore.QSize(0, 0))
		self.autototes_f.setSizeIncrement(QtCore.QSize(0, 0))
		self.autototes_f.setBaseSize(QtCore.QSize(0, 0))
		font = QtGui.QFont()
		font.setFamily(_fromUtf8("MS Shell Dlg 2"))
		font.setPointSize(48)
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
		spacerItem8 = QtGui.QSpacerItem(150, 20, QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout.addItem(spacerItem8)
		self.autocontainers_f = QtGui.QSpinBox(Form)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(1)
		sizePolicy.setVerticalStretch(1)
		sizePolicy.setHeightForWidth(self.autocontainers_f.sizePolicy().hasHeightForWidth())
		self.autocontainers_f.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setPointSize(48)
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
		spacerItem9 = QtGui.QSpacerItem(150, 20, QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout.addItem(spacerItem9)
		self.autostepcontainers_f = QtGui.QSpinBox(Form)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(1)
		sizePolicy.setVerticalStretch(1)
		sizePolicy.setHeightForWidth(self.autostepcontainers_f.sizePolicy().hasHeightForWidth())
		self.autostepcontainers_f.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setPointSize(48)
		self.autostepcontainers_f.setFont(font)
		self.autostepcontainers_f.setAutoFillBackground(False)
		self.autostepcontainers_f.setStyleSheet(_fromUtf8(""))
		self.autostepcontainers_f.setAlignment(QtCore.Qt.AlignCenter)
		self.autostepcontainers_f.setAccelerated(True)
		self.autostepcontainers_f.setMaximum(4)
		self.autostepcontainers_f.setObjectName(_fromUtf8("autostepcontainers_f"))
		self.horizontalLayout.addWidget(self.autostepcontainers_f)
		self.gridLayout_2.addLayout(self.horizontalLayout, 2, 0, 1, 5)
		self.verticalLayout_4 = QtGui.QVBoxLayout()
		self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
		self.autostackchkbox_f = QtGui.QCheckBox(Form)
		font = QtGui.QFont()
		font.setPointSize(16)
		self.autostackchkbox_f.setFont(font)
		self.autostackchkbox_f.setAutoFillBackground(False)
		self.autostackchkbox_f.setStyleSheet(_fromUtf8(""))
		self.autostackchkbox_f.setIconSize(QtCore.QSize(16, 16))
		self.autostackchkbox_f.setObjectName(_fromUtf8("autostackchkbox_f"))
		self.verticalLayout_4.addWidget(self.autostackchkbox_f)
		self.autozonechkbox_f = QtGui.QCheckBox(Form)
		font = QtGui.QFont()
		font.setPointSize(16)
		self.autozonechkbox_f.setFont(font)
		self.autozonechkbox_f.setAutoFillBackground(False)
		self.autozonechkbox_f.setStyleSheet(_fromUtf8(""))
		self.autozonechkbox_f.setChecked(False)
		self.autozonechkbox_f.setObjectName(_fromUtf8("autozonechkbox_f"))
		self.verticalLayout_4.addWidget(self.autozonechkbox_f)
		self.gridLayout_2.addLayout(self.verticalLayout_4, 3, 0, 1, 2)
		self.label_7 = QtGui.QLabel(Form)
		font = QtGui.QFont()
		font.setPointSize(20)
		font.setBold(True)
		font.setWeight(75)
		self.label_7.setFont(font)
		self.label_7.setAlignment(QtCore.Qt.AlignCenter)
		self.label_7.setObjectName(_fromUtf8("label_7"))
		self.gridLayout_2.addWidget(self.label_7, 7, 1, 1, 2)

		self.retranslateUi(Form)
		QtCore.QMetaObject.connectSlotsByName(Form)
		

	def retranslateUi(self, Form):
		Form.setWindowTitle(_translate("Form", "PiScout 2015: Turbomeme edition", None))
		self.label_18.setText(_translate("Form", "Driving ability (0-10)", None))
		self.label_17.setText(_translate("Form", "Harvesting ability (0-10)", None))
		self.submitstack_f.setText(_translate("Form", "Submit stack", None))
		self.coopstackchkbox_f.setText(_translate("Form", "Got stacked set?", None))
		self.autocomments_f.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
		#TextEdit does not support placeholdertext in pyqt 5, but lineedit does. I'll figure something out.
		#self.autocomments_f.setPlaceholderText(_translate("Form", "Comments on autonomous", None))
		self.label_4.setText(_translate("Form", "Totes in Auto Zone", None))
		self.label_3.setText(_translate("Form", "Containers in Auto Zone", None))
		self.label_2.setText(_translate("Form", "Containers from Step", None))
		self.label_25.setText(_translate("Form", "Team number", None))
		self.label_24.setText(_translate("Form", "Match number", None))
		self.teamnumfield_f.setPlaceholderText(_translate("Form", "Team number", None))
		self.matchnumfield_f.setPlaceholderText(_translate("Form", "Match number", None))
		self.label_6.setText(_translate("Form", "Litter in containers", None))
		self.label_5.setText(_translate("Form", "Litter in landfill", None))
		self.label_19.setText(_translate("Form", "Coopertition", None))
		#self.teleopcomments_f.setPlaceholderText(_translate("Form", "Comments on Teleop", None))
		self.label_15.setText(_translate("Form", "Totes taken from step", None))
		self.label_16.setText(_translate("Form", "Containers taken from step", None))
		self.label.setText(_translate("Form", "Autonomous", None))
		self.label_21.setText(_translate("Form", "Metricfac1", None))
		self.label_22.setText(_translate("Form", "Metricfac2", None))
		self.label_23.setText(_translate("Form", "Overall", None))
		self.submitmatchstack_f.setText(_translate("Form", "Submit match stats", None))
		self.autostackchkbox_f.setText(_translate("Form", "Made stacked set?", None))
		self.autozonechkbox_f.setText(_translate("Form", "Moved into auto zone?", None))
		self.label_7.setText(_translate("Form", "Teleop", None))

		#Begin functions block
		
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
		
if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	ex = Ui_Form()
	ex.show()
	sys.exit(app.exec_())

