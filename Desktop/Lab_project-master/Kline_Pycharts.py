# -*- coding: utf-8 -*-

#引入pyqt5需要的模組
import sys 	
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebChannel import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
#引入UI檔
from ui_to_py.PyechartsPages import *
from ui_to_py.page import *
from ui_to_py.uilogin import *
from ui_to_py.MA_Menu import *
from ui_to_py.KD_Menu import *
from ui_to_py.MACD_Menu import *
from ui_to_py.RSI_Menu import *
from ui_to_py.filter import *
from ui_to_py.stock_class import *
from ui_to_py.smart_stock import *
from ui_to_py.history import *
from ui_to_py.market import *
#引入pyecharts模組
from pyecharts.charts import Kline,Line,Bar,Grid
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
#引入其他輔助模組
from other_file import filter8
from datetime import datetime,date
from dateutil.rrule import rrule,DAILY,WEEKLY,MONTHLY
import threading
import time
import pandas as pd
from bs4 import BeautifulSoup
import talib
import numpy as np
import pymysql
import re
import csv

#################################多執行序以讀取開高收低資料，這是個股K線的###########################################
class WorkThread(QThread):
	trigger = pyqtSignal(str)

	def __int__(self):
		super(WorkThread, self).__init__()

	def run(self):
		with open('./other_file/hi.txt','r') as f:
			fuck = f.read()
		while(fuck != " "):
			with open('./other_file/hi.txt','r') as f:
				fuck = f.read()
				QCoreApplication.processEvents()
				self.trigger.emit(str(fuck))
############################################################################################

#################################多執行序以讀取開高收低資料，這是加權指數的###########################################
class MarketThread(QThread):
	trigger = pyqtSignal(str)

	def __int__(self):
		super(MarketThread, self).__init__()

	def run(self):
		with open('./other_file/market.txt','r') as f:
			fuck = f.read()
		while(fuck != " "):
			with open('./other_file/market.txt','r') as f:
				fuck = f.read()
				QCoreApplication.processEvents()
				self.trigger.emit(str(fuck))
############################################################################################

#################################MA的右鍵視窗###########################################
class MA_Menu_Window(QWidget, Ui_MA_Menu):
	def __init__(self, parent=None): 
		super(MA_Menu_Window, self).__init__(parent)
		self.setupUi(self)
		self.total_ma = [self.checkBox_6.text(),self.checkBox_3.text(),self.checkBox_4.text()]
		self.checkBox_6.setChecked(True)
		self.checkBox_3.setChecked(True)
		self.checkBox_4.setChecked(True)
		self.checkBox_6.toggled.connect(lambda:self.output_ma(self.checkBox_6.text()))
		self.checkBox_3.toggled.connect(lambda:self.output_ma(self.checkBox_3.text()))
		self.checkBox_4.toggled.connect(lambda:self.output_ma(self.checkBox_4.text()))

	def output_ma(self,check):
		if check not in self.total_ma:
			self.total_ma.append(check)
		else:
			self.total_ma.remove(check)
############################################################################################

###################################RSI右鍵視窗##############################################
class RSI_Menu_Window(QWidget, Ui_RSI):
	def __init__(self, parent=None): 
		super(RSI_Menu_Window, self).__init__(parent)
		self.setupUi(self)
############################################################################################

##################################KD右鍵視窗################################################
class KD_Menu_Window(QWidget, Ui_KD):
	def __init__(self, parent=None): 
		super(KD_Menu_Window, self).__init__(parent)
		self.setupUi(self)
############################################################################################

###################################MACD右鍵視窗###############################################
class MACD_Menu_Window(QWidget, Ui_MACD):
	def __init__(self, parent=None): 
		super(MACD_Menu_Window, self).__init__(parent)
		self.setupUi(self)
############################################################################################

###################################主頁層的視窗###############################################
class PageMainWindow(QtWidgets.QMainWindow, Ui_Page):
	
	def __init__(self, parent=None): 
		super(PageMainWindow, self).__init__(parent)
		self.setupUi(self)
		db = pymysql.connect(
			host='127.0.0.1',
			user='root',
			password='',
			database="stock",
			port=3306
		)
		self.cursor = db.cursor()
		self.market_close = '''SELECT ClosingIndex FROM TAIEX WHERE TradeDate=%s'''
		self.cursor.execute(self.market_close,'2021-02-23')
		close = self.cursor.fetchone()
		self.label_2.setText('加 權 指 數：' + str(close[0])) #在首頁上方顯示當日大盤的收盤價

		self.pushButton.clicked.connect(lambda:self.switch(self.pushButton)) #連接篩選的頁面跳轉
		self.pushButton_3.clicked.connect(lambda:self.switch(self.pushButton_3)) #連接日成交的頁面跳轉
		self.pushButton_8.clicked.connect(lambda:self.switch(self.pushButton_8)) #連接技術分析的頁面跳轉
		self.pushButton_2.clicked.connect(lambda:self.switch(self.pushButton_2)) #連接智慧選股的頁面跳轉	
		self.label_2.clicked.connect(lambda:self.switch(self.label_2)) #連接上方加權指數的頁面跳轉
		self.actionnext.triggered.connect(lambda:self.next_page()) #連接下一頁的跳轉
	
	def next_page(self): #透過讀檔知道下一個頁面，並進行跳轉
		all_page = {'page':page,'PcWin':PcWin,'market':market,'smart':smart,'day':day,'select':select}
		with open('./other_file/record.txt','r') as f:
			next_p = f.readlines()
		page.hide()
		all_page.get(str(next_p[1]).replace('\n','')).show()
				

	def switch(self,btn): #執行跳轉，並且在文件紀錄跳轉的過程
		if btn == self.pushButton:
			with open('./other_file/record.txt','w') as f:
				f.write('page\n')
				f.write('select\n')
			page.hide()
			select.show()
		elif btn == self.pushButton_3:
			with open('./other_file/record.txt','w') as f:
				f.write('page\n')
				f.write('day\n')
			page.hide()
			day.show()
		elif btn == self.pushButton_8:
			with open('./other_file/record.txt','w') as f:
				f.write('page\n')
				f.write('PcWin\n')
			page.hide()
			PcWin.show()
		elif btn == self.pushButton_2:
			with open('./other_file/record.txt','w') as f:
				f.write('page\n')
				f.write('smart\n')
			page.hide()
			smart.show()
		elif btn == self.label_2:
			with open('./other_file/record.txt','w') as f:
				f.write('page\n')
				f.write('market\n')
			page.hide()
			market.show()
############################################################################################

