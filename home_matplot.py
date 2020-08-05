# -*- coding: utf-8 -*-

#引入pyqt5需要的模組
import sys 	
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
#引入UI檔
from matplotlibabc import *
from page import *
from uilogin import *
#引入其他輔助模組
from datetime import datetime,date
from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule,DAILY,WEEKLY,MONTHLY
import time
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd
import mpl_finance as mpf
import talib
import numpy as np
from matplotlib.widgets import Cursor
import pymysql

# config = {
# 'host':'localhost',
# 'port':3306,
# 'user':'root',
# 'password':'passwd',
# 'db':'database',
# }
# db = pymysql.connect(**config)
# cursor = db.cursor()
# cursor.execute("SELECT * FROM logininfo")
# datas = cursor.fetchall()

#以下class為登入的部分
class LoginMainWindow(QMainWindow, Ui_Dialog):
    def __init__(self, parent=None):    
        super(LoginMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(lambda:self.loginclick(self.pushButton))

    def loginclick(self,btn):
        # for data in datas:
        #     if (self.lineEdit.text() == data[1]):
        #         if (self.lineEdit_2.text() == data[2]):
        self.hide()
        HwWin.show()
            # else:
            #     self.label.setText("帳號/密碼 輸入錯誤")

#以下class為首頁的部分
class HomeMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):    
        super(HomeMainWindow, self).__init__(parent)
        self.setupUi(self)

        self.pushButton.clicked.connect(lambda:self.btclick(self.pushButton)) #點擊"顯示matplotlib"會跑出如下class的圖

    def btclick(self,btn): #將主頁隱藏，顯示圖形
        self.hide() 
        MtWin.show()

