from datetime import datetime
import time
import math
import sys
import os
import pymysql
import decimal
from decimal import Decimal

def historytest(buynamelist,buynumberlist,sellnamelist,sellnumberlist,datelist,ssid):
    buylist={}
    selllist={}
    money=[]
    for i in range(len(buynamelist)): #將條件放入字典
        buylist[buynamelist[i]]=buynumberlist[i]
    for i in range(len(sellnamelist)):
        selllist[sellnamelist[i]]=sellnumberlist[i]
    #建立各自紀錄list，最後確認用
    buydaysmemory=[0 for i in range(len(buylist))]
    checkbuylist=['' for i in range(len(buylist))]
    selldaysmemory=[0 for i in range(len(selllist))]
    checkselllist=['' for i in range(len(selllist))]
    #取資料
    conn=pymysql.connect(host="163.18.104.164",
                    user="bobo",
                    password="bobo123",
                    db='stock',
                    charset='utf8'
                    )
    cursor=conn.cursor()
    cursor.execute("select * from DayStockInformation where sid='%d'" %(ssid)) #取得該股票所有的日成交資料
    results=list(cursor.fetchall()) #放入results中
    cursor.execute("select * from WeekStockInformation where sid='%d'" %(ssid))#週成交
    weekresults=list(cursor.fetchall())
    cursor.execute("select * from MonthStockInformation where sid='%d'" %(ssid))#月成交
    monthresults=list(cursor.fetchall())
    cursor.execute("select * from institutional_investors where sid='%d'" %(ssid)) #三大法人
    threeresults=list(cursor.fetchall())
    cursor.execute("select * from MarginPurchase_ShortSale where sid='%d'" %(ssid))#融資融券
    chan=list(cursor.fetchall())
    #紀錄區間
    d1 = datetime.strptime(datelist[0],'%Y/%m/%d').date()
    d2 = datetime.strptime(datelist[1],'%Y/%m/%d').date()  
    #d1 = datetime.date(datelist[0],datelist[1],datelist[2])   
    #d2 = datetime.date(datelist[3],datelist[4],datelist[5])
    newday=[] #放該區段的日成交資料
    newweek=[] #放該區段的週成交資料
    weeklist=[] #放週別
    newmonth=[] #放該區段的月成交資料
    monthlist=[] #放月別
    newthree=[] #放該區段的三大法人資料
    newchan=[] #放該區段的融資融券資料
    abc=0
    for i in range(len(results)): #放日成交
        if(results[i][1]>= d1 and results[i][1]<d2):
            newday.append(results[i])
            abc+=1
        if(results[i][1]==d2):
            newday.append(results[i])
            abc+=1
            break
    for i in range(len(threeresults)): #放三大法人
        if(threeresults[i][1]>= d1 and threeresults[i][1]<d2):
            newthree.append(threeresults[i])
        if(threeresults[i][1]==d2):
            newthree.append(threeresults[i])
            break
    for i in range(len(chan)): #放融資融券
        if(chan[i][1]>= d1 and chan[i][1]<d2):
            newchan.append(chan[i])
        if(chan[i][1]==d2):
            newchan.append(chan[i])
            break
    for j in range(abc):  #放週成交
        for i in range(len(weekresults)):    
            if(newday[j][1]>= weekresults[i][27] and newday[j][1]<=weekresults[i][28]):
                if(j==0): #第一位置一定放
                    weeklist.append(weekresults[i][1]) #放週別
                    newweek.append(weekresults[i]) #放週資料
                    continue
                else:
                    if(weekresults[i][1]==weeklist[j-1]): #如果跟前者一樣就放週別就好
                        weeklist.append(weekresults[i][1])
                        continue
                    else:
                        weeklist.append(weekresults[i][1]) #放週別
                        newweek.append(weekresults[i]) #放週資料
    for j in range(abc): #放月成交   
        for i in range(len(monthresults)):        
            if(newday[j][1]>= monthresults[i][27] and newday[j][1]<=monthresults[i][28]):
                if(j==0): #第一位置一定放
                    monthlist.append(monthresults[i][1]) #放月別
                    newmonth.append(monthresults[i]) #放月資料
                    continue
                else:
                    if(monthresults[i][1]==monthlist[j-1]): #如果跟前者一樣就放週別就好
                        monthlist.append(monthresults[i][1])
                        continue
                    else:
                        monthlist.append(monthresults[i][1]) #放月別
                        newmonth.append(monthresults[i]) #放月資料
    #開始交易
    count=0 #無持股
    weekcount=0 
    monthcount=0
    totalday=[[] for i in range(3)] #算交易日期(0:買、1:賣、2:未交易)
    for i in range(len(newday)):
        weeknumber=i
        counter=-1
        if(weeknumber!=0):
            if(weeklist[weeknumber]!=weeklist[weeknumber-1]): #不同代表下週了!
                weekcount+=1
            if(monthlist[weeknumber]!=monthlist[weeknumber-1]): #不同代表下個月了!
                monthcount+=1
        if(count==0): #只需關心買入條件 
            for key in buylist:
                counter+=1
                if(key=='日K'): #若為日K判斷
                    buydaysmemory[counter]=KD(buylist[key][0],buylist[key][1],buydaysmemory[counter],newday[i][10])
                    checkbuylist[counter]=checkday(buydaysmemory[counter],buylist[key][2])
                if(key=='週K'): #若為週K判斷
                    if(weeknumber==0): #不用檢查前一個
                        buydaysmemory[counter]=KD(buylist[key][0],buylist[key][1],buydaysmemory[counter],newweek[weekcount][10])
                        checkbuylist[counter]=checkday(buydaysmemory[counter],buylist[key][2])
                    else: #檢查前一個的週別是否一樣，一樣就不用再做判斷
                        if(weeklist[weeknumber]!=weeklist[weeknumber-1]):
                            buydaysmemory[counter]=KD(buylist[key][0],buylist[key][1],buydaysmemory[counter],newweek[weekcount][10])
                            checkbuylist[counter]=checkday(buydaysmemory[counter],buylist[key][2])
                if(key=='月K'): #若為月K判斷
                    if(weeknumber==0): #不用檢查前一個
                        buydaysmemory[counter]=KD(buylist[key][0],buylist[key][1],buydaysmemory[counter],newmonth[monthcount][10])
                        checkbuylist[counter]=checkday(buydaysmemory[counter],buylist[key][2])
                    else: #檢查前一個的週別是否一樣，一樣就不用再做判斷
                        if(monthlist[weeknumber]!=monthlist[weeknumber-1]):
                            buydaysmemory[counter]=KD(buylist[key][0],buylist[key][1],buydaysmemory[counter],newmonth[monthcount][10])
                            checkbuylist[counter]=checkday(buydaysmemory[counter],buylist[key][2])
                if(key=='日D'): #若為日D判斷
                    buydaysmemory[counter]=KD(buylist[key][0],buylist[key][1],buydaysmemory[counter],newday[i][11])
                    checkbuylist[counter]=checkday(buydaysmemory[counter],buylist[key][2])
                if(key=='週D'): #若為週D判斷
                    if(weeknumber==0): #不用檢查前一個
                        buydaysmemory[counter]=KD(buylist[key][0],buylist[key][1],buydaysmemory[counter],newweek[weekcount][11])
                        checkbuylist[counter]=checkday(buydaysmemory[counter],buylist[key][2])
                    else: #檢查前一個的週別是否一樣，一樣就不用再做判斷
                        if(weeklist[weeknumber]!=weeklist[weeknumber-1]): #週別不一樣再做就好，否則不變
                            buydaysmemory[counter]=KD(buylist[key][0],buylist[key][1],buydaysmemory[counter],newweek[weekcount][11])
                            checkbuylist[counter]=checkday(buydaysmemory[counter],buylist[key][2])
                if(key=='月D'): #若為月D判斷
                    if(weeknumber==0): #不用檢查前一個
                        buydaysmemory[counter]=KD(buylist[key][0],buylist[key][1],buydaysmemory[counter],newmonth[monthcount][11])
                        checkbuylist[counter]=checkday(buydaysmemory[counter],buylist[key][2])
                    else: #檢查前一個的週別是否一樣，一樣就不用再做判斷
                        if(monthlist[weeknumber]!=monthlist[weeknumber-1]):
                            buydaysmemory[counter]=KD(buylist[key][0],buylist[key][1],buydaysmemory[counter],newmonth[monthcount][11])
                            checkbuylist[counter]=checkday(buydaysmemory[counter],buylist[key][2])
                if(key=='日KD'): #若為黃金或死亡交叉
                    if(newday[i][10]==newday[i][11]): #交叉
                        buydaysmemory[counter]=GD(results,newday[i][1],newday[i][10],newday[i][11],10,11,buylist[key][0])
                        checkbuylist[counter]=checkother(buydaysmemory[counter])
                    else:
                        buydaysmemory[counter]=12
                        checkbuylist[counter]=checkother(buydaysmemory[counter])
                if(key=='週KD'): #若為黃金或死亡交
                    if(weeknumber==0): #不用檢查前一個
                        if(newweek[weekcount][10]==newweek[weekcount][11]): #交叉
                            buydaysmemory[counter]=GD(weekresults,newweek[weekcount][1],newweek[weekcount][10],newweek[weekcount][11],10,11,buylist[key][0])
                            checkbuylist[counter]=checkother(buydaysmemory[counter])
                        else:
                            buydaysmemory[counter]=12
                            checkbuylist[counter]=checkother(buydaysmemory[counter])
                    else:
                        if(weeklist[weeknumber]!=weeklist[weeknumber-1]):  #檢查前一個的週別是否一樣，一樣就不用再做判斷
                            buydaysmemory[counter]=GD(weekresults,newweek[weekcount][1],newweek[weekcount][10],newweek[weekcount][11],10,11,buylist[key][0])
                            checkbuylist[counter]=checkother(buydaysmemory[counter])   
                if(key=='月KD'): #若為黃金或死亡交叉
                    if(weeknumber==0): #不用檢查前一個
                        if(newmonth[monthcount][10]==newmonth[monthcount][11]): #交叉
                            buydaysmemory[counter]=GD(monthresults,newmonth[monthcount][1],newmonth[monthcount][10],newmonth[monthcount][11],10,11,buylist[key][0])
                            checkbuylist[counter]=checkother(buydaysmemory[counter])
                        else:
                            buydaysmemory[counter]=12
                            checkbuylist[counter]=checkother(buydaysmemory[counter])
                    else:
                        if(monthlist[weeknumber]!=monthlist[weeknumber-1]):  #檢查前一個的週別是否一樣，一樣就不用再做判斷
                            buydaysmemory[counter]=GD(monthresults,newmonth[monthcount][1],newmonth[monthcount][10],newmonth[monthcount][11],10,11,buylist[key][0]) 
                            checkbuylist[counter]=checkother(buydaysmemory[counter]) 
                if(key=='日MACD'): #若為日MACD判斷
                    buydaysmemory[counter]=KD(buylist[key][0],buylist[key][1],buydaysmemory[counter],newday[i][15])
                    checkbuylist[counter]=checkday(buydaysmemory[counter],buylist[key][2])
                if(key=='週MACD'): #若為週MACD判斷
                    if(weeknumber==0): #不用檢查前一個
                        buydaysmemory[counter]=KD(buylist[key][0],buylist[key][1],buydaysmemory[counter],newweek[weekcount][15])
                        checkbuylist[counter]=checkday(buydaysmemory[counter],buylist[key][2])
                    else: #檢查前一個的週別是否一樣，一樣就不用再做判斷
                        if(weeklist[weeknumber]!=weeklist[weeknumber-1]):
                            buydaysmemory[counter]=KD(buylist[key][0],buylist[key][1],buydaysmemory[counter],newweek[weekcount][15])
                            checkbuylist[counter]=checkday(buydaysmemory[counter],buylist[key][2])
                if(key=='月MACD'): #若為月MACD判斷
                    if(weeknumber==0): #不用檢查前一個
                        buydaysmemory[counter]=KD(buylist[key][0],buylist[key][1],buydaysmemory[counter],newmonth[monthcount][15])
                    else: #檢查前一個的週別是否一樣，一樣就不用再做判斷
                        if(monthlist[weeknumber]!=monthlist[weeknumber-1]):
                            buydaysmemory[counter]=KD(buylist[key][0],buylist[key][1],buydaysmemory[counter],newmonth[monthcount][15])                    
                if(key=='日DIF'): #若為日DIF判斷
                    buydaysmemory[counter]=KD(buylist[key][0],buylist[key][1],buydaysmemory[counter],newday[i][22])
                    checkbuylist[counter]=checkday(buydaysmemory[counter],buylist[key][2])
                if(key=='週DIF'): #若為週DIF判斷
                    if(weeknumber==0): #不用檢查前一個
                        buydaysmemory[counter]=KD(buylist[key][0],buylist[key][1],buydaysmemory[counter],newweek[weekcount][22])
                        checkbuylist[counter]=checkday(buydaysmemory[counter],buylist[key][2])
                    else: #檢查前一個的週別是否一樣，一樣就不用再做判斷
                        if(weeklist[weeknumber]!=weeklist[weeknumber-1]):
                            buydaysmemory[counter]=KD(buylist[key][0],buylist[key][1],buydaysmemory[counter],newweek[weekcount][22])
                            checkbuylist[counter]=checkday(buydaysmemory[counter],buylist[key][2])
                if(key=='月DIF'): #若為月DIF判斷
                    if(weeknumber==0): #不用檢查前一個
                        buydaysmemory[counter]=KD(buylist[key][0],buylist[key][1],buydaysmemory[counter],newmonth[monthcount][22])
                        checkbuylist[counter]=checkday(buydaysmemory[counter],buylist[key][2])
                    else: #檢查前一個的週別是否一樣，一樣就不用再做判斷
                        if(monthlist[weeknumber]!=monthlist[weeknumber-1]):
                            buydaysmemory[counter]=KD(buylist[key][0],buylist[key][1],buydaysmemory[counter],newmonth[monthcount][22])
                            checkbuylist[counter]=checkday(buydaysmemory[counter],buylist[key][2])
                if(key=='日MACD落點'): #日MACD落點判斷
                    buydaysmemory[counter]=Place(buylist[key][0],newday[i][15],newday[i][22])
                    checkbuylist[counter]=checkother(buydaysmemory[counter])
                if(key=='週MACD落點'): #週MACD落點判斷
                    if(weeknumber==0):
                        buydaysmemory[counter]=Place(buylist[key][0],newweek[weekcount][15],newweek[weekcount][22])
                        checkbuylist[counter]=checkother(buydaysmemory[counter])
                    else:
                        if(weeklist[weeknumber]!=weeklist[weeknumber-1]):
                           buydaysmemory[counter]=Place(buylist[key][0],newweek[weekcount][15],newweek[weekcount][22])
                           checkbuylist[counter]=checkother(buydaysmemory[counter]) 
                if(key=='月MACD落點'): #月MACD落點判斷
                    if(weeknumber==0):
                        buydaysmemory[counter]=Place(buylist[key][0],newmonth[monthcount][15],newmonth[monthcount][22])
                        checkbuylist[counter]=checkother(buydaysmemory[counter])
                    else:
                        if(monthlist[weeknumber]!=monthlist[weeknumber-1]):
                            buydaysmemory[counter]=Place(buylist[key][0],newmonth[monthcount][15],newmonth[monthcount][22]) 
                            checkbuylist[counter]=checkother(buydaysmemory[counter])
                if(key=='日MACD，日DIF'): #日MACD、DIF交叉判斷
                    if(newday[i][15]==newday[i][22]): #交叉
                        buydaysmemory[counter]=GD(results,newday[i][1],newday[i][22],newday[i][15],22,15,buylist[key][0])
                        checkbuylist[counter]=checkother(buydaysmemory[counter])
                    else:
                        buydaysmemory[counter]=12
                        checkbuylist[counter]=checkother(buydaysmemory[counter])
                if(key=='週MACD，週DIF'): #週MACD、DIF交叉判斷
                    if(weeknumber==0): #不用檢查前一個
                        if(newweek[weekcount][15]==newweek[weekcount][22]): #交叉
                            buydaysmemory[counter]=GD(weekresults,newweek[weekcount][1],newweek[weekcount][22],newweek[weekcount][15],22,15,buylist[key][0])
                            checkbuylist[counter]=checkother(buydaysmemory[counter])
                        else:
                            buydaysmemory[counter]=12
                            checkbuylist[counter]=checkother(buydaysmemory[counter])
                    else:
                        if(weeklist[weeknumber]!=weeklist[weeknumber-1]):  #檢查前一個的週別是否一樣，一樣就不用再做判斷
                            buydaysmemory[counter]=GD(weekresults,newweek[weekcount][1],newweek[weekcount][22],newweek[weekcount][15],22,15,buylist[key][0])
                            checkbuylist[counter]=checkother(buydaysmemory[counter])
                if(key=='月MACD，月DIF'): #月MACD、DIF交叉判斷
                    if(weeknumber==0): #不用檢查前一個
                        if(newmonth[monthcount][15]==newmonth[monthcount][22]): #交叉
                            buydaysmemory[counter]=GD(monthresults,newmonth[monthcount][1],newmonth[monthcount][22],newmonth[monthcount][15],22,15,buylist[key][0])
                            checkbuylist[counter]=checkother(buydaysmemory[counter])
                        else:
                            buydaysmemory[counter]=12
                            checkbuylist[counter]=checkother(buydaysmemory[counter])
                    else:
                        if(monthlist[weeknumber]!=monthlist[weeknumber-1]):  #檢查前一個的週別是否一樣，一樣就不用再做判斷
                            buydaysmemory[counter]=GD(monthresults,newmonth[monthcount][1],newmonth[monthcount][22],newmonth[monthcount][15],22,15,buylist[key][0])
                            checkbuylist[counter]=checkother(buydaysmemory[counter])  
                if(key=='日RSI(6)'):   #若為日RSI(6)判斷
                    buydaysmemory[counter]=KD(buylist[key][0],buylist[key][1],buydaysmemory[counter],newday[i][12])
                    checkbuylist[counter]=checkday(buydaysmemory[counter],buylist[key][2])
                if(key=='週RSI(6)'):   #若為週RSI(6)判斷
                    if(weeknumber==0): #不用檢查前一個
                        buydaysmemory[counter]=KD(buylist[key][0],buylist[key][1],buydaysmemory[counter],newweek[weekcount][12])
                        checkbuylist[counter]=checkday(buydaysmemory[counter],buylist[key][2])
                    else: #檢查前一個的週別是否一樣，一樣就不用再做判斷
                        if(weeklist[weeknumber]!=weeklist[weeknumber-1]):
                            buydaysmemory[counter]=KD(buylist[key][0],buylist[key][1],buydaysmemory[counter],newweek[weekcount][12])
                            checkbuylist[counter]=checkday(buydaysmemory[counter],buylist[key][2])
                if(key=='月RSI(6)'): #若為月RSI(6)判斷
                    if(weeknumber==0): #不用檢查前一個
                        buydaysmemory[counter]=KD(buylist[key][0],buylist[key][1],buydaysmemory[counter],newmonth[monthcount][12])
                        checkbuylist[counter]=checkday(buydaysmemory[counter],buylist[key][2])
                    else: #檢查前一個的週別是否一樣，一樣就不用再做判斷
                        if(monthlist[weeknumber]!=monthlist[weeknumber-1]):
                            buydaysmemory[counter]=KD(buylist[key][0],buylist[key][1],buydaysmemory[counter],newmonth[monthcount][12]) 
                            checkbuylist[counter]=checkday(buydaysmemory[counter],buylist[key][2])   
                if(key=='日RSI(9)'):   #若為日RSI(9)判斷
                    buydaysmemory[counter]=KD(buylist[key][0],buylist[key][1],buydaysmemory[counter],newday[i][13])
                    checkbuylist[counter]=checkday(buydaysmemory[counter],buylist[key][2])
                if(key=='週RSI(9)'):   #若為週RSI(9)判斷
                    if(weeknumber==0): #不用檢查前一個
                        buydaysmemory[counter]=KD(buylist[key][0],buylist[key][1],buydaysmemory[counter],newweek[weekcount][13])
                        checkbuylist[counter]=checkday(buydaysmemory[counter],buylist[key][2])
                    else: #檢查前一個的週別是否一樣，一樣就不用再做判斷
                        if(weeklist[weeknumber]!=weeklist[weeknumber-1]):
                            buydaysmemory[counter]=KD(buylist[key][0],buylist[key][1],buydaysmemory[counter],newweek[weekcount][13])
                            checkbuylist[counter]=checkday(buydaysmemory[counter],buylist[key][2])
                if(key=='月RSI(9)'): #若為月RSI(9)判斷
                    if(weeknumber==0): #不用檢查前一個
                        buydaysmemory[counter]=KD(buylist[key][0],buylist[key][1],buydaysmemory[counter],newmonth[monthcount][13])
                        checkbuylist[counter]=checkday(buydaysmemory[counter],buylist[key][2])
                    else: #檢查前一個的週別是否一樣，一樣就不用再做判斷
                        if(monthlist[weeknumber]!=monthlist[weeknumber-1]):
                            buydaysmemory[counter]=KD(buylist[key][0],buylist[key][1],buydaysmemory[counter],newmonth[monthcount][13])
                            checkbuylist[counter]=checkday(buydaysmemory[counter],buylist[key][2])
                if(key=='日RSI(12)'):   #若為日RSI(12)判斷
                    buydaysmemory[counter]=KD(buylist[key][0],buylist[key][1],buydaysmemory[counter],newday[i][14])
                    checkbuylist[counter]=checkday(buydaysmemory[counter],buylist[key][2])
                if(key=='週RSI(12)'):   #若為週RSI(12)判斷
                    if(weeknumber==0): #不用檢查前一個
                        buydaysmemory[counter]=KD(buylist[key][0],buylist[key][1],buydaysmemory[counter],newweek[weekcount][14])
                        checkbuylist[counter]=checkday(buydaysmemory[counter],buylist[key][2])
                    else: #檢查前一個的週別是否一樣，一樣就不用再做判斷
                        if(weeklist[weeknumber]!=weeklist[weeknumber-1]):
                            buydaysmemory[counter]=KD(buylist[key][0],buylist[key][1],buydaysmemory[counter],newweek[weekcount][14])
                            checkbuylist[counter]=checkday(buydaysmemory[counter],buylist[key][2])    
                if(key=='月RSI(12)'): #若為月RSI(12)判斷
                    if(weeknumber==0): #不用檢查前一個
                        buydaysmemory[counter]=KD(buylist[key][0],buylist[key][1],buydaysmemory[counter],newmonth[monthcount][14])
                        checkbuylist[counter]=checkday(buydaysmemory[counter],buylist[key][2])
                    else: #檢查前一個的週別是否一樣，一樣就不用再做判斷
                        if(monthlist[weeknumber]!=monthlist[weeknumber-1]):
                            buydaysmemory[counter]=KD(buylist[key][0],buylist[key][1],buydaysmemory[counter],newmonth[monthcount][14])
                            checkbuylist[counter]=checkday(buydaysmemory[counter],buylist[key][2])
                if(key=='日RSI'):   #日RSI交叉判斷
                    if(newday[i][12]==newday[i][14]): #交叉
                        buydaysmemory[counter]=GD(results,newday[i][1],newday[i][12],newday[i][14],12,14,buylist[key][0])
                        checkbuylist[counter]=checkother(buydaysmemory[counter])
                    else:
                        buydaysmemory[counter]=12
                        checkbuylist[counter]=checkother(buydaysmemory[counter])
                if(key=='週RSI'): #週RSI交叉判斷
                    if(weeknumber==0): #不用檢查前一個
                        if(newweek[weekcount][12]==newweek[weekcount][14]): #交叉
                            buydaysmemory[counter]=GD(weekresults,newweek[weekcount][1],newweek[weekcount][12],newweek[weekcount][14],12,14,buylist[key][0])
                            checkbuylist[counter]=checkother(buydaysmemory[counter])
                        else:
                            buydaysmemory[counter]=12
                            checkbuylist[counter]=checkother(buydaysmemory[counter])
                    else:
                        if(weeklist[weeknumber]!=weeklist[weeknumber-1]):  #檢查前一個的週別是否一樣，一樣就不用再做判斷
                            buydaysmemory[counter]=GD(weekresults,newweek[weekcount][1],newweek[weekcount][12],newweek[weekcount][14],12,14,buylist[key][0])
                            checkbuylist[counter]=checkother(buydaysmemory[counter])
                if(key=='月RSI'): #月RSI交叉判斷
                    if(weeknumber==0): #不用檢查前一個
                        if(newmonth[monthcount][12]==newmonth[monthcount][14]): #交叉
                            buydaysmemory[counter]=GD(monthresults,newmonth[monthcount][1],newmonth[monthcount][12],newmonth[monthcount][14],12,14,buylist[key][0])
                            checkbuylist[counter]=checkother(buydaysmemory[counter])
                        else:
                            buydaysmemory[counter]=12
                            checkbuylist[counter]=checkother(buydaysmemory[counter])
                    else:
                        if(monthlist[weeknumber]!=monthlist[weeknumber-1]):  #檢查前一個的週別是否一樣，一樣就不用再做判斷
                            buydaysmemory[counter]=GD(monthresults,newmonth[monthcount][1],newmonth[monthcount][12],newmonth[monthcount][14],12,14,buylist[key][0])
                            checkbuylist[counter]=checkother(buydaysmemory[counter])
                if(key=='均線價黃金交叉'): #均線價黃金交叉
                    if(buylist[key][0]=='日'):
                        buydaysmemory[counter]=VALUE(results,newday[i][1],newday[i][16],newday[i][18],newday[i][20],16,18,20,buylist[key][1],0)
                        checkbuylist[counter]=checkother(buydaysmemory[counter])
                    if(buylist[key][0]=='週'):
                        if(weeknumber==0): #不用檢查前一個
                            buydaysmemory[counter]=VALUE(weekresults,newweek[weekcount][1],newweek[weekcount][16],newweek[weekcount][18],newweek[weekcount][20],16,18,20,buylist[key][1],0)
                            checkbuylist[counter]=checkother(buydaysmemory[counter])
                        else:
                            if(weeklist[weeknumber]!=weeklist[weeknumber-1]):  #檢查前一個的週別是否一樣，一樣就不用再做判斷
                                buydaysmemory[counter]=VALUE(weekresults,newweek[weekcount][1],newweek[weekcount][16],newweek[weekcount][18],newweek[weekcount][20],16,18,20,buylist[key][1],0)
                                checkbuylist[counter]=checkother(buydaysmemory[counter])
                    if(buylist[key][0]=='月'):
                        if(weeknumber==0): #不用檢查前一個
                            buydaysmemory[counter]=VALUE(monthresults,newmonth[monthcount][1],newmonth[monthcount][16],newmonth[monthcount][18],newmonth[monthcount][20],16,18,20,buylist[key][1],0)
                            checkbuylist[counter]=checkother(buydaysmemory[counter])
                        else:
                            if(monthlist[weeknumber]!=monthlist[weeknumber-1]):  #檢查前一個的週別是否一樣，一樣就不用再做判斷
                                buydaysmemory[counter]=VALUE(weekresults,newmonth[monthcount][1],newmonth[monthcount][16],newmonth[monthcount][18],newmonth[monthcount][20],16,18,20,buylist[key][1],0)
                                checkbuylist[counter]=checkother(buydaysmemory[counter])
                if(key=='均線價死亡交叉'): #均線價死亡交叉
                    if(buylist[key][0]=='日'):
                        buydaysmemory[counter]=VALUE(results,newday[i][1],newday[i][16],newday[i][18],newday[i][20],16,18,20,buylist[key][1],1)
                        checkbuylist[counter]=checkother(buydaysmemory[counter])
                    if(buylist[key][0]=='週'):
                        if(weeknumber==0): #不用檢查前一個
                            buydaysmemory[counter]=VALUE(weekresults,newweek[weekcount][1],newweek[weekcount][16],newweek[weekcount][18],newweek[weekcount][20],16,18,20,buylist[key][1],1)
                            checkbuylist[counter]=checkother(buydaysmemory[counter])
                        else:
                            if(weeklist[weeknumber]!=weeklist[weeknumber-1]):  #檢查前一個的週別是否一樣，一樣就不用再做判斷
                                buydaysmemory[counter]=VALUE(weekresults,newweek[weekcount][1],newweek[weekcount][16],newweek[weekcount][18],newweek[weekcount][20],16,18,20,buylist[key][1],1)
                                checkbuylist[counter]=checkother(buydaysmemory[counter])
                    if(buylist[key][0]=='月'):
                        if(weeknumber==0): #不用檢查前一個
                            buydaysmemory[counter]=VALUE(monthresults,newmonth[monthcount][1],newmonth[monthcount][16],newmonth[monthcount][18],newmonth[monthcount][20],16,18,20,buylist[key][1],1)
                            checkbuylist[counter]=checkother(buydaysmemory[counter])   
                        else:
                            if(monthlist[weeknumber]!=monthlist[weeknumber-1]):  #檢查前一個的週別是否一樣，一樣就不用再做判斷
                                buydaysmemory[counter]=VALUE(weekresults,newmonth[monthcount][1],newmonth[monthcount][16],newmonth[monthcount][18],newmonth[monthcount][20],16,18,20,buylist[key][1],1)
                                checkbuylist[counter]=checkother(buydaysmemory[counter])
                if(key=='均量價黃金交叉'): #均量價黃金交叉
                    if(buylist[key][0]=='日'):
                        buydaysmemory[counter]=VALUE(results,newday[i][1],newday[i][17],newday[i][19],newday[i][21],17,19,21,buylist[key][1],0)
                        checkbuylist[counter]=checkother(buydaysmemory[counter])
                    if(buylist[key][0]=='週'):
                        if(weeknumber==0): #不用檢查前一個
                            buydaysmemory[counter]=VALUE(weekresults,newweek[weekcount][1],newweek[weekcount][17],newweek[weekcount][19],newweek[weekcount][21],17,19,21,buylist[key][1],0)
                            checkbuylist[counter]=checkother(buydaysmemory[counter])
                        else:
                            if(weeklist[weeknumber]!=weeklist[weeknumber-1]):  #檢查前一個的週別是否一樣，一樣就不用再做判斷
                                buydaysmemory[counter]=VALUE(weekresults,newweek[weekcount][1],newweek[weekcount][17],newweek[weekcount][19],newweek[weekcount][21],17,19,21,buylist[key][1],0)
                                checkbuylist[counter]=checkother(buydaysmemory[counter])
                    if(buylist[key][0]=='月'):
                        if(weeknumber==0): #不用檢查前一個
                            buydaysmemory[counter]=VALUE(monthresults,newmonth[monthcount][1],newmonth[monthcount][17],newmonth[monthcount][19],newmonth[monthcount][21],17,19,21,buylist[key][1],0)
                            checkbuylist[counter]=checkother(buydaysmemory[counter])   
                        else:
                            if(monthlist[weeknumber]!=monthlist[weeknumber-1]):  #檢查前一個的週別是否一樣，一樣就不用再做判斷
                                buydaysmemory[counter]=VALUE(weekresults,newmonth[monthcount][1],newmonth[monthcount][17],newmonth[monthcount][19],newmonth[monthcount][21],17,19,21,buylist[key][1],0)
                                checkbuylist[counter]=checkother(buydaysmemory[counter])
                if(key=='均量價死亡交叉'): #均量價死亡交叉
                    if(buylist[key][0]=='日'):
                        buydaysmemory[counter]=VALUE(results,newday[i][1],newday[i][17],newday[i][19],newday[i][21],17,19,21,buylist[key][1],1)
                        checkbuylist[counter]=checkother(buydaysmemory[counter])
                    if(buylist[key][0]=='週'):
                        if(weeknumber==0): #不用檢查前一個
                            buydaysmemory[counter]=VALUE(weekresults,newweek[weekcount][1],newweek[weekcount][17],newweek[weekcount][19],newweek[weekcount][21],17,19,21,buylist[key][1],1)
                            checkbuylist[counter]=checkother(buydaysmemory[counter])    
                        else:
                            if(weeklist[weeknumber]!=weeklist[weeknumber-1]):  #檢查前一個的週別是否一樣，一樣就不用再做判斷
                                buydaysmemory[counter]=VALUE(weekresults,newweek[weekcount][1],newweek[weekcount][17],newweek[weekcount][19],newweek[weekcount][21],17,19,21,buylist[key][1],1)
                                checkbuylist[counter]=checkother(buydaysmemory[counter])
                    if(buylist[key][0]=='月'):
                        if(weeknumber==0): #不用檢查前一個
                            buydaysmemory[counter]=VALUE(monthresults,newmonth[monthcount][1],newmonth[monthcount][17],newmonth[monthcount][19],newmonth[monthcount][21],17,19,21,buylist[key][1],1)
                            checkbuylist[counter]=checkother(buydaysmemory[counter])    
                        else:
                            if(monthlist[weeknumber]!=monthlist[weeknumber-1]):  #檢查前一個的週別是否一樣，一樣就不用再做判斷
                                buydaysmemory[counter]=VALUE(weekresults,newmonth[monthcount][1],newmonth[monthcount][17],newmonth[monthcount][19],newmonth[monthcount][21],17,19,21,buylist[key][1],1)
                                checkbuylist[counter]=checkother(buydaysmemory[counter])
                if(key=='賣壓比例'): #賣壓比例
                    if(buylist[key][0]=='日'):
                        buydaysmemory[counter]=check(buylist[key][1],buylist[key][2],buydaysmemory[counter],newday[i][24])
                        checkbuylist[counter]=checkother(buydaysmemory[counter])
                    if(buylist[key][0]=='週'):
                        if(weeknumber==0): #不用檢查前一個
                            buydaysmemory[counter]=check(buylist[key][1],buylist[key][2],buydaysmemory[counter],newweek[weekcount][24])
                            checkbuylist[counter]=checkother(buydaysmemory[counter])
                        else:
                            if(weeklist[weeknumber]!=weeklist[weeknumber-1]):  #檢查前一個的週別是否一樣，一樣就不用再做判斷
                                buydaysmemory[counter]=check(buylist[key][1],buylist[key][2],buydaysmemory[counter],newweek[weekcount][24])
                                checkbuylist[counter]=checkother(buydaysmemory[counter])
                    if(buylist[key][0]=='月'):
                        if(weeknumber==0): #不用檢查前一個
                            buydaysmemory[counter]=check(buylist[key][1],buylist[key][2],buydaysmemory[counter],newmonth[monthcount][24])
                            checkbuylist[counter]=checkother(buydaysmemory[counter])
                        else:
                            if(monthlist[weeknumber]!=monthlist[weeknumber-1]):  #檢查前一個的週別是否一樣，一樣就不用再做判斷
                                buydaysmemory[counter]=check(buylist[key][1],buylist[key][2],buydaysmemory[counter],newmonth[monthcount][24])
                                checkbuylist[counter]=checkother(buydaysmemory[counter])
                if(key=='MFI(14)'): #MFI(14)
                    if(buylist[key][0]=='日'):
                        buydaysmemory[counter]=check(buylist[key][1],buylist[key][2],buydaysmemory[counter],newday[i][23])
                        checkbuylist[counter]=checkother(buydaysmemory[counter])
                    if(buylist[key][0]=='週'):
                        if(weeknumber==0): #不用檢查前一個
                            buydaysmemory[counter]=check(buylist[key][1],buylist[key][2],buydaysmemory[counter],newweek[weekcount][23])
                            checkbuylist[counter]=checkother(buydaysmemory[counter])    
                        else:
                            if(weeklist[weeknumber]!=weeklist[weeknumber-1]):  #檢查前一個的週別是否一樣，一樣就不用再做判斷
                                buydaysmemory[counter]=check(buylist[key][1],buylist[key][2],buydaysmemory[counter],newweek[weekcount][23])
                                checkbuylist[counter]=checkother(buydaysmemory[counter])
                    if(buylist[key][0]=='月'):
                        if(weeknumber==0): #不用檢查前一個
                            buydaysmemory[counter]=check(buylist[key][1],buylist[key][2],buydaysmemory[counter],newmonth[monthcount][23])
                            checkbuylist[counter]=checkother(buydaysmemory[counter])   
                        else:
                            if(monthlist[weeknumber]!=monthlist[weeknumber-1]):  #檢查前一個的週別是否一樣，一樣就不用再做判斷
                                buydaysmemory[counter]=check(buylist[key][1],buylist[key][2],buydaysmemory[counter],newmonth[monthcount][23])
                                checkbuylist[counter]=checkother(buydaysmemory[counter])
                if(key=='波動率'): #波動率
                    if(buylist[key][0]=='日'):  
                        if(newday[i][25]!='#'):
                            number1=0.01*int(buylist[key][1])
                            number2=0.01*int(buylist[key][2])
                            if(float(newday[i][25])>number1 and float(newday[i][25])<number2):
                                buydaysmemory[counter]=11
                                checkbuylist[counter]=checkother(buydaysmemory[counter])
                            else:
                                buydaysmemory[counter]=12
                                checkbuylist[counter]=checkother(buydaysmemory[counter])
                        else:
                            buydaysmemory[counter]=12
                            checkbuylist[counter]=checkother(buydaysmemory[counter])
                    if(buylist[key][0]=='週'):
                        if(weeknumber==0): #不用檢查前一個  
                            if(newweek[weekcount][25]!='#'):
                                number1=0.01*int(buylist[key][1])
                                number2=0.01*int(buylist[key][2])
                                if(float(newweek[weekcount][25])>number1 and float(newweek[weekcount][25])<number2):
                                    buydaysmemory[counter]=11
                                    checkbuylist[counter]=checkother(buydaysmemory[counter])
                                else:
                                    buydaysmemory[counter]=12
                                    checkbuylist[counter]=checkother(buydaysmemory[counter])
                            else:
                                buydaysmemory[counter]=12
                                checkbuylist[counter]=checkother(buydaysmemory[counter])
                        else:
                            if(weeklist[weeknumber]!=weeklist[weeknumber-1]):  #檢查前一個的週別是否一樣，一樣就不用再做判斷
                                if(newweek[weekcount][25]!='#'):
                                    number1=0.01*int(buylist[key][1])
                                    number2=0.01*int(buylist[key][2])
                                    if(float(newweek[weekcount][25])>number1 and float(newweek[weekcount][25])<number2):
                                        buydaysmemory[counter]=11  
                                        checkbuylist[counter]=checkother(buydaysmemory[counter])
                                    else:
                                        buydaysmemory[counter]=12  
                                        checkbuylist[counter]=checkother(buydaysmemory[counter])
                                else:
                                    buydaysmemory[counter]=12
                                    checkbuylist[counter]=checkother(buydaysmemory[counter])
                    if(buylist[key][0]=='月'):
                        if(weeknumber==0): #不用檢查前一個  
                            if(newmonth[monthcount][25]!='#'):
                                number1=0.01*int(buylist[key][1])
                                number2=0.01*int(buylist[key][2])
                                if(float(newmonth[monthcount][25])>number1 and float(newmonth[monthcount][25])<number2):
                                    buydaysmemory[counter]=11
                                    checkbuylist[counter]=checkother(buydaysmemory[counter])
                                else:
                                    buydaysmemory[counter]=12
                                    checkbuylist[counter]=checkother(buydaysmemory[counter])
                            else:
                                buydaysmemory[counter]=12
                                checkbuylist[counter]=checkother(buydaysmemory[counter])
                        else:
                            if(monthlist[weeknumber]!=monthlist[weeknumber-1]):  #檢查前一個的週別是否一樣，一樣就不用再做判斷
                                if(newmonth[monthcount][25]!='#'):
                                    number1=0.01*int(buylist[key][1])
                                    number2=0.01*int(buylist[key][2])
                                    if(float(newmonth[monthcount][25])>number1 and float(newmonth[monthcount][25])<number2):
                                        buydaysmemory[counter]=11 
                                        checkbuylist[counter]=checkother(buydaysmemory[counter])
                                    else:
                                        buydaysmemory[counter]=12 
                                        checkbuylist[counter]=checkother(buydaysmemory[counter]) 
                                else:
                                    buydaysmemory[counter]=12
                                    checkbuylist[counter]=checkother(buydaysmemory[counter])
                if(key=='日成交量'): #日成交量
                    if(newday[i][2]!='#'):
                        buydaysmemory[counter]=VOLUME(results,newday[i][1],2,newday[i][2],buydaysmemory[counter],buylist[key][1])
                        checkbuylist[counter]=checkday(buydaysmemory[counter],buylist[key][0])
                    else:
                        buydaysmemory[counter]=0
                        checkbuylist[counter]=checkday(buydaysmemory[counter],buylist[key][0])
                if(key=='週成交量'): #週成交量
                    if(weeknumber==0): #不用檢查前一個
                        buydaysmemory[counter]=VOLUME(weekresults,newweek[weekcount][1],2,newweek[weekcount][2],buydaysmemory[counter],buylist[key][1])
                        checkbuylist[counter]=checkday(buydaysmemory[counter],buylist[key][0])
                    else:
                        if(weeklist[weeknumber]!=weeklist[weeknumber-1]):
                            buydaysmemory[counter]=VOLUME(weekresults,newweek[weekcount][1],2,newweek[weekcount][2],buydaysmemory[counter],buylist[key][1])
                            checkbuylist[counter]=checkday(buydaysmemory[counter],buylist[key][0])
                if(key=='月成交量'): #月成交量
                    if(weeknumber==0): #不用檢查前一個
                        buydaysmemory[counter]=VOLUME(monthresults,newmonth[monthcount][1],2,newmonth[monthcount][2],buydaysmemory[counter],buylist[key][1])
                        checkbuylist[counter]=checkday(buydaysmemory[counter],buylist[key][0])
                    else:
                        if(monthlist[weeknumber]!=monthlist[weeknumber-1]):
                            buydaysmemory[counter]=VOLUME(monthresults,newmonth[monthcount][1],2,newmonth[monthcount][2],buydaysmemory[counter],buylist[key][1])
                            checkbuylist[counter]=checkday(buydaysmemory[counter],buylist[key][0])
                if(key=='三大法人'): #三大法人
                    buydaysmemory[counter]=other(buylist[key][0],buydaysmemory[counter],newthree[i][7])
                    checkbuylist[counter]=checkday(buydaysmemory[counter],buylist[key][1])
                if(key=='外資'): #外資
                    buydaysmemory[counter]=other(buylist[key][0],buydaysmemory[counter],str(float(newthree[i][2])+float(newthree[i][3])))
                    checkbuylist[counter]=checkday(buydaysmemory[counter],buylist[key][1])
                if(key=='投信'): #投信
                    buydaysmemory[counter]=other(buylist[key][0],buydaysmemory[counter],newthree[i][4])
                    checkbuylist[counter]=checkday(buydaysmemory[counter],buylist[key][1])
                if(key=='自營商'): #自營商
                    buydaysmemory[counter]=other(buylist[key][0],buydaysmemory[counter],str(float(newthree[i][5])+float(newthree[i][6])))
                    checkbuylist[counter]=checkday(buydaysmemory[counter],buylist[key][1])
                if(key=='券資比'): #券資比
                    buydaysmemory[counter]=VOLUME(chan,newday[i][1],14,newchan[i][14],buydaysmemory[counter],buylist[key][0])
                    checkbuylist[counter]=checkday(buydaysmemory[counter],buylist[key][1])
                if(key=='融資'): #融資
                    buydaysmemory[counter]=VOLUME(chan,newday[i][1],6,newchan[i][6],buydaysmemory[counter],buylist[key][0])
                    checkbuylist[counter]=checkday(buydaysmemory[counter],buylist[key][1])
                if(key=='融券'): #融券
                    buydaysmemory[counter]=VOLUME(chan,newday[i][1],13,newchan[i][13],buydaysmemory[counter],buylist[key][0])
                    checkbuylist[counter]=checkday(buydaysmemory[counter],buylist[key][1])
                if(key=='通道股價'): #通道股價
                    buydaysmemory[counter]=boolean(buylist[key][0],newday[i][1],results,newday[i][17],buylist[key][1],0)
                    checkbuylist[counter]=checkother(buydaysmemory[counter])    
                if(key=='通道開口'): #通道開口
                    buydaysmemory[counter]=boolean(buylist[key][0],newday[i][1],results,newday[i][17],buylist[key][1],buydaysmemory[counter])
                    checkbuylist[counter]=checkday(buydaysmemory[counter],buylist[key][1])
            for x in range(len(checkbuylist)):
                if(checkbuylist[x]=='NO'): #一個條件不行全部重判斷
                    totalday[2].append(newday[i][1])
                    break
                elif(x==(len(checkbuylist)-1) and checkbuylist[x]=='YES'): #最後一個也為YES代表可以買
                    count=1
                    totalday[0].append(newday[i][1]) #記錄買的日期
                    counter=-1
                    money.append(newday[i][7])
                    #清空紀錄欄
                    buydaysmemory=[0 for i in range(len(buylist))]
                    checkbuylist=['' for i in range(len(buylist))]
        elif(count==1): #只需關心賣出條件
            for key in selllist:
                counter+=1
                if(key=='日K'): #若為日K判斷
                    selldaysmemory[counter]=KD(selllist[key][0],selllist[key][1],selldaysmemory[counter],newday[i][10])
                    checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][2])
                if(key=='週K'): #若為週K判斷
                    if(weeknumber==0): #不用檢查前一個
                        selldaysmemory[counter]=KD(selllist[key][0],selllist[key][1],selldaysmemory[counter],newweek[weekcount][10])
                        checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][2])
                    else: #檢查前一個的週別是否一樣，一樣就不用再做判斷
                        if(weeklist[weeknumber]!=weeklist[weeknumber-1]):
                            selldaysmemory[counter]=KD(selllist[key][0],selllist[key][1],selldaysmemory[counter],newweek[weekcount][10])
                            checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][2])
                if(key=='月K'): #若為月K判斷
                    if(weeknumber==0): #不用檢查前一個
                        selldaysmemory[counter]=KD(selllist[key][0],selllist[key][1],selldaysmemory[counter],newmonth[monthcount][10])
                        checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][2])
                    else: #檢查前一個的週別是否一樣，一樣就不用再做判斷
                        if(monthlist[weeknumber]!=monthlist[weeknumber-1]):
                            selldaysmemory[counter]=KD(selllist[key][0],selllist[key][1],selldaysmemory[counter],newmonth[monthcount][10])
                            checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][2])
                if(key=='日D'): #若為日D判斷
                    selldaysmemory[counter]=KD(selllist[key][0],selllist[key][1],selldaysmemory[counter],newday[i][11])
                    checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][2])
                if(key=='週D'): #若為週D判斷
                    if(weeknumber==0): #不用檢查前一個
                        selldaysmemory[counter]=KD(selllist[key][0],selllist[key][1],selldaysmemory[counter],newweek[weekcount][11])
                        checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][2])
                    else: #檢查前一個的週別是否一樣，一樣就不用再做判斷
                        if(weeklist[weeknumber]!=weeklist[weeknumber-1]): #週別不一樣再做就好，否則不變
                            selldaysmemory[counter]=KD(selllist[key][0],selllist[key][1],selldaysmemory[counter],newweek[weekcount][11])
                            checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][2])
                if(key=='月D'): #若為月D判斷
                    if(weeknumber==0): #不用檢查前一個
                        selldaysmemory[counter]=KD(selllist[key][0],selllist[key][1],selldaysmemory[counter],newmonth[monthcount][11])
                        checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][2])
                    else: #檢查前一個的週別是否一樣，一樣就不用再做判斷
                        if(monthlist[weeknumber]!=monthlist[weeknumber-1]):
                            selldaysmemory[counter]=KD(selllist[key][0],selllist[key][1],selldaysmemory[counter],newmonth[monthcount][11])
                            checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][2])
                if(key=='日KD'): #若為黃金或死亡交叉
                    if(newday[i][10]==newday[i][11]): #交叉
                        selldaysmemory[counter]=GD(results,newday[i][1],newday[i][10],newday[i][11],10,11,selllist[key][0])
                        checkselllist[counter]=checkother(selldaysmemory[counter])
                    else:
                        selldaysmemory[counter]=12
                        checkselllist[counter]=checkother(selldaysmemory[counter])
                if(key=='週KD'): #若為黃金或死亡交叉
                    if(weeknumber==0): #不用檢查前一個
                        if(newweek[weekcount][10]==newweek[weekcount][11]): #交叉
                            selldaysmemory[counter]=GD(weekresults,newweek[weekcount][1],newweek[weekcount][10],newweek[weekcount][11],10,11,selllist[key][0])
                            checkselllist[counter]=checkother(selldaysmemory[counter])
                        else:
                            selldaysmemory[counter]=12
                            checkselllist[counter]=checkother(selldaysmemory[counter])
                    else:
                        if(weeklist[weeknumber]!=weeklist[weeknumber-1]):  #檢查前一個的週別是否一樣，一樣就不用再做判斷
                            selldaysmemory[counter]=GD(weekresults,newweek[weekcount][1],newweek[weekcount][10],newweek[weekcount][11],10,11,selllist[key][0])
                            checkselllist[counter]=checkother(selldaysmemory[counter])
                if(key=='月KD'): #若為黃金或死亡交叉
                    if(weeknumber==0): #不用檢查前一個
                        if(newmonth[monthcount][10]==newmonth[monthcount][11]): #交叉
                            selldaysmemory[counter]=GD(monthresults,newmonth[monthcount][1],newmonth[monthcount][10],newmonth[monthcount][11],10,11,selllist[key][0])
                            checkselllist[counter]=checkother(selldaysmemory[counter])
                        else:
                            selldaysmemory[counter]=12
                            checkselllist[counter]=checkother(selldaysmemory[counter])
                    else:
                        if(monthlist[weeknumber]!=monthlist[weeknumber-1]):  #檢查前一個的週別是否一樣，一樣就不用再做判斷
                            selldaysmemory[counter]=GD(monthresults,newmonth[monthcount][1],newmonth[monthcount][10],newmonth[monthcount][11],10,11,selllist[key][0])
                            checkselllist[counter]=checkother(selldaysmemory[counter])
                if(key=='日MACD'): #若為日MACD判斷
                    selldaysmemory[counter]=KD(selllist[key][0],selllist[key][1],selldaysmemory[counter],newday[i][15])
                    checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][2])
                if(key=='週MACD'): #若為週MACD判斷
                    if(weeknumber==0): #不用檢查前一個
                        selldaysmemory[counter]=KD(selllist[key][0],selllist[key][1],selldaysmemory[counter],newweek[weekcount][15])
                        checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][2])
                    else: #檢查前一個的週別是否一樣，一樣就不用再做判斷
                        if(weeklist[weeknumber]!=weeklist[weeknumber-1]):
                            selldaysmemory[counter]=KD(selllist[key][0],selllist[key][1],selldaysmemory[counter],newweek[weekcount][15])
                            checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][2])
                if(key=='月MACD'): #若為月MACD判斷
                    if(weeknumber==0): #不用檢查前一個
                        selldaysmemory[counter]=KD(selllist[key][0],selllist[key][1],selldaysmemory[counter],newmonth[monthcount][15])
                        checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][2])
                    else: #檢查前一個的週別是否一樣，一樣就不用再做判斷
                        if(monthlist[weeknumber]!=monthlist[weeknumber-1]):
                            selldaysmemory[counter]=KD(selllist[key][0],selllist[key][1],selldaysmemory[counter],newmonth[monthcount][15])                    
                            checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][2])
                if(key=='日DIF'): #若為日DIF判斷
                    selldaysmemory[counter]=KD(selllist[key][0],selllist[key][1],selldaysmemory[counter],newday[i][22])
                    checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][2])
                if(key=='週DIF'): #若為週DIF判斷
                    if(weeknumber==0): #不用檢查前一個
                        selldaysmemory[counter]=KD(selllist[key][0],selllist[key][1],selldaysmemory[counter],newweek[weekcount][22])
                        checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][2])
                    else: #檢查前一個的週別是否一樣，一樣就不用再做判斷
                        if(weeklist[weeknumber]!=weeklist[weeknumber-1]):
                            selldaysmemory[counter]=KD(selllist[key][0],selllist[key][1],selldaysmemory[counter],newweek[weekcount][22])
                            checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][2])
                if(key=='月DIF'): #若為月DIF判斷
                    if(weeknumber==0): #不用檢查前一個
                        selldaysmemory[counter]=KD(selllist[key][0],selllist[key][1],selldaysmemory[counter],newmonth[monthcount][22])
                        checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][2])
                    else: #檢查前一個的週別是否一樣，一樣就不用再做判斷
                        if(monthlist[weeknumber]!=monthlist[weeknumber-1]):
                            selldaysmemory[counter]=KD(selllist[key][0],selllist[key][1],selldaysmemory[counter],newmonth[monthcount][22])
                            checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][2])
                if(key=='日MACD落點'): #日MACD落點判斷
                    selldaysmemory[counter]=Place(selllist[key][0],newday[i][15],newday[i][22])
                    checkselllist[counter]=checkother(selldaysmemory[counter])
                if(key=='週MACD落點'): #週MACD落點判斷
                    if(weeknumber==0):
                        selldaysmemory[counter]=Place(selllist[key][0],newweek[weekcount][15],newweek[weekcount][22])
                        checkselllist[counter]=checkother(selldaysmemory[counter])
                    else:
                        if(weeklist[weeknumber]!=weeklist[weeknumber-1]):
                            selldaysmemory[counter]=Place(selllist[key][0],newweek[weekcount][15],newweek[weekcount][22]) 
                            checkselllist[counter]=checkother(selldaysmemory[counter])
                if(key=='月MACD落點'): #月MACD落點判斷
                    if(weeknumber==0):
                        selldaysmemory[counter]=Place(selllist[key][0],newmonth[monthcount][15],newmonth[monthcount][22])
                        checkselllist[counter]=checkother(selldaysmemory[counter])
                    else:
                        if(monthlist[weeknumber]!=monthlist[weeknumber-1]):
                            selldaysmemory[counter]=Place(selllist[key][0],newmonth[monthcount][15],newmonth[monthcount][22]) 
                            checkselllist[counter]=checkother(selldaysmemory[counter])
                if(key=='日MACD，日DIF'): #日MACD、DIF交叉判斷
                    if(newday[i][15]==newday[i][22]): #交叉
                        selldaysmemory[counter]=GD(results,newday[i][1],newday[i][22],newday[i][15],22,15,selllist[key][0])
                        checkselllist[counter]=checkother(selldaysmemory[counter])
                    else:
                        selldaysmemory[counter]=0
                        checkselllist[counter]=checkother(selldaysmemory[counter])
                if(key=='週MACD，週DIF'): #週MACD、DIF交叉判斷
                    if(weeknumber==0): #不用檢查前一個
                        if(newweek[weekcount][15]==newweek[weekcount][22]): #交叉
                            selldaysmemory[counter]=GD(weekresults,newweek[weekcount][1],newweek[weekcount][22],newweek[weekcount][15],22,15,selllist[key][0])
                            checkselllist[counter]=checkother(selldaysmemory[counter])
                        else:
                            selldaysmemory[counter]=12
                            checkselllist[counter]=checkother(selldaysmemory[counter])
                    else:
                        if(weeklist[weeknumber]!=weeklist[weeknumber-1]):  #檢查前一個的週別是否一樣，一樣就不用再做判斷
                            selldaysmemory[counter]=GD(weekresults,newweek[weekcount][1],newweek[weekcount][22],newweek[weekcount][15],22,15,selllist[key][0])
                            checkselllist[counter]=checkother(selldaysmemory[counter])
                if(key=='月MACD，月DIF'): #月MACD、DIF交叉判斷
                    if(weeknumber==0): #不用檢查前一個
                        if(newmonth[monthcount][15]==newmonth[monthcount][22]): #交叉
                            selldaysmemory[counter]=GD(monthresults,newmonth[monthcount][1],newmonth[monthcount][22],newmonth[monthcount][15],22,15,selllist[key][0])
                            checkselllist[counter]=checkother(selldaysmemory[counter])
                        else:
                            selldaysmemory[counter]=12
                            checkselllist[counter]=checkother(selldaysmemory[counter])
                    else:
                        if(monthlist[weeknumber]!=monthlist[weeknumber-1]):  #檢查前一個的週別是否一樣，一樣就不用再做判斷
                            selldaysmemory[counter]=GD(monthresults,newmonth[monthcount][1],newmonth[monthcount][22],newmonth[monthcount][15],22,15,selllist[key][0])
                            checkselllist[counter]=checkother(selldaysmemory[counter])
                if(key=='日RSI(6)'):   #若為日RSI(6)判斷
                    selldaysmemory[counter]=KD(selllist[key][0],selllist[key][1],selldaysmemory[counter],newday[i][12])
                    checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][2])
                if(key=='週RSI(6)'):   #若為週RSI(6)判斷
                    if(weeknumber==0): #不用檢查前一個
                        selldaysmemory[counter]=KD(selllist[key][0],selllist[key][1],selldaysmemory[counter],newweek[weekcount][12])
                        checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][2])
                    else: #檢查前一個的週別是否一樣，一樣就不用再做判斷
                        if(weeklist[weeknumber]!=weeklist[weeknumber-1]):
                            selldaysmemory[counter]=KD(selllist[key][0],selllist[key][1],selldaysmemory[counter],newweek[weekcount][12])
                            checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][2])
                if(key=='月RSI(6)'): #若為月RSI(6)判斷
                    if(weeknumber==0): #不用檢查前一個
                        selldaysmemory[counter]=KD(selllist[key][0],selllist[key][1],selldaysmemory[counter],newmonth[monthcount][12])
                        checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][2])
                    else: #檢查前一個的週別是否一樣，一樣就不用再做判斷
                        if(monthlist[weeknumber]!=monthlist[weeknumber-1]):
                            selldaysmemory[counter]=KD(selllist[key][0],selllist[key][1],selldaysmemory[counter],newmonth[monthcount][12])    
                            checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][2])
                if(key=='日RSI(9)'):   #若為日RSI(9)判斷
                    selldaysmemory[counter]=KD(selllist[key][0],selllist[key][1],selldaysmemory[counter],newday[i][13])
                    checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][2])
                if(key=='週RSI(9)'):   #若為週RSI(9)判斷
                    if(weeknumber==0): #不用檢查前一個
                        selldaysmemory[counter]=KD(selllist[key][0],selllist[key][1],selldaysmemory[counter],newweek[weekcount][13])
                        checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][2])
                    else: #檢查前一個的週別是否一樣，一樣就不用再做判斷
                        if(weeklist[weeknumber]!=weeklist[weeknumber-1]):
                            selldaysmemory[counter]=KD(selllist[key][0],selllist[key][1],selldaysmemory[counter],newweek[weekcount][13])
                            checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][2])
                if(key=='月RSI(9)'): #若為月RSI(9)判斷
                    if(weeknumber==0): #不用檢查前一個
                        selldaysmemory[counter]=KD(selllist[key][0],selllist[key][1],selldaysmemory[counter],newmonth[monthcount][13])
                        checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][2])
                    else: #檢查前一個的週別是否一樣，一樣就不用再做判斷
                        if(monthlist[weeknumber]!=monthlist[weeknumber-1]):
                            selldaysmemory[counter]=KD(selllist[key][0],selllist[key][1],selldaysmemory[counter],newmonth[monthcount][13])    
                            checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][2])
                if(key=='日RSI(12)'):   #若為日RSI(12)判斷
                    selldaysmemory[counter]=KD(selllist[key][0],selllist[key][1],selldaysmemory[counter],newday[i][14])
                    checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][2])
                if(key=='週RSI(12)'):   #若為週RSI(12)判斷
                    if(weeknumber==0): #不用檢查前一個
                        selldaysmemory[counter]=KD(selllist[key][0],selllist[key][1],selldaysmemory[counter],newweek[weekcount][14])
                        checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][2])
                    else: #檢查前一個的週別是否一樣，一樣就不用再做判斷
                        if(weeklist[weeknumber]!=weeklist[weeknumber-1]):
                            selldaysmemory[counter]=KD(selllist[key][0],selllist[key][1],selldaysmemory[counter],newweek[weekcount][14])
                            checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][2])
                if(key=='月RSI(12)'): #若為月RSI(12)判斷
                    if(weeknumber==0): #不用檢查前一個
                        selldaysmemory[counter]=KD(selllist[key][0],selllist[key][1],selldaysmemory[counter],newmonth[monthcount][14])
                        checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][2])
                    else: #檢查前一個的週別是否一樣，一樣就不用再做判斷
                        if(monthlist[weeknumber]!=monthlist[weeknumber-1]):
                            selldaysmemory[counter]=KD(selllist[key][0],selllist[key][1],selldaysmemory[counter],newmonth[monthcount][14])    
                            checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][2])
                if(key=='日RSI'):   #日RSI交叉判斷
                    if(newday[i][12]==newday[i][14]): #交叉
                        selldaysmemory[counter]=GD(results,newday[i][1],newday[i][12],newday[i][14],12,14,selllist[key][0])
                        checkselllist[counter]=checkother(selldaysmemory[counter])
                    else:
                        selldaysmemory[counter]=12
                        checkselllist[counter]=checkother(selldaysmemory[counter])
                if(key=='週RSI'): #週RSI交叉判斷
                    if(weeknumber==0): #不用檢查前一個
                        if(newweek[weekcount][12]==newweek[weekcount][14]): #交叉
                            selldaysmemory[counter]=GD(weekresults,newweek[weekcount][1],newweek[weekcount][12],newweek[weekcount][14],12,14,selllist[key][0])
                            checkselllist[counter]=checkother(selldaysmemory[counter])
                        else:
                            selldaysmemory[counter]=12
                            checkselllist[counter]=checkother(selldaysmemory[counter])
                    else:
                        if(weeklist[weeknumber]!=weeklist[weeknumber-1]):  #檢查前一個的週別是否一樣，一樣就不用再做判斷
                            selldaysmemory[counter]=GD(weekresults,newweek[weekcount][1],newweek[weekcount][12],newweek[weekcount][14],12,14,selllist[key][0])
                            checkselllist[counter]=checkother(selldaysmemory[counter])
                if(key=='月RSI'): #月RSI交叉判斷
                    if(weeknumber==0): #不用檢查前一個
                        if(newmonth[monthcount][12]==newmonth[monthcount][14]): #交叉
                            selldaysmemory[counter]=GD(monthresults,newmonth[monthcount][1],newmonth[monthcount][12],newmonth[monthcount][14],12,14,selllist[key][0])
                            checkselllist[counter]=checkother(selldaysmemory[counter])
                        else:
                            selldaysmemory[counter]=12
                            checkselllist[counter]=checkother(selldaysmemory[counter])
                    else:
                        if(monthlist[weeknumber]!=monthlist[weeknumber-1]):  #檢查前一個的週別是否一樣，一樣就不用再做判斷
                            selldaysmemory[counter]=GD(monthresults,newmonth[monthcount][1],newmonth[monthcount][12],newmonth[monthcount][14],12,14,selllist[key][0])
                            checkselllist[counter]=checkother(selldaysmemory[counter])
                if(key=='均線價黃金交叉'): #均線價黃金交叉
                    if(selllist[key][0]=='日'):
                        selldaysmemory[counter]=VALUE(results,newday[i][1],newday[i][16],newday[i][18],newday[i][20],16,18,20,selllist[key][1],0)
                        checkselllist[counter]=checkother(selldaysmemory[counter])
                    if(selllist[key][0]=='週'):
                        if(weeknumber==0): #不用檢查前一個
                            selldaysmemory[counter]=VALUE(weekresults,newweek[weekcount][1],newweek[weekcount][16],newweek[weekcount][18],newweek[weekcount][20],16,18,20,selllist[key][1],0)
                            checkselllist[counter]=checkother(selldaysmemory[counter])
                        else:
                            if(weeklist[weeknumber]!=weeklist[weeknumber-1]):  #檢查前一個的週別是否一樣，一樣就不用再做判斷
                                selldaysmemory[counter]=VALUE(weekresults,newweek[weekcount][1],newweek[weekcount][16],newweek[weekcount][18],newweek[weekcount][20],16,18,20,selllist[key][1],0)
                                checkselllist[counter]=checkother(selldaysmemory[counter])
                    if(selllist[key][0]=='月'):
                        if(weeknumber==0): #不用檢查前一個
                            selldaysmemory[counter]=VALUE(monthresults,newmonth[monthcount][1],newmonth[monthcount][16],newmonth[monthcount][18],newmonth[monthcount][20],16,18,20,selllist[key][1],0)
                            checkselllist[counter]=checkother(selldaysmemory[counter])
                        else:
                            if(monthlist[weeknumber]!=monthlist[weeknumber-1]):  #檢查前一個的週別是否一樣，一樣就不用再做判斷
                                selldaysmemory[counter]=VALUE(monthresults,newmonth[monthcount][1],newmonth[monthcount][16],newmonth[monthcount][18],newmonth[monthcount][20],16,18,20,selllist[key][1],0)
                                checkselllist[counter]=checkother(selldaysmemory[counter])
                if(key=='均線價死亡交叉'): #均線價死亡交叉
                    if(selllist[key][0]=='日'):
                        selldaysmemory[counter]=VALUE(results,newday[i][1],newday[i][16],newday[i][18],newday[i][20],16,18,20,selllist[key][1],1)
                        checkselllist[counter]=checkother(selldaysmemory[counter])
                    if(selllist[key][0]=='週'):
                        if(weeknumber==0): #不用檢查前一個
                            selldaysmemory[counter]=VALUE(weekresults,newweek[weekcount][1],newweek[weekcount][16],newweek[weekcount][18],newweek[weekcount][20],16,18,20,selllist[key][1],1)
                            checkselllist[counter]=checkother(selldaysmemory[counter])
                        else:
                            if(weeklist[weeknumber]!=weeklist[weeknumber-1]):  #檢查前一個的週別是否一樣，一樣就不用再做判斷
                                selldaysmemory[counter]=VALUE(weekresults,newweek[weekcount][1],newweek[weekcount][16],newweek[weekcount][18],newweek[weekcount][20],16,18,20,selllist[key][1],1)
                                checkselllist[counter]=checkother(selldaysmemory[counter])
                    if(selllist[key][0]=='月'):
                        if(weeknumber==0): #不用檢查前一個
                            selldaysmemory[counter]=VALUE(monthresults,newmonth[monthcount][1],newmonth[monthcount][16],newmonth[monthcount][18],newmonth[monthcount][20],16,18,20,selllist[key][1],1)
                            checkselllist[counter]=checkother(selldaysmemory[counter])
                        else:
                            if(monthlist[weeknumber]!=monthlist[weeknumber-1]):  #檢查前一個的週別是否一樣，一樣就不用再做判斷
                                selldaysmemory[counter]=VALUE(monthresults,newmonth[monthcount][1],newmonth[monthcount][16],newmonth[monthcount][18],newmonth[monthcount][20],16,18,20,selllist[key][1],1)
                                checkselllist[counter]=checkother(selldaysmemory[counter])
                if(key=='均量價黃金交叉'): #均量價黃金交叉
                    if(selllist[key][0]=='日'):
                        selldaysmemory[counter]=VALUE(results,newday[i][1],newday[i][17],newday[i][19],newday[i][21],17,19,21,selllist[key][1],0)
                        checkselllist[counter]=checkother(selldaysmemory[counter])
                    if(selllist[key][0]=='週'):
                        if(weeknumber==0): #不用檢查前一個
                            selldaysmemory[counter]=VALUE(weekresults,newweek[weekcount][1],newweek[weekcount][17],newweek[weekcount][19],newweek[weekcount][21],17,19,21,selllist[key][1],0)
                            checkselllist[counter]=checkother(selldaysmemory[counter])    
                        else:
                            if(weeklist[weeknumber]!=weeklist[weeknumber-1]):  #檢查前一個的週別是否一樣，一樣就不用再做判斷
                                selldaysmemory[counter]=VALUE(weekresults,newweek[weekcount][1],newweek[weekcount][17],newweek[weekcount][19],newweek[weekcount][21],17,19,21,selllist[key][1],0)
                                checkselllist[counter]=checkother(selldaysmemory[counter])
                    if(selllist[key][0]=='月'):
                        if(weeknumber==0): #不用檢查前一個
                            selldaysmemory[counter]=VALUE(monthresults,newmonth[monthcount][1],newmonth[monthcount][17],newmonth[monthcount][19],newmonth[monthcount][21],17,19,21,selllist[key][1],0)
                            checkselllist[counter]=checkother(selldaysmemory[counter])    
                        else:
                            if(monthlist[weeknumber]!=monthlist[weeknumber-1]):  #檢查前一個的週別是否一樣，一樣就不用再做判斷
                                selldaysmemory[counter]=VALUE(monthresults,newmonth[monthcount][1],newmonth[monthcount][17],newmonth[monthcount][19],newmonth[monthcount][21],17,19,21,selllist[key][1],0)
                                checkselllist[counter]=checkother(selldaysmemory[counter])
                if(key=='均量價死亡交叉'): #均量價死亡交叉
                    if(selllist[key][0]=='日'):
                        selldaysmemory[counter]=VALUE(results,newday[i][1],newday[i][17],newday[i][19],newday[i][21],17,19,21,selllist[key][1],1)
                        checkselllist[counter]=checkother(selldaysmemory[counter])
                    if(selllist[key][0]=='週'):
                        if(weeknumber==0): #不用檢查前一個
                            selldaysmemory[counter]=VALUE(weekresults,newweek[weekcount][1],newweek[weekcount][17],newweek[weekcount][19],newweek[weekcount][21],17,19,21,selllist[key][1],1)
                            checkselllist[counter]=checkother(selldaysmemory[counter])    
                        else:
                            if(weeklist[weeknumber]!=weeklist[weeknumber-1]):  #檢查前一個的週別是否一樣，一樣就不用再做判斷
                                selldaysmemory[counter]=VALUE(weekresults,newweek[weekcount][1],newweek[weekcount][17],newweek[weekcount][19],newweek[weekcount][21],17,19,21,selllist[key][1],1)
                                checkselllist[counter]=checkother(selldaysmemory[counter])
                    if(selllist[key][0]=='月'):
                        if(weeknumber==0): #不用檢查前一個
                            selldaysmemory[counter]=VALUE(monthresults,newmonth[monthcount][1],newmonth[monthcount][17],newmonth[monthcount][19],newmonth[monthcount][21],17,19,21,selllist[key][1],1)
                            checkselllist[counter]=checkother(selldaysmemory[counter])    
                        else:
                            if(monthlist[weeknumber]!=monthlist[weeknumber-1]):  #檢查前一個的週別是否一樣，一樣就不用再做判斷
                                selldaysmemory[counter]=VALUE(monthresults,newmonth[monthcount][1],newmonth[monthcount][17],newmonth[monthcount][19],newmonth[monthcount][21],17,19,21,selllist[key][1],1)
                                checkselllist[counter]=checkother(selldaysmemory[counter])
                if(key=='賣壓比例'): #賣壓比例
                    if(selllist[key][0]=='日'):
                        selldaysmemory[counter]=check(selllist[key][1],selllist[key][2],selldaysmemory[counter],newday[i][24])
                        checkselllist[counter]=checkother(selldaysmemory[counter])
                    if(selllist[key][0]=='週'):
                        if(weeknumber==0): #不用檢查前一個
                            selldaysmemory[counter]=check(selllist[key][1],selllist[key][2],selldaysmemory[counter],newweek[weekcount][24])
                            checkselllist[counter]=checkother(selldaysmemory[counter])
                        else:
                            if(weeklist[weeknumber]!=weeklist[weeknumber-1]):  #檢查前一個的週別是否一樣，一樣就不用再做判斷
                                selldaysmemory[counter]=check(selllist[key][1],selllist[key][2],selldaysmemory[counter],newweek[weekcount][24])
                                checkselllist[counter]=checkother(selldaysmemory[counter])
                    if(selllist[key][0]=='月'):
                        if(weeknumber==0): #不用檢查前一個
                            selldaysmemory[counter]=check(selllist[key][1],selllist[key][2],selldaysmemory[counter],newmonth[monthcount][24])
                            checkselllist[counter]=checkother(selldaysmemory[counter])
                        else:
                            if(monthlist[weeknumber]!=monthlist[weeknumber-1]):  #檢查前一個的週別是否一樣，一樣就不用再做判斷
                                selldaysmemory[counter]=check(selllist[key][1],selllist[key][2],selldaysmemory[counter],newmonth[monthcount][24])
                                checkselllist[counter]=checkother(selldaysmemory[counter])
                if(key=='MFI(14)'): #MFI(14)
                    if(selllist[key][0]=='日'):
                        selldaysmemory[counter]=check(selllist[key][1],selllist[key][2],selldaysmemory[counter],newday[i][23])
                        checkselllist[counter]=checkother(selldaysmemory[counter])   
                    if(selllist[key][0]=='週'):
                        if(weeknumber==0): #不用檢查前一個
                            selldaysmemory[counter]=check(selllist[key][1],selllist[key][2],selldaysmemory[counter],newweek[weekcount][23])
                            checkselllist[counter]=checkother(selldaysmemory[counter])        
                        else:
                            if(weeklist[weeknumber]!=weeklist[weeknumber-1]):  #檢查前一個的週別是否一樣，一樣就不用再做判斷
                                selldaysmemory[counter]=check(selllist[key][1],selllist[key][2],selldaysmemory[counter],newweek[weekcount][23])
                                checkselllist[counter]=checkother(selldaysmemory[counter])    
                    if(selllist[key][0]=='月'):
                        if(weeknumber==0): #不用檢查前一個
                            selldaysmemory[counter]=check(selllist[key][1],selllist[key][2],selldaysmemory[counter],newmonth[monthcount][23])
                            checkselllist[counter]=checkother(selldaysmemory[counter])     
                        else:
                            if(monthlist[weeknumber]!=monthlist[weeknumber-1]):  #檢查前一個的週別是否一樣，一樣就不用再做判斷
                                selldaysmemory[counter]=check(selllist[key][1],selllist[key][2],selldaysmemory[counter],newmonth[monthcount][23])
                                checkselllist[counter]=checkother(selldaysmemory[counter])
                if(key=='波動率'): #波動率
                    if(selllist[key][0]=='日'):  
                        if(newday[i][25]!='#'):
                            number1=0.01*int(selllist[key][1])
                            number2=0.01*int(selllist[key][2])
                            if(float(newday[i][25])>number1 and float(newday[i][25])<number2):
                                selldaysmemory[counter]=11
                                checkselllist[counter]=checkother(selldaysmemory[counter])
                            else:
                                selldaysmemory[counter]=12
                                checkselllist[counter]=checkother(selldaysmemory[counter])
                        else:
                            selldaysmemory[counter]=12
                            checkselllist[counter]=checkother(selldaysmemory[counter])
                    if(selllist[key][0]=='週'):
                        if(weeknumber==0): #不用檢查前一個  
                            if(newweek[weekcount][25]!='#'):
                                number1=0.01*int(selllist[key][1])
                                number2=0.01*int(selllist[key][2])
                                if(float(newweek[weekcount][25])>number1 and float(newweek[weekcount][25])<number2):
                                    selldaysmemory[counter]=11
                                    checkselllist[counter]=checkother(selldaysmemory[counter])
                                else:
                                    selldaysmemory[counter]=12
                                    checkselllist[counter]=checkother(selldaysmemory[counter])
                            else:
                                selldaysmemory[counter]=12
                                checkselllist[counter]=checkother(selldaysmemory[counter])
                        else:
                            if(weeklist[weeknumber]!=weeklist[weeknumber-1]):  #檢查前一個的週別是否一樣，一樣就不用再做判斷
                                if(newweek[weekcount][25]!='#'):
                                    number1=0.01*int(selllist[key][1])
                                    number2=0.01*int(selllist[key][2])
                                    if(float(newweek[weekcount][25])>number1 and float(newweek[weekcount][25])<number2):
                                        selldaysmemory[counter]=11 
                                        checkselllist[counter]=checkother(selldaysmemory[counter]) 
                                    else:
                                        selldaysmemory[counter]=12 
                                        checkselllist[counter]=checkother(selldaysmemory[counter]) 
                                else:
                                    selldaysmemory[counter]=12
                                    checkselllist[counter]=checkother(selldaysmemory[counter])
                    if(selllist[key][0]=='月'):
                        if(weeknumber==0): #不用檢查前一個  
                            if(newmonth[monthcount][25]!='#'):
                                number1=0.01*int(selllist[key][1])
                                number2=0.01*int(selllist[key][2])
                                if(float(newmonth[monthcount][25])>number1 and float(newmonth[monthcount][25])<number2):
                                    selldaysmemory[counter]=11
                                    checkselllist[counter]=checkother(selldaysmemory[counter])
                                else:
                                    selldaysmemory[counter]=12
                                    checkselllist[counter]=checkother(selldaysmemory[counter])
                            else:
                                selldaysmemory[counter]=12
                                checkselllist[counter]=checkother(selldaysmemory[counter])
                        else:
                            if(monthlist[weeknumber]!=monthlist[weeknumber-1]):  #檢查前一個的週別是否一樣，一樣就不用再做判斷
                                if(newmonth[monthcount][25]!='#'):
                                    number1=0.01*int(selllist[key][1])
                                    number2=0.01*int(selllist[key][2])
                                    if(float(newmonth[monthcount][25])>number1 and float(newmonth[monthcount][25])<number2):
                                        selldaysmemory[counter]=11 
                                        checkselllist[counter]=checkother(selldaysmemory[counter])
                                    else:
                                        selldaysmemory[counter]=12  
                                        checkselllist[counter]=checkother(selldaysmemory[counter])
                                else:
                                    selldaysmemory[counter]=12
                                    checkselllist[counter]=checkother(selldaysmemory[counter])
                if(key=='日成交量'): #日成交量
                    selldaysmemory[counter]=VOLUME(results,newday[i][1],2,newday[i][2],selldaysmemory[counter],selllist[key][1])
                    checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][0])
                if(key=='週成交量'): #週成交量
                    if(weeknumber==0): #不用檢查前一個
                        selldaysmemory[counter]=VOLUME(weekresults,newweek[weekcount][1],2,newweek[weekcount][2],selldaysmemory[counter],selllist[key][1])
                        checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][0])
                    else:
                        if(weeklist[weeknumber]!=weeklist[weeknumber-1]):
                            selldaysmemory[counter]=VOLUME(weekresults,newweek[weekcount][1],2,newweek[weekcount][2],selldaysmemory[counter],selllist[key][1])
                            checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][0])
                if(key=='月成交量'): #月成交量
                    if(weeknumber==0): #不用檢查前一個
                        selldaysmemory[counter]=VOLUME(monthresults,newmonth[monthcount][1],2,newmonth[monthcount][2],selldaysmemory[counter],selllist[key][1])
                        checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][0])
                    else:
                        if(monthlist[weeknumber]!=monthlist[weeknumber-1]):
                            selldaysmemory[counter]=VOLUME(monthresults,newmonth[monthcount][1],2,newmonth[monthcount][2],selldaysmemory[counter],selllist[key][1])
                            checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][0])
                if(key=='三大法人'): #三大法人
                    selldaysmemory[counter]=other(selllist[key][0],selldaysmemory[counter],newthree[i][7])
                    checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][1])
                if(key=='外資'): #外資
                    selldaysmemory[counter]=other(selllist[key][0],selldaysmemory[counter],str(float(newthree[i][2])+float(newthree[i][3])))
                    checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][1])
                if(key=='投信'): #投信
                    selldaysmemory[counter]=other(selllist[key][0],selldaysmemory[counter],newthree[i][4])
                    checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][1])
                if(key=='自營商'): #自營商
                    selldaysmemory[counter]=other(selllist[key][0],selldaysmemory[counter],str(float(newthree[i][5])+float(newthree[i][6])))
                    checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][1])
                if(key=='券資比'): #券資比
                    selldaysmemory[counter]=VOLUME(chan,newday[i][1],14,newchan[i][14],selldaysmemory[counter],selllist[key][0])
                    checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][1])
                if(key=='融資'): #融資
                    selldaysmemory[counter]=VOLUME(chan,newday[i][1],6,newchan[i][6],selldaysmemory[counter],selllist[key][0])
                    checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][1])
                if(key=='融券'): #融券
                    selldaysmemory[counter]=VOLUME(chan,newday[i][1],13,newchan[i][13],selldaysmemory[counter],selllist[key][0])
                    checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][1]) 
                if(key=='通道股價'): #通道股價
                    selldaysmemory[counter]=boolean(selllist[key][0],newday[i][1],results,newday[i][17],selllist[key][1],0)
                    checkselllist[counter]=checkother(selldaysmemory[counter]) 
                if(key=='通道開口'): #通道開口
                    selldaysmemory[counter]=boolean(selllist[key][0],newday[i][1],results,newday[i][17],selllist[key][1],selldaysmemory[counter])
                    checkselllist[counter]=checkday(selldaysmemory[counter],selllist[key][1]) 
            for a in range(len(checkselllist)):
                if(checkselllist[a]=='NO'): #一個條件不行全部重判斷
                    totalday[2].append(newday[i][1])
                    break
                elif(a==(len(checkselllist)-1) and checkselllist[a]=='YES'): #最後一個也為YES代表可以買
                    count=0
                    totalday[1].append(newday[i][1]) #記錄買的日期
                    counter=-1
                    money.append(newday[i][7])
                    #清空紀錄欄
                    selldaysmemory=[0 for i in range(len(selllist))]
                    checkselllist=['' for i in range(len(selllist))]
    if(count==1):
        b='目前有持股'
    else:
        b='目前無持股'
    moneyadd=0
    if(len(money)==1):
        money=0
    else:
        if(len(money)%2==0): #偶數
            for i in range(1,len(money),2):
                moneyadd=moneyadd+float(money[i])-float(money[i-1])  
        else:
            for i in range(1,len(money)-1,2):
                moneyadd=moneyadd+float(money[i])-float(money[i-1])
    moneyadd=Decimal(moneyadd*1000).quantize(Decimal("0.01"), rounding = "ROUND_HALF_UP")
    return b,totalday,moneyadd