###################################篩選層的視窗###############################################
class SelectMainWindow(QtWidgets.QMainWindow, Ui_MainPage):
	
	def __init__(self, parent=None): 
		super(SelectMainWindow, self).__init__(parent)
		self.setupUi(self)

		db = pymysql.connect(
			host='127.0.0.1',
			user='root',
			password='',
			database="stock",
			port=3306
		)
		self.cursor = db.cursor()
		self.market_close = '''SELECT ClosingIndex FROM TAIEX WHERE TradeDate=%s'''
		self.cursor.execute(self.market_close,'2021-02-23')
		close = self.cursor.fetchone()
		self.label_2.setText('加 權 指 數：' + str(close[0])) #在上方顯示當日大盤的收盤價
		#########################################篩選的部分#############################################################
		################################以下為篩選條件的所有menu與menu裡創建的元件(之後有空進行優化)###############################
		self.own_menu = QMenu(self)
		self.own_menu1 = QMenu(self)
		self.own_menu2 = QMenu(self)
		self.own_menu3 = QMenu(self)
		self.own_menu4 = QMenu(self)
		self.own_menu5 = QMenu(self)
		self.rank_menu = QMenu(self)
		self.rank_menu1 = QMenu(self)
		self.own_menu.triggered.connect(self.actionClicked)
		self.own_menu1.triggered.connect(self.actionClicked)
		self.own_menu2.triggered.connect(self.actionClicked)
		self.own_menu3.triggered.connect(self.actionClicked)
		self.own_menu4.triggered.connect(self.actionClicked)
		self.own_menu5.triggered.connect(self.actionClicked)
		self.rank_menu.triggered.connect(self.actionClicked)
		self.rank_menu1.triggered.connect(self.actionClicked)
		self.total_own_menu(self.own_menu,self.toolButton_4,self.total_info,'own_menu')
		self.total_own_menu(self.own_menu1,self.toolButton_26,self.total_info1,'own_menu1')
		self.total_own_menu(self.own_menu2,self.toolButton_28,self.total_info2,'own_menu2')
		self.total_own_menu(self.own_menu3,self.toolButton_30,self.total_info3,'own_menu3')
		self.total_own_menu(self.own_menu4,self.toolButton_32,self.total_info4,'own_menu4')
		self.total_own_menu(self.own_menu5,self.toolButton_34,self.total_info5,'own_menu5')

		self.total_rank_menu(self.rank_menu,self.toolButton_8,self.total_info8,'rank_menu')
		self.total_rank_menu(self.rank_menu1,self.toolButton_36,self.total_info9,'rank_menu1')

		self.pushButton.clicked.connect(lambda:self.collect_condition())
		self.actionhome.triggered.connect(lambda:self.back_home())

		self.special_menu = QMenu(self)
		self.special_menu1 = QMenu(self)
		self.special_menu.triggered.connect(self.actionClicked)
		self.special_menu1.triggered.connect(self.actionClicked)
		self.total_special_menu(self.special_menu,self.toolButton_6,self.total_info6,'special_menu')
		self.total_special_menu(self.special_menu1,self.toolButton_38,self.total_info7,'special_menu1')
		self.actionback.triggered.connect(lambda:self.back_page())
		self.actionnext.triggered.connect(lambda:self.next_page())
		self.toolButton_5.clicked.connect(lambda:self.clear_text_condition(self.horizontalLayout_11,self.toolButton_4,self.lineEdit_6,self.lineEdit_7))
		self.toolButton_27.clicked.connect(lambda:self.clear_text_condition(self.horizontalLayout_14,self.toolButton_26,self.lineEdit_24,self.lineEdit_25))
		self.toolButton_29.clicked.connect(lambda:self.clear_text_condition(self.horizontalLayout_12,self.toolButton_28,self.lineEdit_26,self.lineEdit_27))
		self.toolButton_31.clicked.connect(lambda:self.clear_text_condition(self.horizontalLayout_15,self.toolButton_30,self.lineEdit_28,self.lineEdit_29))
		self.toolButton_33.clicked.connect(lambda:self.clear_text_condition(self.horizontalLayout_13,self.toolButton_32,self.lineEdit_30,self.lineEdit_31))
		self.toolButton_35.clicked.connect(lambda:self.clear_text_condition(self.horizontalLayout_16,self.toolButton_34,self.lineEdit_32,self.lineEdit_33))
		self.toolButton_7.clicked.connect(lambda:self.clear_text_special(self.toolButton_6,self.checkBox_2))
		self.toolButton_39.clicked.connect(lambda:self.clear_text_special(self.toolButton_38,self.checkBox_16))
		self.toolButton_9.clicked.connect(lambda:self.clear_text_rank(self.toolButton_8,self.comboBox_7))
		self.toolButton_37.clicked.connect(lambda:self.clear_text_rank(self.toolButton_36,self.comboBox_9))
		###########################################################################################################################################
		self.tableWidget.doubleClicked.connect(lambda:self.go_to_kline())

		self.select_date_list = list() #紀錄T1~T6裡變化的元件，透過此陣列紀錄並放入
		self.T_list = list() #防止T1~T12的條件重複紀錄
		###########################################################################################

		#########################################日成交的部分########################################
		self.day_info()
		self.market_close = '''SELECT ClosingIndex FROM TAIEX WHERE TradeDate=%s'''
		self.cursor.execute(self.market_close,'2021-02-23')
		close = self.cursor.fetchone()
		self.label_2.setText('加 權 指 數：' + str(close[0]))
		self.comboBox_10.activated.connect(lambda:self.get_class(self.comboBox_10.currentText()))
		self.tableWidget_3.doubleClicked.connect(lambda:self.go_to_kline())
		###########################################################################################

		#######################################大盤走勢############################################
		self.date_sql = '''SELECT TradeDate FROM TAIEX'''
		self.cursor.execute(self.date_sql)
		self.date_list = self.cursor.fetchall()
		self.all_value_sql = '''SELECT OpeningIndex,ClosingIndex,HighestIndex,LowestIndex FROM TAIEX'''
		self.cursor.execute(self.all_value_sql)
		self.value = self.cursor.fetchall()
		self.value_list2 = list()
		self.open_pr = list()
		self.close_pr = list()
		self.market_close = '''SELECT ClosingIndex FROM TAIEX WHERE TradeDate=%s'''
		self.cursor.execute(self.market_close,'2021-02-23')
		close = self.cursor.fetchone()
		self.label_2.setText('加 權 指 數：' + str(close[0]))
		for val in self.value:
			self.va_list = list()
			self.open_pr.append(val[0].replace(',',''))
			self.close_pr.append(val[2].replace(',',''))
			for i in val:
				self.va_list.append(float(i.replace(',','')))
			self.value_list2.append(self.va_list)	
		############################################################################################

	def go_to_kline(self):
		PcWin.K_line(self.tableWidget.currentItem().text(),'日')

	def clear_text_condition(self,hlayout,toolbutton,lineedit1,lineedit2): #按下X後清空所有欄位
			toolbutton.setText('請選擇過濾條件')
			for cnt in reversed(range(hlayout.count())):
				widget = hlayout.takeAt(cnt).widget()
				if widget is not None: 
					widget.deleteLater()
			self.label_18 = QtWidgets.QLabel()
			self.label_18.setText('日期：')
			self.dateEdit = QtWidgets.QDateEdit()
			self.dateEdit.setDate(QDate(2021, 3, 26))
			self.dateEdit.setReadOnly(True)
			self.spacerItem20 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
			hlayout.addWidget(self.label_18)
			hlayout.addWidget(self.dateEdit)
			hlayout.addItem(self.spacerItem20)
			lineedit1.clear()
			lineedit2.clear()
	def clear_text_rank(self,toolbutton,combobox):
		toolbutton.setText('請指定排名條件')
		combobox.setCurrentIndex(0)
	def clear_text_special(self,toolbutton,checkbox):
		toolbutton.setText('請指定選股條件')
		checkbox.setChecked(False)

	def create_AC(self,label,combobox,dateedit,hlayout,spacer,day,week,month,season,select_date_list,T_text,T_list,action_text): #判斷日、周、月來決定放入哪些元件
		db = pymysql.connect(
			host='127.0.0.1',
			user='root',
			password='',
			database="stock",
			port=3306
		)
		self.cursor = db.cursor()
		self.week_sql = '''SELECT StartDate,EndDate FROM WeekStockInformation WHERE sid=%s'''
		self.month_sql = '''SELECT Month FROM MonthlyRevenue WHERE sid=%s'''

		label.setText('日期：')

		for cnt in reversed(range(hlayout.count())):
			widget = hlayout.takeAt(cnt).widget()
			if widget is not None: 
				widget.deleteLater()
		hlayout.addWidget(label)
		if T_text in T_list:
			select_date_list.pop(T_list.index(T_text))
			T_list.remove(T_text)
		if week != None:
			self.cursor.execute(self.week_sql,'1101')
			week_all_day = self.cursor.fetchall()
			for weeks in week_all_day:
				combobox.addItem(str(weeks[0]) + '~' + str(weeks[1]))
			hlayout.addWidget(combobox)
			hlayout.addItem(spacer)
			select_date_list.append(combobox)
			T_list.append(T_text)
		elif day != None:
			dateedit.setDate(QDate(2021, 3, 26))
			hlayout.addWidget(dateedit)
			hlayout.addItem(spacer)
			select_date_list.append(dateedit)
			T_list.append(T_text)
		elif month != None:
			if month[0] not in ['(月)開盤價','(月)收盤價','(月)最高價','(月)最低價','(月)漲跌價差','(月)漲跌幅度(%)','(月)成交股數','(月)成交筆數','(月)成交金額']:
				self.cursor.execute(self.month_sql,'1101')
				month_all_day = self.cursor.fetchall()
				for months in month_all_day:
					combobox.addItem(str(months[0]))
				hlayout.addWidget(combobox)
				hlayout.addItem(spacer)	
				select_date_list.append(combobox)
				T_list.append(T_text)
			else:
				self.month_info_sql = '''SELECT StartDate FROM MonthStockInformation WHERE sid=%s'''
				self.cursor.execute(self.month_info_sql,'1101')
				all_month = self.cursor.fetchall()
				for monthss in all_month:
					combobox.addItem(str(monthss[0]))
				hlayout.addWidget(combobox)
				hlayout.addItem(spacer)	
				select_date_list.append(combobox)
				T_list.append(T_text)
		elif season != None:
			self.season_sql = '''SELECT Quarterly FROM OperatingPerformance WHERE sid=%s'''
			self.cursor.execute(self.season_sql,'1101')
			season_all_day = self.cursor.fetchall()
			for seasons in season_all_day:
				combobox.addItem(str(seasons[0]))
			hlayout.addWidget(combobox)
			hlayout.addItem(spacer)
			select_date_list.append(combobox)
			T_list.append(T_text)			
		else:
			if action_text not in ['K(9)','D(9)','RSI(6)','RSI(9)','RSI(12)','成交量均價(5)','成交量均價(20)','成交量均價(60)','成交價均價(5)','成交價均價(20)','成交價均價(60)','DIF(12)','DIF(26)','MFI(14)','賣壓比例','波動率']:
				dateedit.setDate(QDate(2021, 3, 26))
				dateedit.setReadOnly(True)
				hlayout.addWidget(dateedit)
				hlayout.addItem(spacer)
				select_date_list.append(dateedit)
				T_list.append(T_text)
			else:
				dateedit.setDate(QDate(2021, 3, 26))
				hlayout.addWidget(dateedit)
				hlayout.addItem(spacer)
				select_date_list.append(dateedit)
				T_list.append(T_text)


	def actionClicked(self, action): #當menu裡的Action被按下後的動作，判斷哪個條件被選擇，並且判斷日周月
		if action.data() == 'own_menu':
			self.label_18 = QtWidgets.QLabel()
			self.comboBox_6 = QtWidgets.QComboBox()
			self.dateEdit = QtWidgets.QDateEdit()
			self.spacerItem20 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
			month_data = re.search('.月.+',action.text())
			week_data = re.search('.週.+',action.text())
			day_data = re.search('.日.+',action.text())
			season_data = re.search('.季.+',action.text())
			self.create_AC(self.label_18,self.comboBox_6,self.dateEdit,self.horizontalLayout_11,self.spacerItem20,day_data,week_data,month_data,season_data,self.select_date_list,'T1',self.T_list,action.text())
		elif action.data() == 'own_menu1':
			self.label_19 = QtWidgets.QLabel()
			self.comboBox_7 = QtWidgets.QComboBox()
			self.dateEdit_2 = QtWidgets.QDateEdit()
			self.spacerItem21 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
			month_data = re.search('.月.+',action.text())
			week_data = re.search('.週.+',action.text())
			day_data = re.search('.日.+',action.text())
			season_data = re.search('.季.+',action.text())
			self.create_AC(self.label_19,self.comboBox_7,self.dateEdit_2,self.horizontalLayout_18,self.spacerItem21,day_data,week_data,month_data,season_data,self.select_date_list,'T2',self.T_list,action.text())
		elif action.data() == 'own_menu2':
			self.label_20 = QtWidgets.QLabel()
			self.comboBox_8 = QtWidgets.QComboBox()
			self.dateEdit_3 = QtWidgets.QDateEdit()
			self.spacerItem22 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
			month_data = re.search('.月.+',action.text())
			week_data = re.search('.週.+',action.text())
			day_data = re.search('.日.+',action.text())
			season_data = re.search('.季.+',action.text())
			self.create_AC(self.label_20,self.comboBox_8,self.dateEdit_3,self.horizontalLayout_19,self.spacerItem22,day_data,week_data,month_data,season_data,self.select_date_list,'T3',self.T_list,action.text())
		elif action.data() == 'own_menu3':
			self.label_21 = QtWidgets.QLabel()
			self.comboBox_9 = QtWidgets.QComboBox()
			self.dateEdit_4 = QtWidgets.QDateEdit()
			self.spacerItem23 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
			month_data = re.search('.月.+',action.text())
			week_data = re.search('.週.+',action.text())
			day_data = re.search('.日.+',action.text())
			season_data = re.search('.季.+',action.text())
			self.create_AC(self.label_21,self.comboBox_9,self.dateEdit_4,self.horizontalLayout_20,self.spacerItem23,day_data,week_data,month_data,season_data,self.select_date_list,'T4',self.T_list,action.text())
		elif action.data() == 'own_menu4':
			self.label_21 = QtWidgets.QLabel()
			self.comboBox_10 = QtWidgets.QComboBox()
			self.dateEdit_5 = QtWidgets.QDateEdit()
			self.spacerItem24 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
			month_data = re.search('.月.+',action.text())
			week_data = re.search('.週.+',action.text())
			day_data = re.search('.日.+',action.text())
			season_data = re.search('.季.+',action.text())
			self.create_AC(self.label_21,self.comboBox_10,self.dateEdit_5,self.horizontalLayout_21,self.spacerItem24,day_data,week_data,month_data,season_data,self.select_date_list,'T5',self.T_list,action.text())
		elif action.data() == 'own_menu5':
			self.label_22 = QtWidgets.QLabel()
			self.comboBox_11 = QtWidgets.QComboBox()
			self.dateEdit_6 = QtWidgets.QDateEdit()
			self.spacerItem25 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
			month_data = re.search('.月.+',action.text())
			week_data = re.search('.週.+',action.text())
			day_data = re.search('.日.+',action.text())
			season_data = re.search('.季.+',action.text())
			self.create_AC(self.label_22,self.comboBox_11,self.dateEdit_6,self.horizontalLayout_22,self.spacerItem25,day_data,week_data,month_data,season_data,self.select_date_list,'T6',self.T_list,action.text())

	
	def collect_condition(self): #將條件整理好並送入filter8.py裡
		input_name = list() #介面上條件的名稱
		sql_table_name = list() #紀錄SQL的表
		sql_field_name = list() #紀錄SQ的TABLE
		total_output = list() #紀錄所有條件包裝送入
		total_date = list() #將處理過的時間放入此陣列
		db = pymysql.connect(
			host='127.0.0.1',
			user='root',
			password='',
			database="stock",
			port=3306
		)
		self.cursor = db.cursor()
		with open('./other_file/select_filter.csv','r',newline='',encoding='utf-8') as f: #讀出CSV裡的文件內容，此CSV記錄著介面上輸入的參數對照到SQL的表與欄位
			reader = csv.reader(f)
			for row in reader:
				input_name.append(row[0])
				sql_table_name.append(row[1])
				sql_field_name.append(row[2])

		for select in self.select_date_list:
			try:
				total_date.append(select.text())
			except:
				pass
			try:
				combobox_list_week = select.currentText().split('~')
				if len(combobox_list_week) == 2:
					self.split_sql_week = '''SELECT TradingWeek FROM WeekStockInformation WHERE StartDate=%s'''
					self.cursor.execute(self.split_sql_week,str(combobox_list_week[0]))
					split_select_week = self.cursor.fetchone()
					total_date.append(split_select_week[0])
				else:
					combobox_month = select.currentText()
					month_check = re.search('.月.+',combobox_month)
					print(month_check)
					if month_check == None:
						total_date.append(combobox_month)
					else:
						self.cursor.execute('''SELECT TradingMonth FROM MonthStockInformation WHERE StartDate=%s''',str(combobox_month))
						split_select_month = self.cursor.fetchone()
						total_date.append(split_select_month[0])				
			except:
				pass

		total_output.append(['T0','DayStockInformation','2021-03-26'])
		if self.lineEdit_6.text() != '' and self.lineEdit_7.text() != '':
			total_output.append(['T1',str(sql_table_name[input_name.index(self.toolButton_4.text())]),str(sql_field_name[input_name.index(self.toolButton_4.text())]),'NOT' if self.checkBox.isChecked() else '',(self.lineEdit_6.text(),self.lineEdit_7.text()),total_date[self.T_list.index('T1')]])
		if self.lineEdit_24.text() != '' and self.lineEdit_25.text() != '':
			total_output.append(['T2',str(sql_table_name[input_name.index(self.toolButton_26.text())]),str(sql_field_name[input_name.index(self.toolButton_26.text())]),'NOT' if self.checkBox_11.isChecked() else '',(self.lineEdit_24.text(),self.lineEdit_25.text()),total_date[self.T_list.index('T2')]])
		if self.lineEdit_26.text() != '' and self.lineEdit_27.text() != '':
			total_output.append(['T3',str(sql_table_name[input_name.index(self.toolButton_28.text())]),str(sql_field_name[input_name.index(self.toolButton_28.text())]),'NOT' if self.checkBox_12.isChecked() else '',(self.lineEdit_26.text(),self.lineEdit_27.text()),total_date[self.T_list.index('T3')]])
		if self.lineEdit_28.text() != '' and self.lineEdit_29.text() != '':
			total_output.append(['T4',str(sql_table_name[input_name.index(self.toolButton_30.text())]),str(sql_field_name[input_name.index(self.toolButton_30.text())]),'NOT' if self.checkBox_13.isChecked() else '',(self.lineEdit_28.text(),self.lineEdit_29.text()),total_date[self.T_list.index('T4')]])
		if self.lineEdit_30.text() != '' and self.lineEdit_31.text() != '':
			total_output.append(['T5',str(sql_table_name[input_name.index(self.toolButton_32.text())]),str(sql_field_name[input_name.index(self.toolButton_32.text())]),'NOT' if self.checkBox_14.isChecked() else '',(self.lineEdit_30.text(),self.lineEdit_31.text()),total_date[self.T_list.index('T5')]])
		if self.lineEdit_32.text() != '' and self.lineEdit_33.text() != '':	
			total_output.append(['T6',str(sql_table_name[input_name.index(self.toolButton_34.text())]),str(sql_field_name[input_name.index(self.toolButton_34.text())]),'NOT' if self.checkBox_15.isChecked() else '',(self.lineEdit_32.text(),self.lineEdit_33.text()),total_date[self.T_list.index('T6')]])
		if self.toolButton_6.text() != "請指定選股條件":
			db = pymysql.connect(
				host='127.0.0.1',
				user='root',
				password='',
				database="stock",
				port=3306
			)
			self.cursor = db.cursor()
			self.select_stock = '''SELECT * FROM classification WHERE c_name=%s'''
			self.cursor.execute(self.select_stock,self.toolButton_6.text())
			select_stock_list = self.cursor.fetchone()
			total_output.append(['T7','cid','classification','!' if self.checkBox_2.isChecked() else '',select_stock_list[0]])
		if self.toolButton_38.text() != "請指定選股條件":
			db = pymysql.connect(
				host='127.0.0.1',
				user='root',
				password='',
				database="stock",
				port=3306
			)
			self.cursor = db.cursor()
			self.select_stock = '''SELECT * FROM classification WHERE c_name=%s'''
			self.cursor.execute(self.select_stock,self.toolButton_38.text())
			select_stock_list = self.cursor.fetchone()
			total_output.append(['T8','cid','classification','!' if self.checkBox_16.isChecked() else '',select_stock_list[0]])
		if self.toolButton_8.text() != "請指定排名條件":
			total_output.append(['T10',str(sql_table_name[input_name.index(self.toolButton_8.text())]),str(sql_field_name[input_name.index(self.toolButton_8.text())]),'DESC' if self.comboBox_6.currentText() == '高到低' else 'ASC',self.comboBox_7.currentText(),'2021-03-26'])
		if self.toolButton_36.text() != "請指定排名條件":
			total_output.append(['T11',str(sql_table_name[input_name.index(self.toolButton_36.text())]),str(sql_field_name[input_name.index(self.toolButton_36.text())]),'DESC' if self.comboBox_8.currentText() == '高到低' else 'ASC',self.comboBox_9.currentText(),'2021-03-26'])
		self.select_info = filter8.Filter(total_output)
		
		count = 0
		self.tableWidget.setRowCount(len(self.select_info))
		for info in self.select_info: #將條件widget放入table裡
			for i in range(0,9):
				newItem = QTableWidgetItem(str(info[i]))
				textFont = QFont("song", 12, QFont.Bold)  
				newItem.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
				newItem.setFont(textFont)
				newItem.setFlags(QtCore.Qt.ItemIsEnabled)
				self.tableWidget.setItem(count,i,newItem)		
			count += 1

	# def back_page(self): #返回上一頁
	# 	all_page = {'page':page,'PcWin':PcWin,'market':market,'smart':smart,'day':day,'select':select}
	# 	with open('./other_file/record.txt','r') as f:
	# 		back_p = f.readlines()
	# 	select.hide()
	# 	all_page.get(str(back_p[back_p.index('select\n')-1]).replace('\n','')).show()
	
	# def next_page(self): #往前下一頁
	# 	all_page = {'page':page,'PcWin':PcWin,'market':market,'smart':smart,'day':day,'select':select}
	# 	with open('./other_file/record.txt','r') as f:
	# 		next_p = f.readlines()
	# 	select.hide()
	# 	all_page.get(str(next_p[next_p.index('select\n')+1]).replace('\n','')).show()
	
	# def switch(self): #跳轉頁面
	# 	with open('./other_file/record.txt','r') as f:
	# 		switch_info = f.readlines()
	# 	other_info = list()
	# 	for i in range(0,switch_info.index('select\n')):
	# 		other_info.append(switch_info[i])
	# 	other_info.append('market\n')
	# 	with open('./other_file/record.txt','w') as f:
	# 		for j in other_info:
	# 				f.write(j)
	# 	select.hide()
	# 	market.show()

	# def back_home(self): #會到首頁
	# 	select.hide()
	# 	page.show()	


	def total_own_menu(self,menu,toolbutton,info,data_name): #將menu放入toolbutton
		menu.triggered.connect(info)
		self.one_menu(menu,data_name)
		toolbutton.setMenu(menu)
		toolbutton.setPopupMode(QtWidgets.QToolButton.MenuButtonPopup)

	def total_special_menu(self,menu,toolbutton,info,data_name): #將menu放入toolbutton
		menu.triggered.connect(info)
		self.two_menu(menu,data_name)
		toolbutton.setMenu(menu)
		toolbutton.setPopupMode(QtWidgets.QToolButton.MenuButtonPopup)

	def total_rank_menu(self,menu,toolbutton,info,data_name): #將menu放入toolbutton
		menu.triggered.connect(info)
		self.three_menu(menu,data_name)
		toolbutton.setMenu(menu)
		toolbutton.setPopupMode(QtWidgets.QToolButton.MenuButtonPopup)