#以下class為matplotlib的部分
class MatPlotMainWindow(QMainWindow, Ui_FormHello):
    def __init__(self, parent=None):    
        super(MatPlotMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.figure = plt.figure() #設定matplotlib的畫布
        self.canvas = FigureCanvas(self.figure) #此行為在QT上建立畫布
        self.pushButton.clicked.connect(lambda:self.plot_(self.pushButton)) #點擊"顯示matplotlib"會跑出plot_函式的圖
        self.verticalLayout.addWidget(self.canvas) #將畫布添加到verticalLayout
        self.pushButton_3.clicked.connect(lambda:self.backpage(self.pushButton_3)) #點擊"上一頁"會跳到backpage函式，回到上一頁


    def plot_(self,btn):
        po_annotation = []
        red_macd = list()
        green_macd = list()

        dick = pd.read_excel("index_new.xls",index_col="Date",encoding='utf8') #讀取index_new.xls
        bitch = pd.read_csv("day_imformation_2330.csv",index_col="date",encoding='utf8') #讀取day_imformation_2330.csv
        bitch.columns = ["2330_stock","deal-stock","deal-money","open","high","low","close","up&down","Deal"] #設置每個項目的標題
        dick.columns = ["Kvalue","Dvalue","RSI","DIF","MACD"] #設置每個項目的標題
        #bitch取四年的值
        stock_date = str(bitch.index[-1]).split('/')
        stock_last_date = date(int(stock_date[0])+1911,int(stock_date[1]),int(stock_date[2]))
        stock_four_years = stock_last_date + relativedelta(years=-2) #最後一筆資料減四年
        split_stock_date = str(stock_last_date).split('-') #將得到的日期做切片
        split_four_stock = str(stock_four_years).split('-')
        join_stock_date = str(int(split_stock_date[0])-1911) + '/' + str(split_stock_date[1]) + '/' + str(split_stock_date[2]) #將日期組回index的樣式
        join_four_stock = str(int(split_four_stock[0])-1911) + '/' + str(split_four_stock[1]) + '/' + str(split_four_stock[2])
        bitch_two = bitch[join_four_stock:join_stock_date]
        #dick取四年的值
        split_date = list(dick.index)[-1].split('/')
        last_date = date(int(split_date[0])+1911,int(split_date[1]),int(split_date[2]))
        four_years = last_date + relativedelta(years=-2)
        split_last_date = str(last_date).split('-')
        split_four_years = str(four_years).split('-')
        join_last_date = str(int(split_last_date[0])-1911) + '/' + str(split_last_date[1]) + '/' + str(split_last_date[2])
        join_four_years = str(int(split_four_years[0])-1911) + '/' + str(split_four_years[1]) + '/' + str(split_four_years[2])
        dick_two = dick[join_four_years:join_last_date] #依照條件取出dataframe的要求

        ax = self.figure.add_subplot(2, 2, 1)
        ax2 = self.figure.add_subplot(2, 2, 2)
        ax3 = self.figure.add_subplot(2, 2, 3)
        ax4 = self.figure.add_subplot(2, 2, 4)
        plt.xlabel("Day")
        plt.ylabel("Price")

        mpf.candlestick2_ochl(ax, bitch_two['open'], bitch_two['close'], bitch_two['high'],bitch_two['low'], width=0.6, colorup='r', colordown='g', alpha=0.75); 

        def line(form,Ax,color,formname):
            len_y = len(form) #參數長度
            x = range(len_y) #從0~len_y
            _y = [list(form)[0]]*len_y #產生一個(len_y)長度的陣列
            line_x = Ax.plot(x, _y, color=color)[0] #畫水平線
            line_y = Ax.axvline(x=len_y-1, color='black',linestyle='--') #畫垂直線


            def motion(event):
                try:
                    temp = form[int(np.round(event.xdata))] #根據對應的x值把y值提出來
                    if formname == 'sma_60':
                        self.label.setText(str(temp))
                    if formname == 'sma_120':
                        self.label_3.setText(str(temp))
                    if formname == 'sma_240':
                        self.label_5.setText(str(temp))
                    if formname == 'dick_two["Kvalue"]':
                        self.label_7.setText(str(temp))
                    if formname == 'dick_two["Dvalue"]':
                        self.label_9.setText(str(temp))
                    if formname == 'dick_two["RSI"]':
                        self.label_11.setText(str(temp))    
                    if formname == 'dick_two["MACD"]':
                        self.label_13.setText(str(temp))                   
                    for i in range(len_y):
                        _y[i] = temp #將圖上得到的y值放入陣列裡
 
                    line_x.set_ydata(_y)
                    line_y.set_xdata(event.xdata)
                    #print("X：",event.xdata)
                    ######

                    self.figure.canvas.draw_idle() # 绘图动作实时反映在图像上
                except:
                    pass
            self.figure.canvas.mpl_connect('motion_notify_event', motion)

        sma_60 = talib.SMA(bitch_two['low'], 60)
        sma_120 = talib.SMA(bitch_two['low'], 120)
        sma_240 = talib.SMA(bitch_two['low'], 240)

        line(sma_60,ax,'lightgreen','sma_60')
        line(sma_120,ax,'crimson','sma_120')
        line(sma_240,ax,'purple','sma_240')
        line(dick_two["Kvalue"],ax2,'blue','dick_two["Kvalue"]')
        line(dick_two["Dvalue"],ax2,'red','dick_two["Dvalue"]')
        line(dick_two["RSI"],ax3,'blue','dick_two["RSI"]')
        line(dick_two["MACD"],ax4,'skyblue','dick_two["MACD"]')

        ax.plot(sma_60,label='MA_60',color='lightgreen')
        ax.plot(sma_120,label='MA_120',color='crimson')
        ax.plot(sma_240,label='MA_240',color='purple')
        ax2.plot(dick_two["Kvalue"],label='Kvalue',color='blue')
        ax2.plot(dick_two["Dvalue"],label='Dvalue',color='red')
        ax3.plot(dick_two["RSI"],label='RSI',color='blue')
        ax4.plot(dick_two["DIF"],label='DIF')

        dick_two["MACD"].plot(ax=ax4, color='r', kind='bar', legend=True)

        ax.set_xticks(range(0, len(bitch_two.index), int(len(bitch_two.index)/8)))
        ax.set_xticklabels(bitch_two.index[::int(len(bitch_two.index)/8)])
        ax.set_yticks(range(200,400,50))
        ax2.set_xticks(range(0, len(dick_two.index), int(len(dick_two.index)/8)))
        ax2.set_xticklabels(dick_two.index[::int(len(dick_two.index)/8)])
        ax3.set_xticks(range(0, len(dick_two.index), int(len(dick_two.index)/8)))
        ax3.set_xticklabels(dick_two.index[::int(len(dick_two.index)/8)])
        ax4.set_xticks(range(0, len(dick_two.index), int(len(dick_two.index)/8)))
        ax4.set_xticklabels(dick_two.index[::int(len(dick_two.index)/8)])
        ax.legend(loc=2)
        ax2.legend(loc=2)
        ax3.legend(loc=2)
        ax4.legend(loc=2)
        #plt.savefig("fuck.png")

        self.canvas.draw()  
    def backpage(self,btn3): #隱藏matplotlib，顯示主頁
        self.hide()
        HwWin.show()

if __name__=="__main__":  
    app = QApplication(sys.argv)  
    HwWin = HomeMainWindow() #首頁
    MtWin = MatPlotMainWindow() #matplotlib
    LgWin = LoginMainWindow() #Login
    LgWin.show() #顯示主頁
    sys.exit(app.exec_())     
db.close()            