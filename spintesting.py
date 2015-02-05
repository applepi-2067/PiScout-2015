# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'spintesting.ui'
#
# Created: Wed Feb  4 19:07:59 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(400, 300)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton_3 = QtGui.QPushButton(Form)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.verticalLayout.addWidget(self.pushButton_3)
        self.pushButton_4 = QtGui.QPushButton(Form)
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.verticalLayout.addWidget(self.pushButton_4)
        self.pushButton_2 = QtGui.QPushButton(Form)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.verticalLayout.addWidget(self.pushButton_2)
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
        self.pointsedit.setClearButtonEnabled(False)
        self.pointsedit.setObjectName(_fromUtf8("pointsedit"))
        self.horizontalLayout.addWidget(self.pointsedit)
        self.pointspin = QtGui.QSpinBox(Form)
        self.pointspin.setObjectName(_fromUtf8("pointspin"))
        self.horizontalLayout.addWidget(self.pointspin)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.pushButton_5 = QtGui.QPushButton(Form)
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.verticalLayout_2.addWidget(self.pushButton_5)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.pushButton.setText(_translate("Form", "PushButton", None))
        self.pushButton_3.setText(_translate("Form", "PushButton", None))
        self.pushButton_4.setText(_translate("Form", "PushButton", None))
        self.pushButton_2.setText(_translate("Form", "PushButton", None))
        self.matchedit.setPlaceholderText(_translate("Form", "Match number", None))
        self.teamedit.setPlaceholderText(_translate("Form", "Team Number", None))
        self.pointsedit.setPlaceholderText(_translate("Form", "Points", None))
        self.pushButton_5.setText(_translate("Form", "PushButton", None))