############################################以下為整理所有條件放入menu裡##############################################################
	def one_menu(self,menu,data_name):
		self.new_transaction = menu.addMenu('最新交易情況')
		self.new = ['開盤價','收盤價','最高價','最低價','漲跌價差','成交股數','成交筆數','成交金額']
		for i in self.new:
			self.menu_action_new = QAction(i, self)
			self.menu_action_new.setData(data_name)
			self.new_transaction.addAction(self.menu_action_new)
		
		self.old_transaction = menu.addMenu('歷史交易情況')
		self.old_day = ['(日)開盤價','(日)收盤價','(日)最高價','(日)最低價','(日)漲跌價差','(日)漲跌幅度(%)','(日)成交股數',
					'(日)成交筆數','(日)成交金額','(週)開盤價','(週)收盤價','(週)最高價','(週)最低價','(週)漲跌價差','(週)漲跌幅度(%)','(週)成交股數',
					'(週)成交筆數','(週)成交金額','(月)開盤價','(月)收盤價','(月)最高價','(月)最低價','(月)漲跌價差','(月)漲跌幅度(%)','(月)成交股數',
					'(月)成交筆數','(月)成交金額']

		for i in self.old_day:
			self.menu_action_old_day = QAction(i, self)
			self.menu_action_old_day.setData(data_name)
			self.old_transaction.addAction(self.menu_action_old_day)


		self.skill_index = menu.addMenu('技術指標')
		self.skill = ['K(9)','D(9)','RSI(6)','RSI(9)','RSI(12)','成交量均價(5)','成交量均價(20)','成交量均價(60)',
						'成交價均價(5)','成交價均價(20)','成交價均價(60)','DIF(12)','DIF(26)','MFI(14)','賣壓比例','波動率']
		for i in self.skill:
			self.menu_action_skill = QAction(i, self)
			self.menu_action_skill.setData(data_name)
			self.skill_index.addAction(self.menu_action_skill)

		self.new_Legal_person = menu.addMenu('三大法人最新買賣情況')
		self.new_legal = ['法人買賣超(張)_外資_不含自營','法人買賣超(張)_外資_自營','法人買賣超(張)_投信',
					'法人買賣超(張)_自營商_自行買賣','法人買賣超(張)_自營商_避險','總和','估計持股_外資',
					'估計持股_投信','估計持股_自營商','持股比重(%)_外資','估計持股_總和','持股比重(%)_三大法人']
		for i in self.new_legal:
			self.menu_action_new_legal = QAction(i, self)
			self.menu_action_new_legal.setData(data_name)
			self.new_Legal_person.addAction(self.menu_action_new_legal)

		self.old_Legal_person = menu.addMenu('三大法人歷史買賣情況')
		self.old_legal = ['(日)法人買賣超(張)_外資_不含自營','(日)法人買賣超(張)_外資_自營','(日)法人買賣超(張)_投信',
					'(日)法人買賣超(張)_自營商_自行買賣','(日)法人買賣超(張)_自營商_避險','總和','(日)估計持股_外資',
					'(日)估計持股_投信','(日)估計持股_自營商','(日)持股比重(%)_外資','估計持股_總和','(日)持股比重(%)_三大法人']
		for i in self.old_legal:
			self.menu_action_old_legal = QAction(i, self)
			self.menu_action_old_legal.setData(data_name)
			self.old_Legal_person.addAction(self.menu_action_old_legal)

		self.new_Financing = menu.addMenu('融資融券最新買賣狀況')
		self.new_finance = ['融資買進','融資賣出','融資現償','融資餘額','融資增減',
						'融資限額','融資使用率','融券賣出','融券買進','融券券償'
						,'融券餘額','融券增減','融券券資比','券資相抵']
		for i in self.new_finance:
			self.menu_action_new_finance = QAction(i, self)
			self.menu_action_new_finance.setData(data_name)
			self.new_Financing.addAction(self.menu_action_new_finance)

		self.old_Financing = menu.addMenu('融資融券歷史買賣狀況')
		self.old_finance = ['(日)融資買進','(日)融資賣出','(日)融資現償','(日)融資餘額','(日)融資增減',
						'(日)融資限額','(日)融資使用率','(日)融券賣出','(日)融券買進','(日)融券券償'
						,'(日)融券餘額','(日)融券增減','(日)融券券資比','(日)券資相抵']
		for i in self.old_finance:
			self.menu_action_old_finance = QAction(i, self)
			self.menu_action_old_finance.setData(data_name)
			self.old_Financing.addAction(self.menu_action_old_finance)
		
		self.new_Monthly_revenue = menu.addMenu('月營收最新交易情況')
		self.new_Monthly = ['當月營收','上月比較','去年同月營收','去年同月增減','當月累計營收',
						'去年累計營收','前期比較']
		for i in self.new_Monthly:
			self.menu_action_new_Monthly = QAction(i, self)
			self.menu_action_new_Monthly.setData(data_name)
			self.new_Monthly_revenue.addAction(self.menu_action_new_Monthly)

		self.old_Monthly_revenue = menu.addMenu('月營收歷史交易情況')
		self.old_Monthly = ['(月)當月營收','(月)上月比較','(月)去年同月營收','(月)去年同月增減','(月)當月累計營收',
						'(月)去年累計營收','(月)前期比較']
		for i in self.old_Monthly:
			self.menu_action_old_Monthly = QAction(i, self)
			self.menu_action_old_Monthly.setData(data_name)
			self.old_Monthly_revenue.addAction(self.menu_action_old_Monthly)

		self.new_Quarterl_synthesis = menu.addMenu('季綜合最新交易情況')
		self.new_Quarterl = ['交易日數','開盤','最高','最低','收盤',
						'漲跌','漲跌(%)','振福(%)','成交張數千張','成交張數日均','成交金額億元','成交金額日均'
						,'法人買賣超(千張)外資','法人買賣超(千張)投信','法人買賣超(千張)自營','法人買賣超(千張)合計','外資持股(%)','融資(千張)增減'
						,'融資(千張)餘額','融券(千張)增減','融券(千張)餘額','券資比(%)']
		for i in self.new_Quarterl:
			self.menu_action_new_Quarterl = QAction(i, self)
			self.menu_action_new_Quarterl.setData(data_name)
			self.new_Quarterl_synthesis.addAction(self.menu_action_new_Quarterl)

		self.old_Quarterl_synthesis = menu.addMenu('季綜合歷史交易情況')
		self.old_Quarterl = ['(季)交易日數','(季)開盤','(季)最高','(季)最低','(季)收盤',
						'(季)漲跌','(季)漲跌(%)','(季)振福(%)','(季)成交張數千張','(季)成交張數日均','(季)成交金額億元','(季)成交金額日均'
						,'(季)法人買賣超(千張)外資','(季)法人買賣超(千張)投信','(季)法人買賣超(千張)自營','(季)法人買賣超(千張)合計','(季)外資持股(%)','(季)融資(千張)增減'
						,'(季)融資(千張)餘額','(季)融券(千張)增減','(季)融券(千張)餘額','(季)券資比(%)']
		for i in self.old_Quarterl:
			self.menu_action_old_Quarterl = QAction(i, self)
			self.menu_action_old_Quarterl.setData(data_name)
			self.old_Quarterl_synthesis.addAction(self.menu_action_old_Quarterl)

		self.new_business_performance = menu.addMenu('經營績效最新交易情況')
		self.new_business = ['股本(億)','財報評分','年度股價(元)收盤','年度股價(元)平均','年度股價(元)漲跌',
						'年度股價(元)漲跌(%)','獲利金額(億)營業收入','獲利金額(億)營業毛利','獲利金額(億)營業利益','獲利金額(億)業外損益'
						,'獲利金額(億)稅後淨利','獲利率(%)營業毛利','獲利率(%)營業利益','獲利率(%)業外損益','獲利率(%)稅後淨利'
						,'單季ROE(%)','年估ROE(%)','單季ROA(%)','年估ROA(%)','EPS(元)稅後EPS','EPS(元)年增(元)','BPS(元)']
		for i in self.new_business:
			self.menu_action_new_business = QAction(i, self)
			self.menu_action_new_business.setData(data_name)
			self.new_business_performance.addAction(self.menu_action_new_business)
	
		self.old_business_performance = menu.addMenu('經營績效歷史交易情況')
		self.old_business = ['(季)股本(億)','(季)財報評分','(季)年度股價(元)收盤','(季)年度股價(元)平均','(季)年度股價(元)漲跌',
						'(季)年度股價(元)漲跌(%)','(季)獲利金額(億)營業收入','(季)獲利金額(億)營業毛利','(季)獲利金額(億)營業利益','(季)獲利金額(億)業外損益'
						,'(季)獲利金額(億)稅後淨利','(季)獲利率(%)營業毛利','(季)獲利率(%)營業利益','(季)獲利率(%)業外損益','(季)獲利率(%)稅後淨利'
						,'(季)單季ROE(%)','(季)年估ROE(%)','(季)單季ROA(%)','(季)年估ROA(%)','(季)EPS(元)稅後EPS','(季)EPS(元)年增(元)','(季)BPS(元)']
		for i in self.old_business:
			self.menu_action_old_business = QAction(i, self)
			self.menu_action_old_business.setData(data_name)
			self.old_business_performance.addAction(self.menu_action_old_business)

	def two_menu(self,menu,data_name):
		self.classification = menu.addMenu('產業分類')
		db = pymysql.connect(
			host='127.0.0.1',
			user='root',
			password='',
			database="stock",
			port=3306
		)
		self.cursor = db.cursor()
		self.all_stick_sql = '''SELECT * FROM classification'''
		self.cursor.execute(self.all_stick_sql)
		stock_list = self.cursor.fetchall()
		for row1,row2 in stock_list:
			self.menu_action = QAction(row2, self)
			self.menu_action.setData(data_name)
			self.classification.addAction(self.menu_action)

	def three_menu(self,menu,data_name):
		self.new_transaction = menu.addMenu('最新交易情況')
		self.new = ['開盤價','收盤價','最高價','最低價','漲跌價差','成交股數','成交筆數','成交金額']
		for i in self.new:
			self.menu_action_new = QAction(i, self)
			self.menu_action_new.setData(data_name)
			self.new_transaction.addAction(self.menu_action_new)

		self.skill_index = menu.addMenu('技術指標')
		self.skill = ['K(9)','D(9)','RSI(6)','RSI(9)','RSI(12)','成交量均價(5)','成交量均價(20)','成交量均價(60)',
						'成交價均價(5)','成交價均價(20)','成交價均價(60)','DIF(12)','DIF(26)','MFI(14)','賣壓比例','波動率']
		for i in self.skill:
			self.menu_action_skill = QAction(i, self)
			self.menu_action_skill.setData(data_name)
			self.skill_index.addAction(self.menu_action_skill)

		self.new_Legal_person = menu.addMenu('三大法人最新買賣情況')
		self.new_legal = ['法人買賣超(張)_外資_不含自營','法人買賣超(張)_外資_自營','法人買賣超(張)_投信',
					'法人買賣超(張)_自營商_自行買賣','法人買賣超(張)_自營商_避險','估計持股_外資',
					'估計持股_投信','估計持股_自營商','持股比重(%)_外資','持股比重(%)_三大法人']
		for i in self.new_legal:
			self.menu_action_new_legal = QAction(i, self)
			self.menu_action_new_legal.setData(data_name)
			self.new_Legal_person.addAction(self.menu_action_new_legal)

		self.new_Financing = menu.addMenu('融資融券最新買賣狀況')
		self.new_finance = ['融資買進','融資賣出','融資現償','融資餘額','融資增減',
						'融資限額','融資使用率','融券賣出','融券買進','融券券償'
						,'融券餘額','融券增減','融券券資比','券資相抵']
		for i in self.new_finance:
			self.menu_action_new_finance = QAction(i, self)
			self.menu_action_new_finance.setData(data_name)
			self.new_Financing.addAction(self.menu_action_new_finance)
		
		self.new_Monthly_revenue = menu.addMenu('月營收最新交易情況')
		self.new_Monthly = ['當月營收','上月比較','去年同月營收','去年同月增減','當月累計營收',
						'去年累計營收','前期比較']
		for i in self.new_Monthly:
			self.menu_action_new_Monthly = QAction(i, self)
			self.menu_action_new_Monthly.setData(data_name)
			self.new_Monthly_revenue.addAction(self.menu_action_new_Monthly)

		self.new_Quarterl_synthesis = menu.addMenu('季綜合最新交易情況')
		self.new_Quarterl = ['交易日數','開盤','最高','最低','收盤',
						'漲跌','漲跌(%)','振福(%)','成交張數千張','成交張數日均','成交金額億元','成交金額日均'
						,'法人買賣超(千張)外資','法人買賣超(千張)投信','法人買賣超(千張)自營','法人買賣超(千張)合計','外資持股(%)','融資(千張)增減'
						,'融資(千張)餘額','融券(千張)增減','融券(千張)餘額','券資比(%)']
		for i in self.new_Quarterl:
			self.menu_action_new_Quarterl = QAction(i, self)
			self.menu_action_new_Quarterl.setData(data_name)
			self.new_Quarterl_synthesis.addAction(self.menu_action_new_Quarterl)

		self.new_business_performance = menu.addMenu('經營績效最新交易情況')
		self.new_business = ['股本(億)','財報評分','年度股價(元)收盤','年度股價(元)平均','年度股價(元)漲跌',
						'年度股價(元)漲跌(%)','獲利金額(億)營業收入','獲利金額(億)營業毛利','獲利金額(億)營業利益','獲利金額(億)業外損益'
						,'獲利金額(億)稅後淨利','獲利率(%)營業毛利','獲利率(%)營業利益','獲利率(%)業外損益','獲利率(%)稅後淨利'
						,'單季ROE(%)','年估ROE(%)','單季ROA(%)','年估ROA(%)','EPS(元)稅後EPS','EPS(元)年增(元)','BPS(元)']
		for i in self.new_business:
			self.menu_action_new_business = QAction(i, self)
			self.menu_action_new_business.setData(data_name)
			self.new_business_performance.addAction(self.menu_action_new_business)
#############################################################################################################################################

#############################################以下為當按下條件觸發Action後，改變toolbutton文字###################################################
	def total_info(self,action):
		self.toolButton_4.setText(action.text())
	def total_info1(self,action):
		self.toolButton_26.setText(action.text())
	def total_info2(self,action):
		self.toolButton_28.setText(action.text())
	def total_info3(self,action):
		self.toolButton_30.setText(action.text())
	def total_info4(self,action):
		self.toolButton_32.setText(action.text())
	def total_info5(self,action):
		self.toolButton_34.setText(action.text())
	def total_info6(self,action):
		self.toolButton_6.setText(action.text())
	def total_info7(self,action):
		self.toolButton_38.setText(action.text())
	def total_info8(self,action):
		self.toolButton_8.setText(action.text())
	def total_info9(self,action):
		self.toolButton_36.setText(action.text())
	def total_info10(self,action):
		self.toolButton.setText(action.text())
	def total_info11(self,action):
		self.toolButton_2.setText(action.text())
	def total_info12(self,action):
		self.toolButton_40.setText(action.text())
	def total_info13(self,action):
		self.toolButton_41.setText(action.text())
#############################################################################################################################################

####################################################智慧選股的介面####################################################################
# class SmartMainWindow(QtWidgets.QMainWindow, Ui_Smart):
# 	def __init__(self, parent=None): 
# 		super(SmartMainWindow, self).__init__(parent)
# 		self.setupUi(self)
# 		db = pymysql.connect(
# 			host='127.0.0.1',
# 			user='root',
# 			password='',
# 			database="stock",
# 			port=3306
# 		)
# 		self.cursor = db.cursor()
# 		self.market_close = '''SELECT ClosingIndex FROM TAIEX WHERE TradeDate=%s'''
# 		self.cursor.execute(self.market_close,'2021-02-23')
# 		close = self.cursor.fetchone()
# 		self.label_2.setText('加 權 指 數：' + str(close[0]))
# 		self.label_2.clicked.connect(lambda:self.switch())
# 		self.actionhome.triggered.connect(lambda:self.back_home())
# 		self.actionback.triggered.connect(lambda:self.back_page())
# 		self.actionnext.triggered.connect(lambda:self.next_page())

# 	def back_page(self):
# 		all_page = {'page':page,'PcWin':PcWin,'market':market,'smart':smart,'day':day,'select':select}
# 		with open('./other_file/record.txt','r') as f:
# 			back_p = f.readlines()
# 		smart.hide()
# 		all_page.get(str(back_p[back_p.index('smart\n')-1]).replace('\n','')).show()
	
# 	def next_page(self):
# 		all_page = {'page':page,'PcWin':PcWin,'market':market,'smart':smart,'day':day,'select':select}
# 		with open('./other_file/record.txt','r') as f:
# 			next_p = f.readlines()
# 		smart.hide()
# 		all_page.get(str(next_p[next_p.index('smart\n')+1]).replace('\n','')).show()
	
# 	def switch(self):
# 		with open('./other_file/record.txt','r') as f:
# 			switch_info = f.readlines()
# 		other_info = list()
# 		for i in range(0,switch_info.index('smart\n')):
# 			other_info.append(switch_info[i])
# 		other_info.append('market\n')
# 		with open('./other_file/record.txt','w') as f:
# 			for j in other_info:
# 					f.write(j)
# 		smart.hide()
# 		market.show()

# 	def back_home(self):
# 		smart.hide()
# 		page.show()
#############################################################################################################################################

