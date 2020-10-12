# -*- coding: utf-8 -*-

#引入pyqt5需要的模組
import sys 	
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
#引入UI檔
from matplotlibpage import *
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
import re

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
# class LoginMainWindow(QMainWindow, Ui_Dialog):
#     def __init__(self, parent=None):    
#         super(LoginMainWindow, self).__init__(parent)
#         self.setupUi(self)
#         self.pushButton.clicked.connect(lambda:self.loginclick(self.pushButton))

    #def loginclick(self,btn):
        # for data in datas:
        #     if (self.lineEdit.text() == data[1]):
        #         if (self.lineEdit_2.text() == data[2]):
        # self.hide()
        # HwWin.show()
            # else:
            #     self.label.setText("帳號/密碼 輸入錯誤")

#以下class為首頁的部分
# class HomeMainWindow(QMainWindow, Ui_MainWindow):
#     def __init__(self, parent=None):    
#         super(HomeMainWindow, self).__init__(parent)
#         self.setupUi(self)

    #     self.pushButton.clicked.connect(lambda:self.btclick(self.pushButton)) #點擊"顯示matplotlib"會跑出如下class的圖

    # def btclick(self,btn): #將主頁隱藏，顯示圖形
    #     self.hide() 
    #     MtWin.show()

#以下class為matplotlib的部分
class MatPlotMainWindow(QMainWindow, Ui_Matplot):
    
    def __init__(self, parent=None):    
        super(MatPlotMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.figure = plt.figure() #設定matplotlib的畫布
        self.canvas = FigureCanvas(self.figure) #此行為在QT上建立畫布
        self.pushButton.clicked.connect(lambda:self.plot_(3)) #點擊搜尋會跑出plot_函式的圖
        self.verticalLayout.addWidget(self.canvas) #將畫布添加到verticalLayout
        self.pushButton_3.clicked.connect(lambda:self.backpage(self.pushButton_3)) #點擊"上一頁"會跳到backpage函式，回到上一頁
        self.lineEdit.textChanged.connect(self.searchitem)
        self.listView.clicked.connect(self.inputtext)
        self.qlist = list()
        self.pushButton.clicked.connect(self.searchdisappear)
        self.stock_number_name = pd.read_csv("./stock_number_name.csv",index_col="名稱",encoding='utf8') #讀取stock_number_name.csv
        self.tabWidget.currentChanged['int'].connect(self.onChange)


    def plot_(self,month_number):

        high_values = list()
        low_values = list()
        plt.clf()
        global bitch
        global stock_four_years
        global stock_last_date
        if self.lineEdit.text():
            try:
                fuck = str(self.stock_number_name.loc[self.lineEdit.text()].values).strip('[]')
                dick = pd.read_excel("./stock_index/indexOf" + fuck + ".xls",index_col="Date",encoding='utf8') #讀取index_new.xls
                bitch = pd.read_csv("./allstock/twse_day_imformation_" + fuck + ".csv",index_col="日期",encoding='utf8') #讀取day_imformation_2330.csv
            except:
                dick = pd.read_excel("./stock_index/indexOf" + self.lineEdit.text() + ".xls",index_col="Date",encoding='utf8') #讀取index_new.xls
                bitch = pd.read_csv("./allstock/twse_day_imformation_" + self.lineEdit.text() + ".csv",index_col="日期",encoding='utf8') #讀取day_imformation_2330.csv
        
        bitch.columns = ["2330_stock","deal-stock","deal-money","open","high","low","close","up&down","Deal"] #設置每個項目的標題
        dick.columns = ["Kvalue","Dvalue","RSI","DIF","MACD"] #設置每個項目的標題
        stock_date = str(bitch.index[-1]).split('/')
        stock_last_date = date(int(stock_date[0])+1911,int(stock_date[1]),int(stock_date[2]))
        stock_four_years = stock_last_date + relativedelta(months=-int(month_number)) #最後一筆資料減四年
        split_stock_date = str(stock_last_date).split('-') #將得到的日期做切片
        split_four_stock = str(stock_four_years).split('-')
        join_stock_date = str(int(split_stock_date[0])-1911) + '/' + str(split_stock_date[1]) + '/' + str(split_stock_date[2]) #將日期組回index的樣式
        join_four_stock = str(int(split_four_stock[0])-1911) + '/' + str(split_four_stock[1]) + '/' + str(split_four_stock[2])
        bitch_two = bitch[join_four_stock:]
        ##以下為過濾資料   
        count = 0
        for bitch_high in bitch_two['high']:
            if bitch_high == '--':
                bitch_two['high'][count] = '0'
            count += 1
        count = 0
        for bitch_low in bitch_two['low']:
            if bitch_low == '--':
                bitch_two['low'][count] = '0'
            count += 1
        count = 0
        for bitch_open in bitch_two['open']:
            if bitch_open == '--':
                bitch_two['open'][count] = '0'
            count += 1
        count = 0
        for bitch_close in bitch_two['close']:
            if bitch_close == '--':
                bitch_two['close'][count] = '0'
            count += 1
        #####################################
        for index,row in bitch_two.iterrows():
            high_values.append(int(float(row["high"])))
            low_values.append(int(float(row["low"])))
        high_value = max(high_values)
        low_value = min(low_values)
        #dick取四年的值
        split_date = list(dick.index)[-1].split('/')
        last_date = date(int(split_date[0])+1911,int(split_date[1]),int(split_date[2]))
        four_years = last_date + relativedelta(months=-int(month_number))
        split_last_date = str(last_date).split('-')
        split_four_years = str(four_years).split('-')
        join_last_date = str(int(split_last_date[0])-1911) + '/' + str(split_last_date[1]) + '/' + str(split_last_date[2])
        join_four_years = str(int(split_four_years[0])-1911) + '/' + str(split_four_years[1]) + '/' + str(split_four_years[2])
        dick_two = dick[join_four_years:] #依照條件取出dataframe的要求
        if max(dick_two["MACD"]) > max(dick_two["DIF"]):
            high_macd_value = max(dick_two["MACD"])
        else:
            high_macd_value = max(dick_two["DIF"])
        #以下為四張圖的設定
        ax = self.figure.add_axes([0.05,0.65,0.9,0.30])
        ax2 = self.figure.add_axes([0.05,0.45,0.9,0.15], sharex=ax)
        ax3 = self.figure.add_axes([0.05,0.25,0.9,0.15], sharex=ax)
        ax4 = self.figure.add_axes([0.05,0.05,0.9,0.15], sharex=ax)
        #以下為設定個圖的X軸不顯示
        plt.setp(ax.get_xticklabels(), visible=False)
        plt.setp(ax2.get_xticklabels(), visible=False)
        plt.setp(ax3.get_xticklabels(), visible=False)

        mpf.candlestick2_ochl(ax, bitch_two['open'], bitch_two['close'], bitch_two['high'], bitch_two['low'], width=0.6, colorup='r', colordown='g', alpha=0.75); #生成蠟燭圖

        def line(form,Ax,color,formname):
            len_y = len(form) #參數長度
            x = range(len_y) #從0~len_y
            _y = [list(form)[0]]*len_y #產生一個(len_y)長度的陣列
            line_x = Ax.plot(x, _y, color=color)[0] #畫水平線
            line_y = Ax.axvline(x=len_y-1, color='black',linestyle='--') #畫垂直線
            ###以下為數值放置文本的設定
            if high_value > 200:
                high_200 = ((high_value/0.9)-(low_value*0.9)) / 30
                target = int((low_value*0.9)+(30*int(high_200)))+0.5
                ax_text = ax.text(5,target," ",fontsize=12)
            elif 100 < high_value < 200:
                high_100 = ((high_value/0.9)-(low_value*0.9)) / 10
                target = int((low_value*0.9)+(10*int(high_100)))+0.5
                ax_text = ax.text(5,target," ",fontsize=12)
            elif  30 < high_value <= 100:
                high_30 = ((high_value/0.9)-(low_value*0.9)) / 5
                target = int((low_value*0.9)+(5*int(high_30)))+0.5
                ax_text = ax.text(5,target," ",fontsize=12)
            else:
                high_other = ((high_value+3)-(low_value-2)) / 3
                target = int(low_value-2)+(int(high_other)*3)+0.5
                ax_text = ax.text(5,target," ",fontsize=12)
            ax2_text = ax2.text(5,100.5," ",fontsize=12)
            if high_macd_value > 9:
                macd_target = high_macd_value+int(high_macd_value/2.5)
                ax3_text = ax3.text(5,macd_target," ",fontsize=12)
            elif  5 < high_macd_value <= 9:
                macd_target = high_macd_value+int(high_macd_value/2.5)
                ax3_text = ax3.text(5,macd_target," ",fontsize=12)
            elif 3 < high_macd_value <= 5:
                macd_target = high_macd_value+0.5
                ax3_text = ax3.text(5,macd_target," ",fontsize=12)
            elif 1 < high_macd_value <= 3:
                macd_target = high_macd_value+0.55
                ax3_text = ax3.text(5,macd_target," ",fontsize=12)
            elif 0 < high_macd_value <= 1:
                macd_target = high_macd_value+0.2
                ax3_text = ax3.text(5,macd_target," ",fontsize=12)
            ax4_text = ax4.text(5,101," ",fontsize=12)
            ##############################################
            def motion(event):
                try:
                    temp = form[int(np.round(event.xdata))] #根據對應的x值把y值提出來
                    temp_as = temp.astype('float16')
                                        
                    if formname == "sma_10":
                        ax_text.set_text("up line:"+str(temp_as))
                        ax_text.set_color("purple")
                    if formname == "sma_20":
                        ax_text.set_position([30,target])
                        ax_text.set_text("MA20:"+str(temp_as))
                        ax_text.set_color("crimson")
                    if formname == "sma_60":
                        ax_text.set_position([55,target])
                        ax_text.set_text("low line:"+str(temp_as))
                        ax_text.set_color("lightgreen")
                    if formname == 'dick_two["Kvalue"]':
                        ax2_text.set_text("Kvalue:"+str(temp_as))
                        ax2_text.set_color("blue")
                    if formname == 'dick_two["Dvalue"]':
                        ax2_text.set_position([20,100.5])
                        ax2_text.set_text("Dvalue:"+str(temp_as))
                        ax2_text.set_color("red")
                    if formname == 'dick_two["RSI"]':
                        ax4_text.set_text("RSI:"+str(temp_as))
                        ax4_text.set_color("blue")
                    if formname == 'dick_two["DIF"]':
                        ax3_text.set_text("DIF:"+str(temp_as))
                        ax3_text.set_color("skyblue")
                    for i in range(len_y):
                        _y[i] = temp #將圖上得到的y值放入陣列裡
                    line_x.set_ydata(_y)
                    line_y.set_xdata(event.xdata)
                    #print("X：",event.xdata)
                    ######
                    self.figure.canvas.draw_idle() # 繪製matplotlib
                except:
                    pass
            self.figure.canvas.mpl_connect('motion_notify_event', motion)


        sma_10 = talib.SMA(bitch_two['low'], 10)
        sma_20 = talib.SMA(bitch_two['low'], 20)
        sma_60 = talib.SMA(bitch_two['low'], 60)
        #sma_120 = talib.SMA(bitch_two['low'], 120)
        #sma_240 = talib.SMA(bitch_two['low'], 240)
        H_line,M_line,L_line=talib.BBANDS(bitch_two['close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
        line(H_line,ax,'purple','sma_10')
        line(M_line,ax,'crimson','sma_20')
        line(L_line,ax,'lightgreen','sma_60')
        #line(sma_120,ax,'crimson','sma_120')
        #line(sma_240,ax,'purple','sma_240')
        line(dick_two["Kvalue"],ax2,'blue','dick_two["Kvalue"]')
        line(dick_two["Dvalue"],ax2,'red','dick_two["Dvalue"]')
        line(dick_two["RSI"],ax4,'blue','dick_two["RSI"]')
        line(dick_two["DIF"],ax3,'skyblue','dick_two["DIF"]')

        ax.plot(H_line,label='MA_10',color='crimson')
        ax.plot(M_line,label='MA_20',color='purple')
        ax.plot(L_line,label='MA_60',color='lightgreen')
        #ax.plot(sma_120,label='MA_120',color='crimson')
        #ax.plot(sma_240,label='MA_240',color='purple')
        ax2.plot(dick_two["Kvalue"],label='Kvalue',color='blue')
        ax2.plot(dick_two["Dvalue"],label='Dvalue',color='red')
        ax4.plot(dick_two["RSI"],label='RSI',color='blue')
        ax3.plot(dick_two["DIF"],label='DIF',color='skyblue')

        ax3.set_xlim(xmin=0,xmax=len(dick_two["MACD"]))
        for row in range(len(dick_two["MACD"])):
            ax3.bar(row,dick_two["MACD"][row],color='r' if dick_two["MACD"][row] > 0 else 'g')

        ax.set_xticks(range(0, len(bitch_two.index), int(len(bitch_two.index)/8)))
        ax.set_xticklabels(bitch_two.index[::int(len(bitch_two.index)/8)])
        #以下為調整蠟燭圖，防止圖超出邊界
        if high_value > 200:
            ax.set_yticks(range(int(low_value*0.9),int(high_value/0.9),30))
        elif 100 < high_value < 200:
            ax.set_yticks(range(int(low_value*0.9),int(high_value/0.9),10))
        elif  30 < high_value < 100:
            ax.set_yticks(range(int(low_value*0.9),int(high_value/0.9),5))
        else:
            ax.set_yticks(range(int(low_value-2),int(high_value+3),3))
        ###########################

        self.canvas.draw()  
    # def backpage(self,btn3): #隱藏matplotlib，顯示主頁
    #     self.hide()
    #     HwWin.show()

    # def deal_stock(self,bitch,view_month):
    #     global bitch_two
    #     self.stock_date = str(bitch.index[-1]).split('/')
    #     self.stock_last_date = date(int(self.stock_date[0])+1911,int(self.stock_date[1]),int(self.stock_date[2]))
    #     self.stock_four_years = self.stock_last_date + relativedelta(months=-int(view_month)) #最後一筆資料減四年
    #     self.split_stock_date = str(self.stock_last_date).split('-') #將得到的日期做切片
    #     self.split_four_stock = str(self.stock_four_years).split('-')
    #     self.join_stock_date = str(int(self.split_stock_date[0])-1911) + '/' + str(self.split_stock_date[1]) + '/' + str(self.split_stock_date[2]) #將日期組回index的樣式
    #     self.join_four_stock = str(int(self.split_four_stock[0])-1911) + '/' + str(self.split_four_stock[1]) + '/' + str(self.split_four_stock[2])
    #     bitch_two = bitch[self.join_four_stock:] 

    def searchitem(self,text):
        self.qlist.clear()
        if (text == ''):
            self.listView.hide()
        else:
            self.listView.show()
            for stock_number in self.stock_number_name['代號']:
                result_number = re.match('(.*'+text+'.*)',str(stock_number),flags=0)
                if (result_number != None):
                    self.qlist.append(str(stock_number))
            for stock_number in self.stock_number_name.index:
                result_text = re.match('(.*'+text+'.*)',str(stock_number),flags=0)
                if (result_text != None):
                    self.qlist.append(stock_number)
            
            slm = QStringListModel()
            slm.setStringList(self.qlist)
            self.listView.setModel(slm)

    def inputtext(self,qModelIndex):
        self.lineEdit.setText(self.qlist[qModelIndex.row()])
        self.listView.hide()

    def searchdisappear(self):
        self.listView.hide()

    def onChange(self,index):
        currentTab = self.tabWidget.currentIndex()
        if currentTab == 0:
            self.plot_(3)
            self.verticalLayout.addWidget(self.canvas) #將畫布添加到verticalLayout
        if currentTab == 1:
            self.plot_(6)
            self.verticalLayout_2.addWidget(self.canvas) #將畫布添加到verticalLayout_2
        if currentTab == 2:
            self.plot_(12)
            self.verticalLayout_3.addWidget(self.canvas) #將畫布添加到verticalLayout_3
            

if __name__=="__main__":  
    app = QApplication(sys.argv)  
    #HwWin = HomeMainWindow() #首頁
    MtWin = MatPlotMainWindow() #matplotlib
    MtWin.show()
    #LgWin = LoginMainWindow() #Login
    #LgWin.show() #顯示主頁
    sys.exit(app.exec_())     
db.close()      