# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'history.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Ui_History(object):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(1600, 900)
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
		self.verticalLayout.setObjectName("verticalLayout")
		self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
		self.lineEdit.setMinimumSize(QtCore.QSize(100, 20))
		self.lineEdit.setMaximumSize(QtCore.QSize(100, 20))
		self.lineEdit.setLayoutDirection(QtCore.Qt.LeftToRight)
		self.lineEdit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
		self.lineEdit.setObjectName("lineEdit")
		self.verticalLayout.addWidget(self.lineEdit)
		self.label_6 = QtWidgets.QLabel(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
		self.label_6.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setPointSize(15)
		self.label_6.setFont(font)
		self.label_6.setTextFormat(QtCore.Qt.AutoText)
		self.label_6.setAlignment(QtCore.Qt.AlignCenter)
		self.label_6.setObjectName("label_6")
		self.verticalLayout.addWidget(self.label_6)
		self.label_7 = QtWidgets.QLabel(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
		self.label_7.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setPointSize(15)
		self.label_7.setFont(font)
		self.label_7.setObjectName("label_7")
		self.verticalLayout.addWidget(self.label_7)
		self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
		self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		self.tableWidget.setRowCount(2)
		self.tableWidget.setColumnCount(4)
		self.tableWidget.resizeColumnsToContents()
		self.tableWidget.resizeRowsToContents()
		self.tableWidget.setObjectName("tableWidget")
		self.tableWidget.horizontalHeader().setVisible(False)
		self.tableWidget.verticalHeader().setVisible(False)
		for i in range(0,4):
			total = ['事件代碼','視窗','事件','是否停留']
			number = [0,1,2,3]
			newItem = QTableWidgetItem(total[i])
			textFont = QFont("song", 10, QFont.Bold)  
			newItem.setBackground(QColor('#00AAAA'))  
			newItem.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
			newItem.setFont(textFont)
			self.tableWidget.setItem(0,number[i],newItem)
		self.verticalLayout.addWidget(self.tableWidget)
		MainWindow.setCentralWidget(self.centralwidget)
		self.toolBar = QtWidgets.QToolBar(MainWindow)
		self.toolBar.setObjectName("toolBar")
		MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
		self.actionhome = QtWidgets.QAction(MainWindow)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(":/icon/house.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.actionhome.setIcon(icon)
		self.actionhome.setObjectName("actionhome")
		self.actionback = QtWidgets.QAction(MainWindow)
		icon1 = QtGui.QIcon()
		icon1.addPixmap(QtGui.QPixmap(":/icon/iconfinder_restart-1_18208.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.actionback.setIcon(icon1)
		self.actionback.setObjectName("actionback")
		self.actionnext = QtWidgets.QAction(MainWindow)
		icon2 = QtGui.QIcon()
		icon2.addPixmap(QtGui.QPixmap(":/icon/iconfinder_restart-1_18209.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.actionnext.setIcon(icon2)
		self.actionnext.setObjectName("actionnext")
		self.actionenter = QtWidgets.QAction(MainWindow)
		icon3 = QtGui.QIcon()
		icon3.addPixmap(QtGui.QPixmap(":/icon/enter.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.actionenter.setIcon(icon3)
		self.actionenter.setObjectName("actionenter")
		self.toolBar.addAction(self.actionhome)
		self.toolBar.addSeparator()
		self.toolBar.addAction(self.actionback)
		self.toolBar.addAction(self.actionnext)
		self.toolBar.addSeparator()
		self.toolBar.addAction(self.actionenter)

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
		self.label_6.setText(_translate("MainWindow", "加 權 指 數：16000"))
		self.label_7.setText(_translate("MainWindow", "代碼  "))
		self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
		self.actionhome.setText(_translate("MainWindow", "home"))
		self.actionback.setText(_translate("MainWindow", "back"))
		self.actionnext.setText(_translate("MainWindow", "next"))
		self.actionenter.setText(_translate("MainWindow", "enter"))
from ui_folder import icons