###################################日成交層的視窗###############################################
#class dayMainWindow(QtWidgets.QMainWindow, Ui_MainPage):
	
	# def __init__(self, parent=None): 
	# 	super(dayMainWindow, self).__init__(parent)
	# 	self.setupUi(self)
	# 	db = pymysql.connect(
	# 		host='127.0.0.1',
	# 		user='root',
	# 		password='',
	# 		database="stock",
	# 		port=3306
	# 	)

	# 	self.cursor = db.cursor()

		# self.actionhome.triggered.connect(lambda:self.back_home())
		# self.actionback.triggered.connect(lambda:self.back_page())
		# self.actionnext.triggered.connect(lambda:self.next_page())


	# def back_page(self):
	# 	all_page = {'page':page,'PcWin':PcWin,'market':market,'smart':smart,'day':day,'select':select}
	# 	with open('./other_file/record.txt','r') as f:
	# 		back_p = f.readlines()
	# 	day.hide()
	# 	all_page.get(str(back_p[back_p.index('day\n')-1]).replace('\n','')).show()
	
	# def next_page(self):
	# 	all_page = {'page':page,'PcWin':PcWin,'market':market,'smart':smart,'day':day,'select':select}
	# 	with open('./other_file/record.txt','r') as f:
	# 		next_p = f.readlines()
	# 	day.hide()
	# 	all_page.get(str(next_p[next_p.index('day\n')+1]).replace('\n','')).show()

	def go_to_kline(self):
		with open('./other_file/record.txt','a') as f:
			f.write('PcWin' + '\n')
		PcWin.K_line(self.tableWidget_3.currentItem().text(),'日')
	
	# def switch(self):
	# 	with open('./other_file/record.txt','r') as f:
	# 		switch_info = f.readlines()
	# 	other_info = list()
	# 	for i in range(0,switch_info.index('day\n')):
	# 		other_info.append(switch_info[i])
	# 	other_info.append('market\n')
	# 	with open('./other_file/record.txt','w') as f:
	# 		for j in other_info:
	# 				f.write(j)
	# 	day.hide()
	# 	market.show()

	def get_class(self, class_text):
		self.class_sql = '''SELECT cid FROM classification where c_name=%s'''
		self.cursor.execute(self.class_sql, class_text)
		class_id = self.cursor.fetchone()
		self.class_get_sql = '''SELECT sid FROM stock where cid=%s'''
		self.cursor.execute(self.class_get_sql, str(class_id[0]))
		class_get_id = self.cursor.fetchall()

		self.tableWidget_3.setRowCount(len(class_get_id)+1)
		count = 0
		for cla_id in class_get_id:
			self.one_stock_sql = '''SELECT * FROM DayStockInformation where sid=%s AND TradeDate=%s'''
			try:
				self.cursor.execute(self.one_stock_sql,(str(cla_id[0]),'2021-02-02'))
				self.one_stock_list = self.cursor.fetchall()
				for one in range(0,10):
					newItem = QTableWidgetItem(str(self.one_stock_list[0][one]))
					textFont = QFont("song", 12, QFont.Bold)  
					newItem.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
					newItem.setFont(textFont)					
					newItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
					self.tableWidget_3.setItem(count,one,newItem)	
				count += 1				
			except:
				pass
		
	# def back_home(self):
	# 	day.hide()
	# 	page.show()


	def day_info(self):
		self.all_stick_sql = '''SELECT * FROM stock'''
		self.cursor.execute(self.all_stick_sql)
		stock_list = self.cursor.fetchall()
		count = 0
		self.tableWidget_3.setRowCount(len(stock_list))
		self.one_stock_sql = '''SELECT * FROM DayStockInformation where TradeDate=%s'''
		try:
			self.cursor.execute(self.one_stock_sql,'2021-02-02')
			one_stock_list = self.cursor.fetchall()
			count = 0
			for one_stock in one_stock_list:
				for one in range(0,9):
					newItem = QTableWidgetItem(str(one_stock[one]))
					textFont = QFont("song", 12, QFont.Bold)  
					newItem.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
					newItem.setFont(textFont)	
					newItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)				
					self.tableWidget_3.setItem(count,one,newItem)	
				count += 1				
		except:
			pass


############################################################################################

		# self.actionhome.triggered.connect(lambda:self.back_home())
		# self.actionback.triggered.connect(lambda:self.back_page())
		# self.actionnext.triggered.connect(lambda:self.next_page())

	# def back_page(self):
	# 	all_page = {'page':page,'PcWin':PcWin,'market':market,'smart':smart,'day':day,'select':select}
	# 	with open('./other_file/record.txt','r') as f:
	# 		back_p = f.readlines()
	# 	market.hide()
	# 	all_page.get(str(back_p[back_p.index('market\n')-1]).replace('\n','')).show()
	
	# def next_page(self):
	# 	all_page = {'page':page,'PcWin':PcWin,'market':market,'smart':smart,'day':day,'select':select}
	# 	with open('./other_file/record.txt','r') as f:
	# 		next_p = f.readlines()
	# 	market.hide()
	# 	all_page.get(str(next_p[next_p.index('market\n')+1]).replace('\n','')).show()

	# def back_home(self):
	# 	market.hide()
	# 	page.show()

	def market_kline(self):
		self.kline = (
			Kline(init_opts=opts.InitOpts(width="1300px", height="300px"))
			.add_xaxis(self.date_list[-180:])
			.add_yaxis(
				"kline", 
				self.value_list2[-180:], 
				itemstyle_opts=opts.ItemStyleOpts(
					color="#ec0000",
					color0="#00da3c",
					border_color="#ec0000",
					border_color0="#00da3c",
				),
			)
			.set_global_opts(
				datazoom_opts = [opts.DataZoomOpts(type_="slider"),opts.DataZoomOpts(type_="inside")],
				tooltip_opts = opts.TooltipOpts(
					is_show_content=True,
					formatter=JsCode(
						"""
							function (params) {
								let res = '';
								let res_two = '';
								res_two += params[0].value[1] + ' ';
								res_two += params[0].value[2] + ' ';
								res_two += params[0].value[3] + ' ';
								res_two += params[0].value[4] + ' ';

								stock_info = res_two;

							}
						"""
					)
				),
				axispointer_opts = opts.AxisPointerOpts(is_show=True),
				xaxis_opts = opts.AxisOpts(
					is_show=True,
					splitline_opts = opts.SplitLineOpts(is_show=True),
					axistick_opts = opts.AxisTickOpts(is_show=False),
					axislabel_opts = opts.LabelOpts(is_show=False),
				),
				yaxis_opts=opts.AxisOpts(
					splitline_opts = opts.SplitLineOpts(is_show=True),
					is_scale=True
				),
				legend_opts = opts.LegendOpts(is_show=False, pos_right="center"),
			)
		)
		if self.webEngineView.geometry().width() < 1600:
			grid_chart = Grid(init_opts=opts.InitOpts(width="1550px", height="740px"))
			opendata = list()
			closedata = list()
			for opens in self.open_pr[-180:]:
				opendata.append(float(opens))
			for close in self.close_pr[-180:]:
				closedata.append(float(close))
			grid_chart.add_js_funcs("var openData = {}".format(opendata))
			grid_chart.add_js_funcs("var closeData = {}".format(closedata))			
			grid_chart.add_js_funcs("var stock_info = ''")
			grid_chart.add_js_funcs("""
			document.addEventListener("DOMContentLoaded", function(){
				new QWebChannel(qt.webChannelTransport, function(channel){
					window.bridge = channel.objects.bridge;
				})
			})
			function bitch(){
				if (window.bridge){
					window.bridge.strValue = stock_info;
				}
			}
			document.body.onmousemove = bitch;
			""")
		else:
			grid_chart = Grid(init_opts=opts.InitOpts(width=str(self.webEngineView.geometry().width()) + "px", height=str(self.webEngineView.geometry().height()-50) + "px"))
		
			grid_chart.add_js_funcs("var stock_info = ''")
			grid_chart.add_js_funcs("""
			document.addEventListener("DOMContentLoaded", function(){
				new QWebChannel(qt.webChannelTransport, function(channel){
					window.bridge = channel.objects.bridge;
				})
			})
			function bitch(){
				if (window.bridge){
					window.bridge.strValue = stock_info;
				}
			}
			document.body.onmousemove = bitch;
			""")
		grid_chart.add(self.kline,grid_opts=opts.GridOpts(is_show=True))

		grid_chart.render("render_Market.html")
		with open('./render_Market.html','r') as f:
			html = f.read()
		soup = BeautifulSoup(html,'html.parser')
		new_tag = soup.new_tag('script', src='./qwebchannel.js')
		soup.head.insert(0,new_tag)
		with open('./render_Market.html','w') as f:
			html = f.write(str(soup))
		self.webEngineView.setUrl(QtCore.QUrl("file:///render_Market.html"))
		self.thread = MarketThread()
		self.thread.start()
		self.thread.trigger.connect(self.addinfo)		

	def resizeEvent(self, event):
		self.market_kline()

	def addinfo(self,info):
		try:
			pe = QPalette()
			pe.setColor(QPalette.WindowText,Qt.red if info.split(' ')[1]>info.split(' ')[0] else QColor('#00BB00'))
			self.label_20.setText("最低價：" + info.split(' ')[3])
			self.label_20.setPalette(pe)
			self.label_21.setText("最高價：" + info.split(' ')[2])
			self.label_21.setPalette(pe)
			self.label_22.setText("收盤價：" + info.split(' ')[1])
			self.label_22.setPalette(pe)
			self.label_23.setText("開盤價：" + info.split(' ')[0])
			self.label_23.setPalette(pe)
		except:
			pass
	def _getStrValue(self):
		  
		return '100'        

	def _setStrValue(self, fuck):

		self.fuck_list = fuck.split()
		try:
			with open('./other_file/market.txt','w') as f:
				f.write(str(self.fuck_list[0]) + ' ' +str(self.fuck_list[1]) + ' ' +str(self.fuck_list[2]) + ' ' +str(self.fuck_list[3]))
		except:
			pass
	strValue = pyqtProperty(str, fget=_getStrValue, fset=_setStrValue) 	