def KD(operator,value,days,getvalue):
    if(getvalue=='#' or value=='#'):
        return 0
    elif(operator=='>'):
        if(float(getvalue)>float(value)):
            days+=1
            return days
        else:
            return 0
    elif(operator=='<'):
        if(float(getvalue) < float(value)):
            days+=1
            return days
        else:
            return 0
    elif(operator=='='):
        if(float(getvalue)==float(value)):
            days+=1
            return days
        else:
            return 0
    elif(operator=='買超'):
        if(float(getvalue)>0):
            days+=1
            return days
        else:
            return 0
    elif(operator=='賣超'):
        if(float(getvalue)<0):
            days+=1
            return days
        else:
            return 0 
def GD(results,newlistvalue,value1,value2,number1,number2,key):#資料list、要確認的日期、要確認的值
    for i in range(len(results)):
        if(newlistvalue==results[i][1]):
            temp1=results[i-1][number1] #找前一天的值
            temp2=results[i-1][number2] #找前一天的值
            break
    if(temp1=='#' or temp2=='#' or value1=='#' or value2=='#'):
        return 12
    elif(key=='黃金交叉'): #要檢查黃金交叉
        if(float(temp1)<float(temp2) and float(temp1)<float(value1) and float(temp2)<float(value2)):
            return 11
        else:
            return 12
    elif(key=='<20黃金交叉'): 
        if(float(temp1)<float(temp2) and float(temp1)<float(value1) and float(temp2)<float(value2) and float(value1)<20 and float(value2)<20 ):
            return 11
        else:
            return 12
    elif(key=='20~50黃金交叉'):
        if(float(temp1)<float(temp2) and float(temp1)<float(value1) and float(temp2)<float(value2) and float(value1)>20 and float(value2)>20 and float(value1)<50 and float(value2)<50 ):
            return 11
        else:
            return 12
    elif(key=='50~80黃金交叉'):
        if(float(temp1)<float(temp2) and float(temp1)<float(value1) and float(temp2)<float(value2) and float(value1)>50 and float(value2)>50 and float(value1)<80 and float(value2)<80):
            return 11
        else:
            return 12
    elif(key=='>80黃金交叉'):
        if(float(temp1)<float(temp2) and float(temp1)<float(value1) and float(temp2)<float(value2) and float(value1)>80 and float(value2)>80):
            return 11
        else:
            return 12
    elif(key=='死亡交叉'): #要檢查死亡交叉
        if(float(temp1)>float(temp2) and float(temp1)>float(value1) and float(temp2)>float(value2)):
            return 11
        else:
            return 12
    elif(key=='<20死亡交叉'): 
        if(float(temp1)>float(temp2) and float(temp1)>float(value1) and float(temp2)>float(value2) and float(value1)<20 and float(value2)<20 ):
            return 11
        else:
            return 12
    elif(key=='20~50死亡交叉'):
        if(float(temp1)>float(temp2) and float(temp1)>float(value1) and float(temp2)>float(value2) and float(value1)>20 and float(value2)>20 and float(value1)<50 and float(value2)<50 ):
            return 11
        else:
            return 12
    elif(key=='50~80死亡交叉'):
        if(float(temp1)>float(temp2) and float(temp1)>float(value1) and float(temp2)>float(value2) and float(value1)>50 and float(value2)>50 and float(value1)<80 and float(value2)<80):
            return 11
        else:
            return 12
    elif(key=='>80死亡交叉'):
        if(float(temp1)>float(temp2) and float(temp1)>float(value1) and float(temp2)>float(value2) and float(value1)>80 and float(value2)>80):
            return 11
        else:
            return 12   
