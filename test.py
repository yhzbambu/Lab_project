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
#引入UI檔
from ui_folder.filter import *


class MA_Menu_Window(QWidget, Ui_MainWindow):
	def __init__(self, parent=None): 
		super(MA_Menu_Window, self).__init__(parent)
		self.setupUi(self)

if __name__=="__main__":  
    app = QApplication(sys.argv)  
    abc = MA_Menu_Window() #Pyecharts
    abc.show()
    sys.exit(app.exec_())   