###################################技術分析層的視窗###############################################
class PyechartsMainWindow(QtWidgets.QMainWindow, Ui_Pyechart):
	
	def __init__(self, parent=None): 
		super(PyechartsMainWindow, self).__init__(parent)
		self.setupUi(self)

		db = pymysql.connect(
			host='127.0.0.1',
			user='root',
			password='',
			database="stock",
			port=3306
		)
		self.cursor = db.cursor()

		self.market_close = '''SELECT ClosingIndex FROM TAIEX WHERE TradeDate=%s'''
		self.cursor.execute(self.market_close,'2021-02-23')
		close = self.cursor.fetchone()
		self.label_1000.setText('加 權 指 數：' + str(close[0]))
	
		self.ma_menu = MA_Menu_Window()
		self.rsi_menu = RSI_Menu_Window()
		self.kd_menu = KD_Menu_Window()
		self.macd_menu = MACD_Menu_Window()
		self.stock_number_name = pd.read_csv("./other_file/stock_number_name.csv",index_col="stock_name",encoding='utf8') #讀取stock_number_name.csv
   
		self.actionenter.triggered.connect(lambda:self.K_line(self.lineEdit_100.text(),self.comboBox_135.currentText())) #點擊搜尋會跑出K_line函式的圖
		self.home.triggered.connect(lambda:self.back_home())

		self.ma_menu.pushButton.clicked.connect(lambda:self.MA_botton())


		self.comboBox_2.setCurrentIndex(3)
		self.comboBox_3.setCurrentIndex(0)
		self.comboBox_4.setCurrentIndex(1)
		self.comboBox.activated.connect(lambda:self.K_line(self.lineEdit_100.text(),self.comboBox_135.currentText()))
		self.comboBox_2.activated.connect(lambda:self.K_line(self.lineEdit_100.text(),self.comboBox_135.currentText()))
		self.comboBox_3.activated.connect(lambda:self.K_line(self.lineEdit_100.text(),self.comboBox_135.currentText()))
		self.comboBox_4.activated.connect(lambda:self.K_line(self.lineEdit_100.text(),self.comboBox_135.currentText()))
		self.comboBox_6.activated.connect(lambda:self.Balance_sheet(self.lineEdit_100.text(),self.comboBox_6.currentText(),self.comboBox_5.currentText()))
		self.comboBox_5.activated.connect(lambda:self.Balance_sheet(self.lineEdit_100.text(),self.comboBox_6.currentText(),self.comboBox_5.currentText()))
		self.comboBox_135.activated.connect(lambda:self.K_line(self.lineEdit_100.text(),self.comboBox_135.currentText()))
		
		self.radioButton_2.setChecked(True)
		self.radioButton_2.toggled.connect(lambda:self.company_change(self.radioButton_2))
		self.radioButton.toggled.connect(lambda:self.company_change(self.radioButton))
		self.pushButton_5.clicked.connect(lambda:self.legal_entities(self.lineEdit_100.text(),self.dateEdit_3.text(),self.dateEdit_4.text()))
		self.pushButton_4.clicked.connect(lambda:self.Financing(self.lineEdit_100.text(),self.dateEdit.text(),self.dateEdit_2.text()))
		self.base_company(self.lineEdit_100.text())
		self.legal_entities(self.lineEdit_100.text(),0,0)
		self.Financing(self.lineEdit_100.text(),0,0)
		self.month_income(self.lineEdit_100.text())
		self.business_performance(self.lineEdit_100.text())
		self.dividend(self.lineEdit_100.text())

		self.listWidget.itemClicked.connect(lambda:self.history_test(self.listWidget,self.listWidget_2))
		self.listWidget_3.itemClicked.connect(lambda:self.history_test(self.listWidget_3,self.listWidget_4))
		self.listWidget_2.itemClicked.connect(lambda:self.check_input(self.listWidget.currentItem().text(),self.listWidget_2,self.listWidget_5))
		self.listWidget_4.itemClicked.connect(lambda:self.check_input(self.listWidget_3.currentItem().text(),self.listWidget_4,self.listWidget_6))
		self.listWidget_5.doubleClicked.connect(lambda:self.cancel_item(self.listWidget_5,self.listWidget_2))
		self.listWidget_6.doubleClicked.connect(lambda:self.cancel_item(self.listWidget_6,self.listWidget_4))
		self.label_1000.clicked.connect(lambda:self.switch())
		self.pushButton_2.clicked.connect(lambda:self.clear_confident(self.pushButton_2))
		self.pushButton.clicked.connect(lambda:self.clear_confident(self.pushButton))

		self.actionback.triggered.connect(lambda:self.back_page())
		self.actionnext.triggered.connect(lambda:self.next_page())

	def clear_confident(self, btn):
		if btn == self.pushButton_2:
			self.listWidget_5.clear()
		elif btn == self.pushButton:
			self.listWidget_6.clear()


	def back_page(self):
		all_page = {'page':page,'PcWin':PcWin,'market':market,'smart':smart,'day':day,'select':select}
		with open('./other_file/record.txt','r') as f:
			back_p = f.readlines()
		PcWin.hide()
		all_page.get(str(back_p[back_p.index('PcWin\n')-1]).replace('\n','')).show()
	
	def next_page(self):
		all_page = {'page':page,'PcWin':PcWin,'market':market,'smart':smart,'day':day,'select':select}
		with open('./other_file/record.txt','r') as f:
			next_p = f.readlines()
		PcWin.hide()
		all_page.get(str(next_p[next_p.index('PcWin\n')+1]).replace('\n','')).show()
	
	def switch(self):
		with open('./other_file/record.txt','r') as f:
			switch_info = f.readlines()
		other_info = list()
		for i in range(0,switch_info.index('PcWin\n')):
			other_info.append(switch_info[i])
		other_info.append('market\n')
		with open('./other_file/record.txt','w') as f:
			for j in other_info:
					f.write(j)
		PcWin.hide()
		market.show()

	def cancel_item(self,list_cancel,list_color):
		list_cancel.takeItem(list_cancel.currentIndex().row())

	def get_total_text(self,sk_item,sk_index,listwd_index,listwd_index2):
		text_item = list()
		if sk_item[listwd_index.currentIndex().row()].findChildren(QLabel) != None:
			for i in sk_item[listwd_index.currentIndex().row()].findChildren(QLabel):
				text_item.append(i.text())
		if sk_item[listwd_index.currentIndex().row()].findChild(QComboBox) != None:
			for i in sk_item[listwd_index.currentIndex().row()].findChildren(QComboBox):
				text_item.append(i.currentText())	
		if sk_item[listwd_index.currentIndex().row()].findChildren(QLineEdit) != None:
			for i in sk_item[listwd_index.currentIndex().row()].findChildren(QLineEdit):
				text_item.append(i.text())	

		if sk_index == 'KD':
			if len(text_item) == 9:
				total_info = str(text_item[0])+str(text_item[4])+str(text_item[7])+str(text_item[1])+str(text_item[5])+str(text_item[8])+str(text_item[2])+str(text_item[6])+str(text_item[3])
				listwd_index2.addItem(total_info)
			elif len(text_item) == 2:
				total_info = str(text_item[0])+str(text_item[1])
				listwd_index2.addItem(total_info)
		elif sk_index == 'MACD,DIF':
			if len(text_item) == 6:
				total_info = str(text_item[0])+str(text_item[3])+str(text_item[5])+str(text_item[1])+str(text_item[4])+str(text_item[2])
				listwd_index2.addItem(total_info)
			elif len(text_item) == 3:
				total_info = str(text_item[0])+str(text_item[2])+str(text_item[1])
				listwd_index2.addItem(total_info)
		elif sk_index == 'RSI':
			total_info = str(text_item[0])+str(text_item[3])+str(text_item[5])+str(text_item[1])+str(text_item[4])+str(text_item[2])
			listwd_index2.addItem(total_info)
		elif sk_index == '均線':
			total_info = str(text_item[0])+str(text_item[1])
			listwd_index2.addItem(total_info)
		elif sk_index == '布林通道':
			if len(text_item) == 4:
				total_info = str(text_item[0])+str(text_item[2])+str(text_item[3])+str(text_item[1])
				listwd_index2.addItem(total_info)
			elif len(text_item) == 1:
				total_info = str(text_item[0])
				listwd_index2.addItem(total_info)
		elif sk_index == '賣壓比例':
			total_info = str(text_item[0])+str(text_item[1])+str(text_item[2])
			listwd_index2.addItem(total_info)
		elif sk_index == 'MFI':
			total_info = str(text_item[0])+str(text_item[1])+str(text_item[2])
			listwd_index2.addItem(total_info)
		elif sk_index == '波動率':
			total_info = str(text_item[2])+str(text_item[0])+str(text_item[3])+str(text_item[1])
			listwd_index2.addItem(total_info)
		elif sk_index == '交易情況':
			total_info = str(text_item[0])+str(text_item[2])+str(text_item[1])+str(text_item[3])
			listwd_index2.addItem(total_info)
		elif sk_index == '法人買賣':
			total_info = str(text_item[0])+str(text_item[2])+str(text_item[3])+str(text_item[1])
			listwd_index2.addItem(total_info)
		elif sk_index == '融資融券':
			if len(text_item) == 4 and '%' in text_item:
				total_info = str(text_item[2])+str(text_item[0])+str(text_item[3])+str(text_item[1])
				listwd_index2.addItem(total_info)
			else:
				total_info = str(text_item[0])+str(text_item[2])+str(text_item[3])+str(text_item[1])
				listwd_index2.addItem(total_info)
		elif sk_index == '獲利情況':
			if len(text_item) == 3 and '上季' in text_item:
				total_info = str(text_item[0])+str(text_item[2])+str(text_item[1])
				listwd_index2.addItem(total_info)
			elif len(text_item) == 5:
				total_info = str(text_item[0])+str(text_item[2])+str(text_item[1])+str(text_item[3])+str(text_item[4])
				listwd_index2.addItem(total_info)
			else:
				total_info = str(text_item[1])+str(text_item[0])+str(text_item[2])
				listwd_index2.addItem(total_info)				
		elif sk_index == '股利':
			if len(text_item) == 3:
				total_info = str(text_item[0])+str(text_item[2])+str(text_item[1])
				listwd_index2.addItem(total_info)
			elif len(text_item) == 4:
				total_info = str(text_item[0])+str(text_item[2])+str(text_item[1])+str(text_item[3])
				listwd_index2.addItem(total_info)


	def check_input(self,sk,listwd,listwd2):
		KD_item = [self.widget,self.widget_2,self.widget_3,self.widget_4,self.widget_5,self.widget_6,self.widget_7,self.widget_8,self.widget_9]
		MACD_item = [self.widget_16,self.widget_17,self.widget_18,self.widget_19,self.widget_20,self.widget_21,self.widget_10,self.widget_12,self.widget_11,self.widget_13,self.widget_14,self.widget_15]
		RSI_item = [self.widget_22,self.widget_27,self.widget_23,self.widget_24,self.widget_25,self.widget_26,self.widget_33,self.widget_32,self.widget_31]
		MA_item= [self.widget_42,self.widget_95,self.widget_40,self.widget_39]
		BOOL_item = [self.widget_38,self.widget_37]
		MFI_item= [self.widget_35]
		SELL_item= [self.widget_36]
		Fluctuation_item = [self.widget_34]
		Transaction_item = [self.widget_30,self.widget_29,self.widget_28]
		Legal_item = [self.widget_59,self.widget_58,self.widget_57,self.widget_50,self.widget_49,self.widget_60,self.widget_56,self.widget_55,self.widget_54,self.widget_53,self.widget_52,self.widget_51]
		Financing_item = [self.widget_70,self.widget_71,self.widget_72,self.widget_69,self.widget_68,self.widget_67,self.widget_66,self.widget_65,self.widget_64,self.widget_63,self.widget_62,self.widget_61]
		Profit_item = [self.widget_85,self.widget_86,self.widget_87,self.widget_88,self.widget_89,self.widget_90,self.widget_91,self.widget_94,self.widget_93,self.widget_92,self.widget_73,self.widget_74,self.widget_75]
		Dividend_item = [self.widget_76,self.widget_77,self.widget_78,self.widget_80,self.widget_79,self.widget_81,self.widget_83,self.widget_82,self.widget_84]
		if sk == 'KD':
			self.get_total_text(KD_item,sk,listwd,listwd2)
		elif sk == 'MACD,DIF':
			self.get_total_text(MACD_item,sk,listwd,listwd2)
		elif sk == 'RSI':
			self.get_total_text(RSI_item,sk,listwd,listwd2)
		elif sk == '均線':
			self.get_total_text(MA_item,sk,listwd,listwd2)
		elif sk == '布林通道':
			self.get_total_text(BOOL_item,sk,listwd,listwd2)
		elif sk == '賣壓比例':
			self.get_total_text(MFI_item,sk,listwd,listwd2)
		elif sk == 'MFI':
			self.get_total_text(SELL_item,sk,listwd,listwd2)
		elif sk == '波動率':
			self.get_total_text(Fluctuation_item,sk,listwd,listwd2)
		elif sk == '交易情況':
			self.get_total_text(Transaction_item,sk,listwd,listwd2)
		elif sk == '法人買賣':
			self.get_total_text(Legal_item,sk,listwd,listwd2)
		elif sk == '融資融券':
			self.get_total_text(Financing_item,sk,listwd,listwd2)
		elif sk == '獲利情況':
			self.get_total_text(Profit_item,sk,listwd,listwd2)
		elif sk == '股利':
			self.get_total_text(Dividend_item,sk,listwd,listwd2)


	def history_test(self,listwid1,listwid2):
		PcWin.history_all_item()
		KD_item = [self.widget,self.widget_2,self.widget_3,self.widget_4,self.widget_5,self.widget_6,self.widget_7,self.widget_8,self.widget_9]
		MACD_item = [self.widget_16,self.widget_17,self.widget_18,self.widget_19,self.widget_20,self.widget_21,self.widget_10,self.widget_12,self.widget_11,self.widget_13,self.widget_14,self.widget_15]
		RSI_item = [self.widget_22,self.widget_27,self.widget_23,self.widget_24,self.widget_25,self.widget_26,self.widget_33,self.widget_32,self.widget_31]
		MA_item= [self.widget_42,self.widget_95,self.widget_40,self.widget_39]
		BOOL_item = [self.widget_38,self.widget_37]
		MFI_item= [self.widget_35]
		SELL_item= [self.widget_36]
		Fluctuation_item = [self.widget_34]
		Transaction_item = [self.widget_30,self.widget_29,self.widget_28]
		Legal_item = [self.widget_59,self.widget_58,self.widget_57,self.widget_50,self.widget_49,self.widget_60,self.widget_56,self.widget_55,self.widget_54,self.widget_53,self.widget_52,self.widget_51]
		Financing_item = [self.widget_70,self.widget_71,self.widget_72,self.widget_69,self.widget_68,self.widget_67,self.widget_66,self.widget_65,self.widget_64,self.widget_63,self.widget_62,self.widget_61]
		Profit_item = [self.widget_85,self.widget_86,self.widget_87,self.widget_88,self.widget_89,self.widget_90,self.widget_91,self.widget_94,self.widget_93,self.widget_92,self.widget_73,self.widget_74,self.widget_75]
		Dividend_item = [self.widget_76,self.widget_77,self.widget_78,self.widget_80,self.widget_79,self.widget_81,self.widget_83,self.widget_82,self.widget_84]
		

		for i in range(0,listwid2.count()):
			listwid2.takeItem(0)
		if listwid1.currentItem().text() == 'KD':	
			for KD in KD_item:		
				item = QListWidgetItem()
				item.setSizeHint(QSize(0, 30))
				listwid2.addItem(item)
				listwid2.setItemWidget(item,KD)
		elif listwid1.currentItem().text() == 'MACD,DIF':
			for MACD in MACD_item:
				item = QListWidgetItem()
				item.setSizeHint(QSize(0, 30))
				listwid2.addItem(item)
				listwid2.setItemWidget(item, MACD)
		elif listwid1.currentItem().text() == 'RSI':
			for RSI in RSI_item:
				item = QListWidgetItem()
				item.setSizeHint(QSize(0, 30))
				listwid2.addItem(item)
				listwid2.setItemWidget(item, RSI)		
		elif listwid1.currentItem().text() == '均線':
			for MA in MA_item:
				item = QListWidgetItem()
				item.setSizeHint(QSize(0, 30))
				listwid2.addItem(item)
				listwid2.setItemWidget(item, MA)	
		elif listwid1.currentItem().text() == '布林通道':
			for BOOL in BOOL_item:
				item = QListWidgetItem()
				item.setSizeHint(QSize(0, 30))
				listwid2.addItem(item)
				listwid2.setItemWidget(item, BOOL)
		elif listwid1.currentItem().text() == 'MFI':
			for MFI in MFI_item:
				item = QListWidgetItem()
				item.setSizeHint(QSize(0, 30))
				listwid2.addItem(item)
				listwid2.setItemWidget(item, MFI)
		elif listwid1.currentItem().text() == '賣壓比例':
			for SELL in SELL_item:
				item = QListWidgetItem()
				item.setSizeHint(QSize(0, 30))
				listwid2.addItem(item)
				listwid2.setItemWidget(item, SELL)
		elif listwid1.currentItem().text() == '波動率':
			for Fluctuation in Fluctuation_item:
				item = QListWidgetItem()
				item.setSizeHint(QSize(0, 30))
				listwid2.addItem(item)
				listwid2.setItemWidget(item, Fluctuation)
		elif listwid1.currentItem().text() == '交易情況':
			for Transaction in Transaction_item:
				item = QListWidgetItem()
				item.setSizeHint(QSize(0, 30))
				listwid2.addItem(item)
				listwid2.setItemWidget(item, Transaction)
		elif listwid1.currentItem().text() == '法人買賣':
			for Legal in Legal_item:
				item = QListWidgetItem()
				item.setSizeHint(QSize(0, 30))
				listwid2.addItem(item)
				listwid2.setItemWidget(item, Legal)
		elif listwid1.currentItem().text() == '融資融券':
			for Financing in Financing_item:
				item = QListWidgetItem()
				item.setSizeHint(QSize(0, 30))
				listwid2.addItem(item)
				listwid2.setItemWidget(item, Financing)
		elif listwid1.currentItem().text() == '獲利情況':
			for Profit in Profit_item:
				item = QListWidgetItem()
				item.setSizeHint(QSize(0, 30))
				listwid2.addItem(item)
				listwid2.setItemWidget(item, Profit)
		elif listwid1.currentItem().text() == '股利':
			for Dividend in Dividend_item:
				item = QListWidgetItem()
				item.setSizeHint(QSize(0, 30))
				listwid2.addItem(item)
				listwid2.setItemWidget(item, Dividend)


	def back_home(self):
		PcWin.hide()
		page.show()


	def contextMenuEvent(self,event):
		menu = QMenu(self)
		MA = menu.addAction('MA')
		KD = menu.addAction('KD')
		RSI = menu.addAction('RSI')
		MACD = menu.addAction('MACD')
		MA.triggered.connect(self.ma_menu.show)
		KD.triggered.connect(self.kd_menu.show)
		RSI.triggered.connect(self.rsi_menu.show)
		MACD.triggered.connect(self.macd_menu.show)
		menu.exec_(event.globalPos())
	

	def sort_info(self,pr_list,sql_pr,num,date_sql):
		no_show = list()
		count = 0
		check_count = 0
		show_list = ['ClosingPrice','OpeningPrice','HighestPrice','LowestPrice']
		if sql_pr in show_list:
			self.search_close = 'SELECT '+sql_pr+' FROM '+date_sql+' where sid=%s'
			self.cursor.execute(self.search_close,num)
			for clo in self.cursor.fetchall():
				if clo[0] == '---' or clo[0] == '--':
					pass
				else:
					pr_list.append(clo[0])
		else:
			self.search_close = 'SELECT ClosingPrice FROM '+date_sql+' where sid=%s'
			self.cursor.execute(self.search_close,num)
			
			for clo in self.cursor.fetchall():
				if clo[0] == '---' or clo[0] == '--':
					no_show.append(count)
					count += 1
				else:
					count += 1		
			self.search_close = 'SELECT '+sql_pr+' FROM '+date_sql+' where sid=%s'
			self.cursor.execute(self.search_close,num)
			for clo in self.cursor.fetchall():
				if clo[0] == '---':
					pass
				elif check_count not in no_show:
					pr_list.append(str(clo[0]).replace(',',''))
				check_count += 1
	def K_line(self,stock_text,date_sqls):
		
		values = list()
		dates = list()
		vols = list()
		macd = list()
		rsi = list()
		k_value = list()
		d_value = list()
		dif = list()
		osc = list()
		close_pr = list()
		open_pr = list()
		high_pr = list()
		low_pr = list()
		date_status = str()
		day.hide()
		PcWin.show()
		self.lineEdit_100.setText(stock_text)
		self.base_company(stock_text)
		self.legal_entities(stock_text,0,0)
		self.Financing(stock_text,0,0)
		self.month_income(stock_text)
		self.business_performance(stock_text)
		self.dividend(stock_text)
		self.Balance_sheet(stock_text,self.comboBox_6.currentText(),self.comboBox_5.currentText())
#################################以下為資料讀取###########################################
		if date_sqls == '日':
			date_status = 'DayStockInformation'
		elif date_sqls == '週':
			date_status = 'WeekStockInformation'
		elif date_sqls == '月':
			date_status = 'MonthStockInformation'
		if stock_text:
			try:
				number = str(self.stock_number_name.loc[stock_text].values).strip('[]')
				self.label_5.setText(number + '-' + stock_text)
				self.sort_info(close_pr,'ClosingPrice',number,date_status) #收盤
				self.sort_info(open_pr,'OpeningPrice',number,date_status) #開盤
				self.sort_info(high_pr,'HighestPrice',number,date_status) #最高價
				self.sort_info(low_pr,'LowestPrice',number,date_status) #最低價
				if date_status == 'DayStockInformation':
					self.sort_info(dates,'TradeDate',number,date_status) #日期
				elif date_status == 'WeekStockInformation':
					self.sort_info(dates,'StartDate',number,date_status) #日期
				elif date_status == 'MonthStockInformation':
					self.sort_info(dates,'StartDate',number,date_status) #日期
				self.sort_info(vols,'TradeVolume',number,date_status) #成交量
				self.sort_info(macd,'MACD9',number,date_status) #macd
				self.sort_info(rsi,'RSI6',number,date_status) #rsi
				self.sort_info(k_value,'K9_',number,date_status) #k_value
				self.sort_info(d_value,'D9',number,date_status) #d_value
				self.sort_info(dif,'DIF12and26',number,date_status) #dif
				
			except:
				self.label_5.setText(stock_text + '-' + str(self.stock_number_name[self.stock_number_name.number == int(stock_text)].index.values).strip('[]').strip("'"))
				self.sort_info(close_pr,'ClosingPrice',stock_text,date_status) #收盤
				self.sort_info(open_pr,'OpeningPrice',stock_text,date_status) #開盤
				self.sort_info(high_pr,'HighestPrice',stock_text,date_status) #最高價
				self.sort_info(low_pr,'LowestPrice',stock_text,date_status) #最低價
				if date_status == 'DayStockInformation':
					self.sort_info(dates,'TradeDate',stock_text,date_status) #日期
				elif date_status == 'WeekStockInformation':
					self.sort_info(dates,'StartDate',stock_text,date_status) #日期
				elif date_status == 'MonthStockInformation':
					self.sort_info(dates,'StartDate',stock_text,date_status) #日期
				self.sort_info(vols,'TradeVolume',stock_text,date_status) #成交量
				self.sort_info(macd,'MACD9',stock_text,date_status) #macd
				self.sort_info(rsi,'RSI6',stock_text,date_status) #rsi
				self.sort_info(k_value,'K9_',stock_text,date_status) #k_value
				self.sort_info(d_value,'D9',stock_text,date_status) #d_value
				self.sort_info(dif,'DIF12and26',stock_text,date_status) #dif
				
		else:
			self.sort_info(close_pr,'ClosingPrice','1101',date_status) #收盤
			self.sort_info(open_pr,'OpeningPrice','1101',date_status) #開盤
			self.sort_info(high_pr,'HighestPrice','1101',date_status) #最高價
			self.sort_info(low_pr,'LowestPrice','1101',date_status) #最低價
			if date_status == 'DayStockInformation':
				self.sort_info(dates,'TradeDate','1101',date_status) #日期
			elif date_status == 'WeekStockInformation':
				self.sort_info(dates,'StartDate','1101',date_status) #日期
			elif date_status == 'MonthStockInformation':
				self.sort_info(dates,'StartDate','1101',date_status) #日期
			self.sort_info(vols,'TradeVolume','1101',date_status) #成交量
			self.sort_info(macd,'MACD9','1101',date_status) #macd
			self.sort_info(rsi,'RSI6','1101',date_status) #rsi
			self.sort_info(k_value,'K9_','1101',date_status) #k_value
			self.sort_info(d_value,'D9','1101',date_status) #d_value
			self.sort_info(dif,'DIF12and26','1101',date_status) #dif