def Place(operator,MACDvalue,DIFvalue):
    if(MACDvalue == '#' or DIFvalue=='#'):
        return 12
    elif(operator=='>'):
        if(float(MACDvalue)>0 and float(DIFvalue)>0):
            return 11
        else:
            return 12
    elif(operator=='<'):
        if(float(MACDvalue)<0 and float(DIFvalue)<0):
            return 11
        else:
            return 12
    elif(operator=='='):
        if(float(MACDvalue)==0.0 and float(DIFvalue)==0.0):
            return 11
        else:
            return 12
def VALUE(results,newlistvalue,number5,number20,number60,value5,value20,value60,key,gd):
    for i in range(len(results)):
        if(newlistvalue==results[i][1]):
            temp1=results[i-1][value5] #找前一天的成交價/量均值(5)
            temp2=results[i-1][value20] #找前一天的成交價/量均值(20)
            temp3=results[i-1][value60] #找前一天的成交價/量均值(60)
            break
    if(key=='5/20' and float(number5)==float(number20) and temp1!='#' and temp2!='#' and number5 !='#' and number20 !='#'): #5/20
        if(gd==0): #黃金
            if(float(temp1)<float(temp2) and float(temp1)<float(number5) and float(temp2)<float(number20)):
                return 11
            else:
                return 12
        else:      #死亡
            if(float(temp1)>float(temp2) and float(temp1)>float(number5) and float(temp2)>float(number20)):
                return 11
            else:
                return 12
    else:
        return 12
    if(key=='5/60' and float(number5)==float(number60) and temp1!='#' and temp3!='#' and number5 !='#' and number60!='#'): #5/60
        if(gd==0): #黃金
            if(float(temp1)<float(temp3) and float(temp1)<float(number5) and float(temp2)<float(number60)):
                return 11
            else:
                return 12
        else:      #死亡
            if(float(temp1)>float(temp3) and float(temp1)>float(number5) and float(temp2)>float(number60)):
                return 11
            else:
                return 12
    else:
        return 12
    if(key=='20/60' and float(number20)==float(number60) and temp2!='#' and temp3!='#' and number20!='#' and number60!='#'): #20/60
        if(gd==0): #黃金
            if(float(temp2)<float(temp3) and float(temp2)<float(number20) and float(temp3)<float(number60)):
                return 11
            else:
                return 12
        else:      #死亡
            if(float(temp2)>float(temp3) and float(temp2)>float(number20) and float(temp3)>float(number60)):
                return 11
            else:
                return 12 
    else:
        return 12
def VOLUME(results,valuedate,number,value,days,key):
    for i in range(len(results)):
        if(valuedate==results[i][1]):
            temp1=results[i-1][number] #找前一天的值
            break
    if(temp1!='#' and value!='#'):
        if(key=='增加'): #增加
            if(float(value)>float(temp1)):
                days+=1
                return days
            else:
                return 0
        if(key=='減少'): #減少
            if(float(value)<float(temp1)):
                days+=1
                return days
            else:
                return 0
    else:
        return 0  
def check(operator,value,days,getvalue):
    if(getvalue=='#' or value=='#'):
        return 12
    elif(operator=='>'):
        if(float(getvalue)>float(value)):
            return 11
        else:
            return 12
    elif(operator=='<'):
        if(float(getvalue) < float(value)):
            return 11
        else:
            return 12
    elif(operator=='='):
        if(float(getvalue)==float(value)):
            return 11
        else:
            return 12  
def checkday(days,daysmemory):
    if(days==float(daysmemory)):
        return 'YES'
    else:
        return 'NO'
def checkother(checkchar):  
    if(checkchar==11):
        return 'YES'
    if(checkchar==12):
        return 'NO'
def other(key,days,value):
    if(key=='買超'):
        if(value!='#'):
            if(float(value)>0):
                days+=1
                return days
            else:
                return 0
        else:
            return 0
    elif(key=='賣超'):
        if(value!='#'):
            if(float(value)<0):
                days+=1
                return days
            else:
                return 0
        else:
            return 0