##########################################################################################

#################################以下為資料整理############################################

		for ma_dif in range(35,len(macd)):
			osc.append(float(dif[ma_dif])-float(macd[ma_dif]))
		for info in zip(open_pr,close_pr,high_pr,low_pr):
			values.append(info)
		sma_5 = talib.SMA(np.array(close_pr,dtype=float)[-180:], 5) #製作MA5
		sma_20 = talib.SMA(np.array(close_pr,dtype=float)[-180:], 20) #製作MA20
		sma_60 = talib.SMA(np.array(close_pr,dtype=float)[-180:], 60) #製作MA60
		H_line,M_line,L_line=talib.BBANDS(np.array(close_pr,dtype=float)[-180:], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)#製作布林通道

##########################################################################################
#################################以下為均線K線###########################################     
		kline = (
			Kline(init_opts=opts.InitOpts(width="1300px", height="300px"))
			.add_xaxis(dates[-180:])
			.add_yaxis(
				"kline", 
				values[-180:], 
				itemstyle_opts=opts.ItemStyleOpts(
					color="#ec0000",
					color0="#00da3c",
					border_color="#ec0000",
					border_color0="#00da3c",
				),
			)
			.set_global_opts(
				datazoom_opts = [opts.DataZoomOpts(type_="slider",pos_bottom='bottom',xaxis_index=[0, 1, 2, 3],),opts.DataZoomOpts(type_="inside",xaxis_index=[0, 1, 2, 3],)],
				#title_opts = opts.TitleOpts(title="Kline"),
				tooltip_opts = opts.TooltipOpts(
					position=['0%','0%'],
					trigger="axis",
					trigger_on="mousemove",
					axis_pointer_type='cross',
					#is_always_show_content=True,
					formatter=JsCode(
						"""
							function (params) {
								let res = '';
								let res_two = '';
								for (let i = 0; i < params.length; i++) {
									var data = '<p>' + params[i].name + '</p>';
									if (params[i].seriesName == 'vol' || params[i].seriesName == 'MACD'){
										res += '<p>' + params[i].marker + params[i].seriesName + '：' + '<span>' + params[i].value + '</span>' + '</p>';
									}else if(params[i].seriesName == 'kline'){
										res_two += params[i].value[1] + ' ';
										res_two += params[i].value[2] + ' ';
										res_two += params[i].value[3] + ' ';
										res_two += params[i].value[4] + ' ';
									}else if(params[i].seriesName == 'kline_bool'){
										var z;
									}else{
										res += '<p>' + params[i].marker + params[i].seriesName + '：' + '<span>' + params[i].value[1] + '</span>' + '</p>';
									}
								}
								stock_info = res_two;
								return data + res;
							}
						"""
					)
				),
				axispointer_opts = opts.AxisPointerOpts(is_show=True,link=[{"xAxisIndex": "all"},{"yAxisIndex": [2,3]}]),
				xaxis_opts = opts.AxisOpts(
					is_show=True,
					splitline_opts = opts.SplitLineOpts(is_show=True),
					axistick_opts = opts.AxisTickOpts(is_show=False),
					axislabel_opts = opts.LabelOpts(is_show=False),
				),
				yaxis_opts=opts.AxisOpts(
					splitline_opts = opts.SplitLineOpts(is_show=True),
					is_scale=True
				),
				legend_opts = opts.LegendOpts(is_show=False, pos_right="center"),
			)
		)
##########################################################################################

#################################以下為布林通道K線##########################################
		kline_bool = (
			Kline(init_opts=opts.InitOpts(width="1300px", height="300px"))
			.add_xaxis(dates[-180:])
			.add_yaxis(
				"kline_bool", 
				values[-180:], 
				itemstyle_opts=opts.ItemStyleOpts(
					color="#ec0000",
					color0="#00da3c",
					border_color="#ec0000",
					border_color0="#00da3c",
				),
			)
			.set_global_opts(
				datazoom_opts = [opts.DataZoomOpts(type_="slider",pos_bottom='bottom',xaxis_index=[0, 1, 2, 3],),opts.DataZoomOpts(type_="inside",xaxis_index=[0, 1, 2, 3],)],
				#title_opts = opts.TitleOpts(title="Kline"),
				tooltip_opts = opts.TooltipOpts(
					position=['0%','0%'],
					trigger="axis",
					trigger_on="click",
					axis_pointer_type='cross',
					#is_always_show_content=True,
				),
				axispointer_opts = opts.AxisPointerOpts(is_show=True,link=[{"xAxisIndex": "all"}]),
				xaxis_opts = opts.AxisOpts(
					is_show=True,
					splitline_opts = opts.SplitLineOpts(is_show=True),
					axistick_opts = opts.AxisTickOpts(is_show=False),
					axislabel_opts = opts.LabelOpts(is_show=False),
				),
				yaxis_opts=opts.AxisOpts(
					splitline_opts = opts.SplitLineOpts(is_show=True),
					is_scale=True
				),
				legend_opts = opts.LegendOpts(is_show=False, pos_right="center"),
			)
		)
##########################################################################################

#################################以下為均線################################################
		line_average_MA5 = (
			Line()
			.add_xaxis(dates[-180:])
			.add_yaxis(
				series_name="MA5",
				y_axis=sma_5,
				is_smooth=True,
				linestyle_opts=opts.LineStyleOpts(opacity=0.5),
				label_opts=opts.LabelOpts(is_show=False),
				is_symbol_show=False,
			)
		)
		# line_average_MA10 = (
		# 	Line()
		# 	.add_xaxis(dates[-180:])
		# 	.add_yaxis(
		# 		series_name="MA10",
		# 		y_axis=sma_10,
		# 		is_smooth=True,
		# 		linestyle_opts=opts.LineStyleOpts(opacity=0.5),
		# 		label_opts=opts.LabelOpts(is_show=False),
		# 		is_symbol_show=False,
		# 	)
		# )
		line_average_MA20 = (
			Line()
			.add_xaxis(dates[-180:])
			.add_yaxis(
				series_name="MA20",
				y_axis=sma_20,
				is_smooth=True,
				linestyle_opts=opts.LineStyleOpts(opacity=0.5),
				label_opts=opts.LabelOpts(is_show=False),
				is_symbol_show=False,
			)
		)
		line_average_MA60 = (
			Line()
			.add_xaxis(dates[-180:])
			.add_yaxis(
				series_name="MA60",
				y_axis=sma_60,
				is_smooth=True,
				linestyle_opts=opts.LineStyleOpts(opacity=0.5),
				label_opts=opts.LabelOpts(is_show=False),
				is_symbol_show=False,
			)	
		)
##########################################################################################

#################################以下為RSI指標##############################################
		line_RSI = (
			Line()
			.add_xaxis(dates[-180:])
			.add_yaxis(
				series_name="RSI",
				y_axis=rsi[-180:],
				is_smooth=True,
				linestyle_opts=opts.LineStyleOpts(opacity=0.5),
				label_opts=opts.LabelOpts(is_show=False),
				is_symbol_show=False
			)
			.set_global_opts(
				xaxis_opts = opts.AxisOpts(
					splitline_opts = opts.SplitLineOpts(is_show=True),
					is_show=True,
					axislabel_opts = opts.LabelOpts(is_show=True if str(self.comboBox_4.currentText()) == "RSI" else False),
					axistick_opts = opts.AxisTickOpts(is_show=False),
				),
				yaxis_opts=opts.AxisOpts(
					splitline_opts = opts.SplitLineOpts(is_show=True),
					is_scale=True,
				),
				legend_opts = opts.LegendOpts(is_show=False, pos_bottom=10, pos_left="center"),
			)
		)
############################################################################################

#################################以下為KD指標################################################
		line_K = (
			Line()
			.add_xaxis(dates[-180:])
			.add_yaxis(
				series_name="K",
				y_axis=k_value[-180:],
				is_smooth=True,
				linestyle_opts=opts.LineStyleOpts(opacity=0.5),
				label_opts=opts.LabelOpts(is_show=False),
				is_symbol_show=False
			)
			.set_global_opts(
				xaxis_opts = opts.AxisOpts(
					is_show=True,
					splitline_opts = opts.SplitLineOpts(is_show=True),
					axislabel_opts = opts.LabelOpts(is_show=True if str(self.comboBox_4.currentText()) == "KD" else False),
					axistick_opts = opts.AxisTickOpts(is_show=False),
				),
				yaxis_opts=opts.AxisOpts(
					splitline_opts = opts.SplitLineOpts(is_show=True),
					is_scale=True
				),
				legend_opts = opts.LegendOpts(is_show=False, pos_bottom=10, pos_left="center"),
			)
		)

		line_D = (
			Line()
			.add_xaxis(dates[-180:])
			.add_yaxis(
				series_name="D",
				y_axis=d_value[-180:],
				is_smooth=True,
				linestyle_opts=opts.LineStyleOpts(opacity=0.5),
				label_opts=opts.LabelOpts(is_show=False),
				is_symbol_show=False
			)
			.set_global_opts(
				yaxis_opts=opts.AxisOpts(
					splitline_opts = opts.SplitLineOpts(is_show=True),
					is_scale=True
				),
				legend_opts = opts.LegendOpts(is_show=False, pos_bottom=10, pos_left="center"),
			)
		)
############################################################################################

#################################以下為布林通道##############################################
		line_bool_H = (
			Line()
			.add_xaxis(dates[-180:])
			.add_yaxis(
				series_name="bool",
				y_axis=H_line,
				is_smooth=True,
				linestyle_opts=opts.LineStyleOpts(opacity=0.5),
				label_opts=opts.LabelOpts(is_show=False),
				is_symbol_show=False
			)
			.set_global_opts(
				yaxis_opts=opts.AxisOpts(
					splitline_opts = opts.SplitLineOpts(is_show=True),
					is_scale=True
				),
				legend_opts = opts.LegendOpts(is_show=False, pos_bottom=10, pos_left="center"),
			)
		)

		line_bool_M = (
			Line()
			.add_xaxis(dates[-180:])
			.add_yaxis(
				series_name="bool",
				y_axis=M_line,
				is_smooth=True,
				linestyle_opts=opts.LineStyleOpts(opacity=0.5),
				label_opts=opts.LabelOpts(is_show=False),
				is_symbol_show=False
			)
			.set_global_opts(
				yaxis_opts=opts.AxisOpts(
					splitline_opts = opts.SplitLineOpts(is_show=True),
					is_scale=True
				),
				legend_opts = opts.LegendOpts(is_show=False, pos_bottom=10, pos_left="center"),
			)
		)

		line_bool_L = (
			Line()
			.add_xaxis(dates[-180:])
			.add_yaxis(
				series_name="bool",
				y_axis=L_line,
				is_smooth=True,
				linestyle_opts=opts.LineStyleOpts(opacity=0.5),
				label_opts=opts.LabelOpts(is_show=False),
				is_symbol_show=False
			)
			.set_global_opts(
				yaxis_opts=opts.AxisOpts(
					splitline_opts = opts.SplitLineOpts(is_show=True),
					is_scale=True
				),
				legend_opts = opts.LegendOpts(is_show=False, pos_bottom=10, pos_left="center"),
			)
		)
############################################################################################

#################################以下為成交量################################################
		bar_macd = (
			Bar()
			.add_xaxis(dates[-180:])
			.add_yaxis(
				series_name="OSC", 
				y_axis=osc[-180:],
				label_opts=opts.LabelOpts(is_show=False),
				itemstyle_opts=opts.ItemStyleOpts(
					color=JsCode(
						"""
					function(params) {
						var colorList;
						if (params.value > 0) {
							colorList = '#ef232a';
						} else {
							colorList = '#14b143';
						}
						return colorList;
					}
					"""
					)
				),
			)
			.set_global_opts(
				xaxis_opts = opts.AxisOpts(
					is_show=True,
					splitline_opts = opts.SplitLineOpts(is_show=True),
					axislabel_opts = opts.LabelOpts(is_show=True if str(self.comboBox_4.currentText()) == "成交量" else False),
					axistick_opts = opts.AxisTickOpts(is_show=False),
				),
				legend_opts = opts.LegendOpts(is_show=False, pos_bottom=10, pos_left="center"),
				yaxis_opts=opts.AxisOpts(
					splitline_opts = opts.SplitLineOpts(is_show=True),
					is_scale=True
				),
			)
		)
############################################################################################

#################################以下為MACD & DIF################################################
		macd_line = (
			Line()
			.add_xaxis(dates[-180:])
			.add_yaxis(
				series_name="macd_line",
				y_axis=macd[-180:],
				is_smooth=True,
				linestyle_opts=opts.LineStyleOpts(color="#006000"),
				label_opts=opts.LabelOpts(is_show=False),
				is_symbol_show=False,
			)
			.set_global_opts(
				yaxis_opts=opts.AxisOpts(
					splitline_opts = opts.SplitLineOpts(is_show=True),
					is_scale=True
				),
				legend_opts = opts.LegendOpts(is_show=False, pos_bottom=10, pos_left="center"),
			)
		)

		dif = (
			Line()
			.add_xaxis(dates[-180:])
			.add_yaxis(
				series_name="DIF",
				y_axis=dif[-180:],
				is_smooth=True,
				linestyle_opts=opts.LineStyleOpts(color="#3A006F"),
				label_opts=opts.LabelOpts(is_show=False),
				is_symbol_show=False,
			)
			.set_global_opts(
				yaxis_opts=opts.AxisOpts(
					splitline_opts = opts.SplitLineOpts(is_show=True),
					is_scale=True
				),
				legend_opts = opts.LegendOpts(is_show=False, pos_bottom=10, pos_left="center"),
			)
		)

		bar = (
			Bar(init_opts=opts.InitOpts(width="1300px", height="300px"))
			.add_xaxis(dates[-180:])
			.add_yaxis(
				series_name="vol", 
				y_axis=vols[-180:],
				label_opts=opts.LabelOpts(is_show=False),
				itemstyle_opts=opts.ItemStyleOpts(
					color=JsCode(
						"""
					function(params) {
						var colorList;
						if (openData[params.dataIndex] < closeData[params.dataIndex] || openData[params.dataIndex] == closeData[params.dataIndex]) {
							colorList = '#ef232a';
						} else {
							colorList = '#14b143';
						}
						return colorList;
					}
					"""
					)
				),
			)
			.set_global_opts(
				xaxis_opts = opts.AxisOpts(
					is_show=True,
					splitline_opts = opts.SplitLineOpts(is_show=True),
					axislabel_opts = opts.LabelOpts(is_show=True if str(self.comboBox_4.currentText()) == "成交量" else False),
					axistick_opts = opts.AxisTickOpts(is_show=False),
				),
				legend_opts = opts.LegendOpts(is_show=False, pos_bottom=10, pos_left="center"),
				yaxis_opts=opts.AxisOpts(
					splitline_opts = opts.SplitLineOpts(is_show=True),
					is_scale=True
				),
			)
		)
############################################################################################

#################################以下為圖形繪製################################################
		for line_aver in self.ma_menu.total_ma:
			if line_aver == 'MA5':
				Kline_line = kline.overlap(line_average_MA5) #K線與均線合成
			elif line_aver == 'MA10':
				Kline_line = kline.overlap(line_average_MA10) #K線與均線合成
			elif line_aver == 'MA20':
				Kline_line = kline.overlap(line_average_MA20) #K線與均線合成
			elif line_aver == 'MA60':
				Kline_line = kline.overlap(line_average_MA60) #K線與均線合成
		KD_line = line_K.overlap(line_D) #KD指標合成
		MACD = bar_macd.overlap(macd_line).overlap(dif)
		for line_bool in [line_bool_H,line_bool_M,line_bool_L]:
			bool_line = kline_bool.overlap(line_bool)#K線與布林通道合成
		
		for com2 in range(self.comboBox_2.count()):
			self.comboBox_2.model().item(com2).setEnabled(True)
		for com3 in range(self.comboBox_3.count()):
			self.comboBox_3.model().item(com3).setEnabled(True)
		for com4 in range(self.comboBox_4.count()):
			self.comboBox_4.model().item(com4).setEnabled(True)
		# for disable in [self.comboBox_2.currentText(),self.comboBox_3.currentText(),self.comboBox_4.currentText()]:
		# 	self.comboBox_2.model().item(self.comboBox_2.findText(disable)).setEnabled(False)
		for disable in [self.comboBox_3.currentText(),self.comboBox_4.currentText()]:
			self.comboBox_2.model().item(self.comboBox_2.findText(disable)).setEnabled(False)
			self.comboBox_3.model().item(self.comboBox_3.findText(disable)).setEnabled(False)
			self.comboBox_4.model().item(self.comboBox_4.findText(disable)).setEnabled(False)
		if (self.comboBox_2.currentText() == '成交量'):
			self.comboBox_2.model().item(self.comboBox_2.findText('成交量')).setEnabled(False)
			self.comboBox_3.model().item(self.comboBox_3.findText('成交量')).setEnabled(False)
			self.comboBox_4.model().item(self.comboBox_4.findText('成交量')).setEnabled(False)
		elif (self.comboBox_2.currentText() == '布林通道'):
			self.comboBox_2.model().item(self.comboBox_2.findText('布林通道')).setEnabled(False)
		if self.comboBox_4.currentText() != self.comboBox_3.currentText() and self.comboBox_4.currentText() != self.comboBox_2.currentText() and self.comboBox_4.currentText() != self.comboBox.currentText() and self.comboBox_3.currentText() != self.comboBox_2.currentText() and self.comboBox_3.currentText() != self.comboBox.currentText() and self.comboBox_2.currentText() != self.comboBox.currentText():
			technology_all = {'K線及均線':Kline_line,'布林通道':bool_line,'KD':KD_line,'成交量':bar,'RSI':line_RSI,'MACD':MACD}
			if self.webEngineView.geometry().width() < 700:
				grid_chart = Grid(init_opts=opts.InitOpts(width="1500px", height="700px"))
			else:
				grid_chart = Grid(init_opts=opts.InitOpts(width=str(self.webEngineView.geometry().width()) + "px", height=str(self.webEngineView.geometry().height()-50) + "px"))
			opendata = list()
			closedata = list()
			for opens in open_pr[-180:]:
				opendata.append(float(opens))
			for close in close_pr[-180:]:
				closedata.append(float(close))
			grid_chart.add_js_funcs("var openData = {}".format(opendata))
			grid_chart.add_js_funcs("var closeData = {}".format(closedata))
			grid_chart.add_js_funcs("var stock_info = ''")
			grid_chart.add_js_funcs("""
			document.addEventListener("DOMContentLoaded", function(){
				new QWebChannel(qt.webChannelTransport, function(channel){
					window.bridge = channel.objects.bridge;
				})
			})
			function bitch(){
				if (window.bridge){
					window.bridge.strValue = stock_info;
				}
			}
			document.body.onmousemove = bitch;
			""")
					
			if (self.comboBox_2.currentText() == "布林通道"):
				self.comboBox_4.setDisabled(True)
				grid_chart.add(
					technology_all[self.comboBox.currentText()],
					grid_opts=opts.GridOpts(is_show=True,pos_top='1%',height="34%",pos_left='4%',pos_right='10'),
				)
				grid_chart.add(
					technology_all[self.comboBox_2.currentText()],
					grid_opts=opts.GridOpts(is_show=True,pos_bottom='28%', height="34%",pos_left='4%',pos_right='10'),
				)
				grid_chart.add(
					technology_all[self.comboBox_3.currentText()],
					grid_opts=opts.GridOpts(is_show=True,pos_bottom='9%', height="17%",pos_left='4%',pos_right='10'),
				)
				grid_chart.add(
					technology_all[self.comboBox_4.currentText()],
					grid_opts=opts.GridOpts(is_show=True,pos_bottom='-100%', height="0%"),
				)				
			else:
				opendata = list()
				closedata = list()
				for opens in open_pr[-180:]:
					opendata.append(float(opens))
				for close in close_pr[-180:]:
					closedata.append(float(close))
				grid_chart.add_js_funcs("var openData = {}".format(opendata))
				grid_chart.add_js_funcs("var closeData = {}".format(closedata))
				grid_chart.add_js_funcs("var stock_info = ''")
				grid_chart.add_js_funcs("""
				document.addEventListener("DOMContentLoaded", function(){
					new QWebChannel(qt.webChannelTransport, function(channel){
						window.bridge = channel.objects.bridge;
					})
				})
				function bitch(){
					if (window.bridge){
						window.bridge.strValue = stock_info;
					}
				}
				document.body.onmousemove = bitch;
				""")
				
				grid_chart.add(
					technology_all[self.comboBox.currentText()],
					grid_opts=opts.GridOpts(is_show=True,pos_top='1%',height="34%",pos_left='4%',pos_right='10'),
				)
				grid_chart.add(
					technology_all[self.comboBox_2.currentText()],
					grid_opts=opts.GridOpts(is_show=True,pos_bottom='45.5%', height="16%",pos_left='4%',pos_right='10'),
				)
				grid_chart.add(
					technology_all[self.comboBox_3.currentText()],
					grid_opts=opts.GridOpts(is_show=True,pos_bottom='27%', height="16%",pos_left='4%',pos_right='10'),
				)
				grid_chart.add(
					technology_all[self.comboBox_4.currentText()],
					grid_opts=opts.GridOpts(is_show=True,pos_bottom='9%', height="16%",pos_left='4%',pos_right='10'),
				)
				self.comboBox_4.setDisabled(False)
			grid_chart.render("render.html")
			with open('./render.html','r') as f:
				html = f.read()
			soup = BeautifulSoup(html,'html.parser')
			new_tag = soup.new_tag('script', src='./qwebchannel.js')
			soup.head.insert(0,new_tag)
			with open('./render.html','w') as f:
				html = f.write(str(soup))
		else:
			pass
		if stock_text: 
			self.webEngineView.setUrl(QtCore.QUrl("file:///render.html"))
			self.verticalLayout.addWidget(self.webEngineView)
			self.thread = WorkThread()
			self.thread.start()
			self.thread.trigger.connect(self.addinfo)			
############################################################################################

#################################以下為JavaScript傳輸########################################
	def _getStrValue(self):
		  
		return '100'        

	def _setStrValue(self, fuck):

		self.fuck_list = fuck.split()
		try:
			with open('./other_file/hi.txt','w') as f:
				f.write(str(self.fuck_list[0]) + ' ' +str(self.fuck_list[1]) + ' ' +str(self.fuck_list[2]) + ' ' +str(self.fuck_list[3]))
		except:
			pass
	strValue = pyqtProperty(str, fget=_getStrValue, fset=_setStrValue) 	
############################################################################################