def boolean(key,date,results,ma20,mbnumber,days):
    for i in range(len(results)):
        if(date==results[i][1]): #找到位置
            if(i==0):
                return 12
                break
            else:
                position=i
                yesterdayposition=i-1
                yesterdaygmoney=results[i-1][7]
                break
    b=position-1 #往前找
    a=0
    yesterdayb=position-2#算昨日的標準差
    yesterdaya=0
    yesterdayma20=results[b][17]#前一天的MA20
    for i in range(19):
        if(float(results[b][7])=='#'):
            return 12
            break
        else:
            a=a+math.pow(float(results[b][7])-float(ma20),2)
            b-=1
        if(float(results[yesterdayb][7])=='#'):
            return 12
            break
        else:
            yesterdaya=yesterdaya+math.pow(float(results[yesterdayb][7])-float(yesterdayma20),2)
            yesterdayb-=1
    yesterdayMB=math.sqrt(yesterdaya/20)   #算出昨日標準差
    MB=math.sqrt(a/20) #除以20開根號算出標準差
    ub=float(results[position][7])+2*MB
    lb=float(results[position][7])-2*MB
    yesub=float(results[position-1][7])+2*yesterdayMB
    yeslb=float(results[position-1][7])-2*yesterdayMB
    if(results[position][7]!='#' and yesterdaygmoney!='#'):
        submoney=float(results[position][7])-float(yesterdaygmoney) #今日價減昨日
    if(key=='突破'):
        if(submoney>0):
            nowmbnumber=submoney/MB
            if(float(nowmbnumber)>=float(mbnumber)):
                return 11
            else:
                return 12
        else:
            return  12  
    elif(key=='跌破'):
        if(submoney<0):
            nowmbnumber=submoney/MB
            if(float(nowmbnumber)<=(-float(mbnumber))):
                return 11
            else:
                return 12
        else:
            return 12
    elif(key=='變大'):
        if((ub-lb)>(yesub-yeslb)):
            return days+1
        else:
            return 0
    elif(key=='變小'):
        if((ub-lb)<(yesub-yeslb)):
            return days+1
        else:
            return 0

# test=[2015,1,2,2015,5,20]
# ssid=1101
# buynamelist=['日K','日K']
# buynumberlist=[['>','20','1'],['<','50','1']]
# sellnamelist=['賣壓比例']
# sellnumberlist=[['日','>','120']]

# count,datelist,moneylist=historytest(buynamelist,buynumberlist,sellnamelist,sellnumberlist,test,ssid)
# print(count)
# print(moneylist)
# print(datelist[0]) #買
# print(datelist[1]) #賣
# print(datelist[2]) #未交易