##################################以下為每個tab頁的功能#######################################
	def Balance_sheet(self,stock_num,season_change,table_change):
		self.tableWidget_3.clear()
		try:
			FinDetail = pd.read_html("./other_file/auto_selenium/selenium" + stock_num + "/FinDetail (" + str(sorted(set(self.season),reverse=True).index(season_change)+1) + ').xls',encoding='utf-8')
			if table_change == '資產':
				self.FD_start = 2
				self.FD_end = FinDetail[0][0][FinDetail[0][0].values == '負債'].index[0]
				self.tableWidget_3.setRowCount(self.FD_end)
			elif table_change == '負債':
				self.FD_start = FinDetail[0][0][FinDetail[0][0].values == '負債'].index[0]
				self.FD_end = FinDetail[0][0][FinDetail[0][0].values == '股東權益'].index[0]
				self.tableWidget_3.setRowCount(self.FD_end-self.FD_start+2)
			elif table_change == '股東權益':
				self.FD_start = FinDetail[0][0][FinDetail[0][0].values == '股東權益'].index[0]
				self.FD_end = FinDetail[0][0][FinDetail[0][0].values == '財務報告書–公開資訊觀測站'].index[0]
				self.tableWidget_3.setRowCount(self.FD_end-self.FD_start+2)
		except:
			pass
		for i in range(0,8):
			sort_season = sorted(set(self.season),reverse=True)
			season_index = sorted(set(self.season),reverse=True).index(season_change)
			total = ['資產',sort_season[season_index],sort_season[season_index+1],sort_season[season_index+2],sort_season[season_index+3],sort_season[season_index+4],sort_season[season_index+5],sort_season[season_index+6]]
			number = [0,4,6,8,10,12,14,16]
			newItem = QTableWidgetItem(total[i])
			textFont = QFont("song", 10, QFont.Bold)  
			newItem.setBackground(QColor('#0080FF'))  
			newItem.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
			newItem.setFont(textFont)
			self.tableWidget_3.setItem(0,number[i],newItem)
		for j in range(0,14):
			total = ['金額','%','金額','%','金額','%','金額','%','金額','%','金額','%','金額','%']
			number = [4,5,6,7,8,9,10,11,12,13,14,15,16,17]
			newItem = QTableWidgetItem(total[j])
			textFont = QFont("song", 10, QFont.Bold)  
			newItem.setBackground(QColor('#84C1FF'))  
			newItem.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
			newItem.setFont(textFont)
			self.tableWidget_3.setItem(1,number[j],newItem)	
		try:
			for a in FinDetail[0].columns:
				count = 2
				for k in range(self.FD_start,self.FD_end):
					newItem = QTableWidgetItem(FinDetail[0][a][k])
					textFont = QFont("song", 10, QFont.Bold)  
					newItem.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
					newItem.setFont(textFont)	
					if a == 0:	
						self.tableWidget_3.setSpan(count,0,1,4)	
						self.tableWidget_3.setItem(count,0,newItem)	
					else:
						self.tableWidget_3.setItem(count,a+3,newItem)
					count += 1		
		except:
			pass				

	def base_company(self,stock_num):
		self.tableWidget_6.clear()
		self.tableWidget_6.setRowCount(11)
		for i in range(0,10):
			total = ['公司名稱','董事長','實收資本額','發言人','總機電話','統一編號','公司地址','英文簡稱','英文通訊地址','主要經營業務']
			newItem = QTableWidgetItem(total[i])
			textFont = QFont("song", 12, QFont.Bold)  
			newItem.setBackground(QColor('#2894FF'))  
			newItem.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
			newItem.setFont(textFont)
			self.tableWidget_6.setItem(i,0,newItem)				
		for j in range(0,8):
			total = ['成立日期','總經理','已發行普通股數','代理發言人','傳真號碼','公司網站','電子郵件','英文全名']
			newItem = QTableWidgetItem(total[j])
			textFont = QFont("song", 12, QFont.Bold)  
			newItem.setBackground(QColor('#2894FF'))  
			newItem.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
			newItem.setFont(textFont)
			self.tableWidget_6.setItem(j,5,newItem)		
		for a in range(0,8):
			self.tableWidget_6.setSpan(a,0,1,2)
			self.tableWidget_6.setSpan(a,2,1,3)
			self.tableWidget_6.setSpan(a,5,1,2)
			self.tableWidget_6.setSpan(a,7,1,3)
		self.tableWidget_6.setSpan(8,0,1,2)
		self.tableWidget_6.setSpan(8,2,1,8)
		self.tableWidget_6.setSpan(9,0,2,2)
		self.tableWidget_6.setSpan(9,2,2,8)

		if stock_num != '':
			try:
				stock_num = str(self.stock_number_name.loc[stock_num].values).strip('[]')
				self.stock_info = '''SELECT * FROM Company_information WHERE sid=%s'''
				self.cursor.execute(self.stock_info,stock_num)
				stock_list = self.cursor.fetchall()
				stock_len = len(stock_list[0])
				count = 0
				for st_len in range(1,17):
					count_plus = [3,5,7,9,11,13,15,17]
					if st_len in count_plus:
						count += 1
					newItem = QTableWidgetItem(stock_list[0][st_len])
					textFont = QFont("song", 12, QFont.Bold)  
					newItem.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
					newItem.setFont(textFont)
					if st_len % 2 != 0:
						self.tableWidget_6.setItem(count,2,newItem)
					else:
						self.tableWidget_6.setItem(count,7,newItem)

				textFont = QFont("song", 12, QFont.Bold)  
				newItem1 = QTableWidgetItem(stock_list[0][17])
				newItem2 = QTableWidgetItem(stock_list[0][18])
				newItem1.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
				newItem1.setFont(textFont)
				newItem2.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
				newItem2.setFont(textFont)		
				self.tableWidget_6.setItem(8,2,newItem1)
				self.tableWidget_6.setItem(9,2,newItem2)
			except:
				self.stock_info = '''SELECT * FROM Company_information WHERE sid=%s'''
				self.cursor.execute(self.stock_info,stock_num)
				stock_list = self.cursor.fetchall()
				stock_len = len(stock_list[0])
				count = 0
				for st_len in range(1,17):
					count_plus = [3,5,7,9,11,13,15,17]
					if st_len in count_plus:
						count += 1
					newItem = QTableWidgetItem(stock_list[0][st_len])
					textFont = QFont("song", 12, QFont.Bold)  
					newItem.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
					newItem.setFont(textFont)
					if st_len % 2 != 0:
						self.tableWidget_6.setItem(count,2,newItem)
					else:
						self.tableWidget_6.setItem(count,7,newItem)

				textFont = QFont("song", 12, QFont.Bold)  
				newItem1 = QTableWidgetItem(stock_list[0][17])
				newItem2 = QTableWidgetItem(stock_list[0][18])
				newItem1.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
				newItem1.setFont(textFont)
				newItem2.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
				newItem2.setFont(textFont)		
				self.tableWidget_6.setItem(8,2,newItem1)
				self.tableWidget_6.setItem(9,2,newItem2)

	def service_company(self,stock_num):
		self.tableWidget_6.clear()
		self.tableWidget_6.setRowCount(9)
		for i in range(0,7):
			total = ['特別股','公司債發行','股票過戶地址','簽證會計事務所','簽證會計師1','簽證會計師2','備註']
			newItem = QTableWidgetItem(total[i])
			textFont = QFont("song", 12, QFont.Bold)  
			newItem.setBackground(QColor('#2894FF'))  
			newItem.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
			newItem.setFont(textFont)
			self.tableWidget_6.setItem(i,0,newItem)				
		for j in range(0,6):
			total = ['特別股發行','股票過戶機構','過戶機構電話','變更前名稱','變更前簡稱','變更核准日']
			newItem = QTableWidgetItem(total[j])
			textFont = QFont("song", 12, QFont.Bold)  
			newItem.setBackground(QColor('#2894FF'))  
			newItem.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
			newItem.setFont(textFont)
			self.tableWidget_6.setItem(j,5,newItem)		
		for a in range(0,6):
			self.tableWidget_6.setSpan(a,0,1,2)
			self.tableWidget_6.setSpan(a,2,1,3)
			self.tableWidget_6.setSpan(a,5,1,2)
			self.tableWidget_6.setSpan(a,7,1,3)
		self.tableWidget_6.setSpan(6,0,3,2)
		self.tableWidget_6.setSpan(6,2,3,8)

		if stock_num != '':
			try:
				stock_num = str(self.stock_number_name.loc[stock_num].values).strip('[]')
				self.stock_info = '''SELECT * FROM Company_information WHERE sid=%s'''
				self.cursor.execute(self.stock_info,stock_num)
				stock_list = self.cursor.fetchall()
				stock_len = len(stock_list[0])
				count = 0
				for st_len in range(19,32):
					count_plus = [21,23,25,27,29,31]
					if st_len in count_plus:
						count += 1
					newItem = QTableWidgetItem(stock_list[0][st_len])
					textFont = QFont("song", 12, QFont.Bold)  
					newItem.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
					newItem.setFont(textFont)
					if st_len % 2 != 0:
						self.tableWidget_6.setItem(count,2,newItem)
					else:
						self.tableWidget_6.setItem(count,7,newItem)

				textFont = QFont("song", 12, QFont.Bold)  
				newItem1 = QTableWidgetItem(stock_list[0][17])
				newItem2 = QTableWidgetItem(stock_list[0][18])
				newItem1.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
				newItem1.setFont(textFont)
				newItem2.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
				newItem2.setFont(textFont)		
				self.tableWidget_6.setItem(8,2,newItem1)
				self.tableWidget_6.setItem(9,2,newItem2)	
			except:
				self.stock_info = '''SELECT * FROM Company_information WHERE sid=%s'''
				self.cursor.execute(self.stock_info,stock_num)
				stock_list = self.cursor.fetchall()
				stock_len = len(stock_list[0])
				count = 0
				for st_len in range(19,32):
					count_plus = [21,23,25,27,29,31]
					if st_len in count_plus:
						count += 1
					newItem = QTableWidgetItem(stock_list[0][st_len])
					textFont = QFont("song", 12, QFont.Bold)  
					newItem.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
					newItem.setFont(textFont)
					if st_len % 2 != 0:
						self.tableWidget_6.setItem(count,2,newItem)
					else:
						self.tableWidget_6.setItem(count,7,newItem)

				textFont = QFont("song", 12, QFont.Bold)  
				newItem1 = QTableWidgetItem(stock_list[0][17])
				newItem2 = QTableWidgetItem(stock_list[0][18])
				newItem1.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
				newItem1.setFont(textFont)
				newItem2.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
				newItem2.setFont(textFont)		
				self.tableWidget_6.setItem(8,2,newItem1)
				self.tableWidget_6.setItem(9,2,newItem2)


	def legal_entities(self,stock_num,date1,date2):
		if stock_num != '':
			try:
				stock_num = str(self.stock_number_name.loc[stock_num].values).strip('[]')
				self.stock_info = '''SELECT * FROM institutional_investors WHERE sid=%s'''
				self.cursor.execute(self.stock_info,stock_num)
				stock_list = self.cursor.fetchall()
				if date1 == 0 and date2 == 0:
					self.tableWidget_2.setRowCount(len(stock_list)+3)
					for st_len in range(0,len(stock_list)):
						for st_list in range(1,len(stock_list[st_len])):
							input_table = [0,2,1,3,4,5,6,7,8,9,10,11,12]
							newItem = QTableWidgetItem(str(stock_list[len(stock_list)-st_len-1][st_list]))
							textFont = QFont("song", 12, QFont.Bold)  
							newItem.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
							newItem.setFont(textFont)					
							self.tableWidget_2.setItem(st_len+3,input_table[st_list-1],newItem)
				else:
					self.stock_info = '''SELECT * FROM institutional_investors WHERE sid=%s AND TradeDate BETWEEN %s AND %s;'''
					date11 = datetime.date(datetime.strptime(date1, "%Y/%m/%d"))
					date22 = datetime.date(datetime.strptime(date2, "%Y/%m/%d"))
					self.cursor.execute(self.stock_info,(stock_num,date11,date22))
					stock_list_date = self.cursor.fetchall()	
					self.tableWidget_2.setRowCount(len(stock_list_date)+3)
					for st_len in range(0,len(stock_list_date)):
						for st_list in range(1,len(stock_list_date[st_len])):
							input_table = [0,2,1,3,4,5,6,7,8,9,10,11,12]
							newItem = QTableWidgetItem(str(stock_list_date[len(stock_list_date)-st_len-1][st_list]))
							textFont = QFont("song", 12, QFont.Bold)  
							newItem.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
							newItem.setFont(textFont)					
							self.tableWidget_2.setItem(st_len+3,input_table[st_list-1],newItem)


			except:
				self.stock_info = '''SELECT * FROM institutional_investors WHERE sid=%s'''
				self.cursor.execute(self.stock_info,stock_num)
				stock_list = self.cursor.fetchall()
				if date1 == 0 and date2 == 0:
					self.tableWidget_2.setRowCount(len(stock_list)+3)
					for st_len in range(0,len(stock_list)):
						for st_list in range(1,len(stock_list[st_len])):
							input_table = [0,2,1,3,4,5,6,7,8,9,10,11,12]
							newItem = QTableWidgetItem(str(stock_list[len(stock_list)-st_len-1][st_list]))
							textFont = QFont("song", 12, QFont.Bold)  
							newItem.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
							newItem.setFont(textFont)					
							self.tableWidget_2.setItem(st_len+3,input_table[st_list-1],newItem)
				else:
					self.stock_info = '''SELECT * FROM institutional_investors WHERE sid=%s AND TradeDate BETWEEN %s AND %s;'''
					date11 = datetime.date(datetime.strptime(date1, "%Y/%m/%d"))
					date22 = datetime.date(datetime.strptime(date2, "%Y/%m/%d"))
					self.cursor.execute(self.stock_info,(stock_num,date11,date22))
					stock_list_date = self.cursor.fetchall()	
					self.tableWidget_2.setRowCount(len(stock_list_date)+3)
					for st_len in range(0,len(stock_list_date)):
						for st_list in range(1,len(stock_list_date[st_len])):
							input_table = [0,2,1,3,4,5,6,7,8,9,10,11,12]
							newItem = QTableWidgetItem(str(stock_list_date[len(stock_list_date)-st_len-1][st_list]))
							textFont = QFont("song", 12, QFont.Bold)  
							newItem.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
							newItem.setFont(textFont)					
							self.tableWidget_2.setItem(st_len+3,input_table[st_list-1],newItem)




	def Financing(self,stock_num,date1,date2):
		if stock_num != '':
			try:
				stock_num = str(self.stock_number_name.loc[stock_num].values).strip('[]')
				self.stock_info = '''SELECT * FROM MarginPurchase_ShortSale WHERE sid=%s'''
				self.cursor.execute(self.stock_info,stock_num)
				stock_list = self.cursor.fetchall()
				if date1 == 0 and date2 == 0:
					self.tableWidget_5.setRowCount(len(stock_list)+2)
					for st_len in range(0,len(stock_list)):
						for st_list in range(1,len(stock_list[st_len])):
							input_table = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
							newItem = QTableWidgetItem(str(stock_list[len(stock_list)-st_len-1][st_list]))
							textFont = QFont("song", 12, QFont.Bold)  
							newItem.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
							newItem.setFont(textFont)					
							self.tableWidget_5.setItem(st_len+2,input_table[st_list-1],newItem)
				else:
					self.stock_info = '''SELECT * FROM institutional_investors WHERE sid=%s AND TradeDate BETWEEN %s AND %s;'''
					date11 = datetime.date(datetime.strptime(date1, "%Y/%m/%d"))
					date22 = datetime.date(datetime.strptime(date2, "%Y/%m/%d"))
					self.cursor.execute(self.stock_info,(stock_num,date11,date22))
					stock_list_date = self.cursor.fetchall()	
					self.tableWidget_5.setRowCount(len(stock_list_date)+2)
					for st_len in range(0,len(stock_list_date)):
						for st_list in range(1,len(stock_list_date[st_len])):
							input_table = [0,2,1,3,4,5,6,7,8,9,10,11,12]
							newItem = QTableWidgetItem(str(stock_list_date[len(stock_list_date)-st_len-1][st_list]))
							textFont = QFont("song", 12, QFont.Bold)  
							newItem.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
							newItem.setFont(textFont)					
							self.tableWidget_5.setItem(st_len+2,input_table[st_list-1],newItem)

			except:
				self.stock_info = '''SELECT * FROM MarginPurchase_ShortSale WHERE sid=%s'''
				self.cursor.execute(self.stock_info,stock_num)
				stock_list = self.cursor.fetchall()
				if date1 == 0 and date2 == 0:
					self.tableWidget_5.setRowCount(len(stock_list)+2)
					for st_len in range(0,len(stock_list)):
						for st_list in range(1,len(stock_list[st_len])):
							input_table = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
							newItem = QTableWidgetItem(str(stock_list[len(stock_list)-st_len-1][st_list]))
							textFont = QFont("song", 12, QFont.Bold)  
							newItem.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
							newItem.setFont(textFont)					
							self.tableWidget_5.setItem(st_len+2,input_table[st_list-1],newItem)
				else:
					self.stock_info = '''SELECT * FROM institutional_investors WHERE sid=%s AND TradeDate BETWEEN %s AND %s;'''
					date11 = datetime.date(datetime.strptime(date1, "%Y/%m/%d"))
					date22 = datetime.date(datetime.strptime(date2, "%Y/%m/%d"))
					self.cursor.execute(self.stock_info,(stock_num,date11,date22))
					stock_list_date = self.cursor.fetchall()	
					self.tableWidget_5.setRowCount(len(stock_list_date)+2)
					for st_len in range(0,len(stock_list_date)):
						for st_list in range(1,len(stock_list_date[st_len])):
							input_table = [0,2,1,3,4,5,6,7,8,9,10,11,12]
							newItem = QTableWidgetItem(str(stock_list_date[len(stock_list_date)-st_len-1][st_list]))
							textFont = QFont("song", 12, QFont.Bold)  
							newItem.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
							newItem.setFont(textFont)					
							self.tableWidget_5.setItem(st_len+2,input_table[st_list-1],newItem)
 

	def month_income(self,stock_num):
		if stock_num != '':
			try:
				stock_num = str(self.stock_number_name.loc[stock_num].values).strip('[]')
				self.stock_info = '''SELECT * FROM MonthlyRevenue WHERE sid=%s'''
				self.cursor.execute(self.stock_info,stock_num)
				stock_list = self.cursor.fetchall()

				self.tableWidget_7.setRowCount(len(stock_list)+2)
				for st_len in range(0,len(stock_list)):
					for st_list in range(1,len(stock_list[st_len])):
						input_table = [0,1,2,3,4,5,6,7]
						newItem = QTableWidgetItem(str(stock_list[len(stock_list)-st_len-1][st_list]))
						textFont = QFont("song", 12, QFont.Bold)  
						newItem.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
						newItem.setFont(textFont)					
						self.tableWidget_7.setItem(st_len+2,input_table[st_list-1],newItem)	
			except:
				self.stock_info = '''SELECT * FROM MonthlyRevenue WHERE sid=%s'''
				self.cursor.execute(self.stock_info,stock_num)
				stock_list = self.cursor.fetchall()

				self.tableWidget_7.setRowCount(len(stock_list)+2)
				for st_len in range(0,len(stock_list)):
					for st_list in range(1,len(stock_list[st_len])):
						input_table = [0,1,2,3,4,5,6,7]
						newItem = QTableWidgetItem(str(stock_list[len(stock_list)-st_len-1][st_list]))
						textFont = QFont("song", 12, QFont.Bold)  
						newItem.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
						newItem.setFont(textFont)					
						self.tableWidget_7.setItem(st_len+2,input_table[st_list-1],newItem)	

	def business_performance(self,stock_num):
		if stock_num != '':
			try:
				stock_num = str(self.stock_number_name.loc[stock_num].values).strip('[]')
				self.stock_info = '''SELECT * FROM OperatingPerformance WHERE sid=%s'''
				self.cursor.execute(self.stock_info,stock_num)
				stock_list = self.cursor.fetchall()

				self.tableWidget.setRowCount(len(stock_list)+3)
				for st_len in range(0,len(stock_list)):
					for st_list in range(1,len(stock_list[st_len])):
						input_table = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22]
						newItem = QTableWidgetItem(str(stock_list[len(stock_list)-st_len-1][st_list]))
						textFont = QFont("song", 12, QFont.Bold)  
						newItem.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
						newItem.setFont(textFont)					
						self.tableWidget.setItem(st_len+3,input_table[st_list-1],newItem)	
			except:
				self.stock_info = '''SELECT * FROM OperatingPerformance WHERE sid=%s'''
				self.cursor.execute(self.stock_info,stock_num)
				stock_list = self.cursor.fetchall()

				self.tableWidget.setRowCount(len(stock_list)+3)
				for st_len in range(0,len(stock_list)):
					for st_list in range(1,len(stock_list[st_len])):
						input_table = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22]
						newItem = QTableWidgetItem(str(stock_list[len(stock_list)-st_len-1][st_list]))
						textFont = QFont("song", 12, QFont.Bold)  
						newItem.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
						newItem.setFont(textFont)					
						self.tableWidget.setItem(st_len+3,input_table[st_list-1],newItem)	

	def dividend(self,stock_num):
		if stock_num != '':
			try:
				stock_num = str(self.stock_number_name.loc[stock_num].values).strip('[]')
				self.stock_info = '''SELECT * FROM EntitlementSchedule WHERE sid=%s'''
				self.cursor.execute(self.stock_info,stock_num)
				stock_list = self.cursor.fetchall()

				self.tableWidget_4.setRowCount(len(stock_list)+3)
				for st_len in range(0,len(stock_list)):
					for st_list in range(1,len(stock_list[st_len])):
						input_table = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
						newItem = QTableWidgetItem(str(stock_list[len(stock_list)-st_len-1][st_list]))
						textFont = QFont("song", 12, QFont.Bold)  
						newItem.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
						newItem.setFont(textFont)					
						self.tableWidget_4.setItem(st_len+3,input_table[st_list-1],newItem)	
			except:
				self.stock_info = '''SELECT * FROM EntitlementSchedule WHERE sid=%s'''
				self.cursor.execute(self.stock_info,stock_num)
				stock_list = self.cursor.fetchall()

				self.tableWidget_4.setRowCount(len(stock_list)+3)
				for st_len in range(0,len(stock_list)):
					for st_list in range(1,len(stock_list[st_len])):
						input_table = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
						newItem = QTableWidgetItem(str(stock_list[len(stock_list)-st_len-1][st_list]))
						textFont = QFont("song", 12, QFont.Bold)  
						newItem.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
						newItem.setFont(textFont)					
						self.tableWidget_4.setItem(st_len+3,input_table[st_list-1],newItem)


	def company_change(self,btn):
		if btn.text() == '公司基本資料':
			self.base_company(self.lineEdit_100.text())
		elif btn.text() == '公司服務資訊':
			self.service_company(self.lineEdit_100.text())

######################################################################################


#############################當視窗縮放將觸發此事件#####################################
	def resizeEvent(self, event):
		self.K_line(self.lineEdit_100.text(),self.comboBox_135.currentText())
######################################################################################

#############################K線圖的開高收低 & MA右鍵#####################################
	def addinfo(self,info):
		try:
			pe = QPalette()
			pe.setColor(QPalette.WindowText,Qt.red if info.split(' ')[1]>info.split(' ')[0] else QColor('#00BB00'))
			self.label.setText("最低價：" + info.split(' ')[3])
			self.label.setPalette(pe)
			self.label_2.setText("最高價：" + info.split(' ')[2])
			self.label_2.setPalette(pe)
			self.label_3.setText("收盤價：" + info.split(' ')[1])
			self.label_3.setPalette(pe)
			self.label_4.setText("開盤價：" + info.split(' ')[0])
			self.label_4.setPalette(pe)
		except:
			pass
	
	def MA_botton(self):
		self.K_line(self.lineEdit_100.text(),self.comboBox_135.currentText())
		self.ma_menu.hide()
############################################################################################

if __name__=="__main__":  
	app = QApplication(sys.argv)  
	with open('./other_file/record.txt','w') as f:
		f.truncate() 
	PcWin = PyechartsMainWindow() #Pyecharts
	page = PageMainWindow()
	#day = dayMainWindow()
	#market = MarketMainWindow()
	select = SelectMainWindow()
	#smart = SmartMainWindow()
	channel = QWebChannel()
	channel123 = QWebChannel()
	share = PyechartsMainWindow()
	share1 = SelectMainWindow()
	channel.registerObject("bridge",share)
	channel123.registerObject("bridge",share1)
	PcWin.webEngineView.page().setWebChannel(channel)
	select.webEngineView.page().setWebChannel(channel123)
	page.show()
	sys.exit(app.exec_())     