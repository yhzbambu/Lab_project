import datetime
import time
import math
import sys
import os
import pymysql


def historytest(buylist,selllist,datelist,ssid):
    conn=pymysql.connect(host="163.18.104.164",
                    user="bobo",
                    password="bobo123",
                    db='stock',
                    charset='utf8'
                    )
    cursor=conn.cursor()
    cursor.execute("select * from DayStockInformation where sid='%d'" %(ssid)) #取得該股票所有的日成交資料
    results=list(cursor.fetchall()) #放入results中
    cursor.execute("select * from WeekStockInformation where sid='%d'" %(ssid))
    weekresults=list(cursor.fetchall())
    cursor.execute("select * from MonthStockInformation where sid='%d'" %(ssid))
    monthresults=list(cursor.fetchall())
    totalday=[[] for i in range(3)] #算交易日期(0:買、1:賣、2:未交易)
    
    buymoney=[] #買賣價格整理
    conbuyday=[] #紀錄連續幾日買(61)
    consellday=[] #紀錄連續幾日賣(61)
    record=[]
    recordweek=[]
    mrecord=[]
    recordmonth=[]
    for i in range(24):
        conbuyday.append(0)
        consellday.append(0) 
    buydaysmemory=[buylist[2],buylist[5],buylist[10],buylist[13],buylist[18],buylist[21],buylist[24],buylist[37],buylist[41],buylist[44],buylist[49],buylist[52],buylist[57],buylist[60],buylist[63],buylist[76],buylist[80],buylist[83],buylist[88],buylist[91],buylist[96],buylist[99],buylist[102],buylist[115]] #紀錄條件天數(買)(61)
    selldaysmemory=[selllist[2],selllist[5],selllist[10],selllist[13],selllist[18],selllist[21],selllist[24],selllist[37],selllist[41],selllist[44],selllist[49],selllist[52],selllist[57],selllist[60],selllist[63],selllist[76],selllist[80],selllist[83],selllist[88],selllist[91],selllist[96],selllist[99],selllist[102],selllist[115]] #紀錄條件天數(賣)(61)
    for i in range(len(buydaysmemory)):
        if(buydaysmemory[i]==''):
            buydaysmemory[i]='0'
        if(selldaysmemory[i]==''):
            selldaysmemory[i]='0'
    d1 = datetime.date(datelist[0],datelist[1],datelist[2])   
    d2 = datetime.date(datelist[3],datelist[4],datelist[5])
    newlist=[] #放該區段的資料
    abc=0
    for i in range(len(results)):
        if(results[i][1]>= d1 and results[i][1]<d2):
            newlist.append(results[i])
            abc+=1
        if(results[i][1]==d2):
            newlist.append(results[i])
            abc+=1
            break
    
    for j in range(abc):
        for i in range(len(weekresults)):    
            if(newlist[j][1]>= weekresults[i][27] and newlist[j][1]<=weekresults[i][28]):
                if(j==0): #第一位置一定放
                    record.append(weekresults[i][1]) #放週別
                    recordweek.append(weekresults[i]) #放週資料
                    continue
                else:
                    if(weekresults[i][1]==record[j-1]): #如果跟前者一樣就放週別就好
                        record.append(weekresults[i][1])
                        continue
                    else:
                        record.append(weekresults[i][1]) #放週別
                        recordweek.append(weekresults[i]) #放週資料
    for j in range(abc):
        for i in range(len(monthresults)):        
            if(newlist[j][1]>= monthresults[i][27] and newlist[j][1]<=monthresults[i][28]):
                if(j==0): #第一位置一定放
                    mrecord.append(monthresults[i][1]) #放月別
                    recordmonth.append(monthresults[i]) #放月資料
                    continue
                else:
                    if(monthresults[i][1]==mrecord[j-1]): #如果跟前者一樣就放週別就好
                        mrecord.append(monthresults[i][1])
                        continue
                    else:
                        mrecord.append(monthresults[i][1]) #放月別
                        recordmonth.append(monthresults[i]) #放月資料
    #print(recordmonth)
    count=0 #無持股
    weekcount=0
    monthcount=0
    for i in range(len(newlist)):
        
        weeknumber=i
        if(count==0): #只需關心買入條件
            if(buylist[0]!=''): #判斷日K
                DKanswer,conbuyday[0]=KD(buylist[0],buylist[1],conbuyday[0],newlist[i][10])
                if(DKanswer=="NO"):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(buylist[3]!=''): #判斷日D
                (DDanswer,conbuyday[1])=KD(buylist[3],buylist[4],conbuyday[1],newlist[i][11])
                if(DDanswer=="NO"):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(buylist[6] != ''): #判斷黃金交叉 
                if(newlist[i][10]==newlist[i][11]): #交叉
                    ans=check(buylist[6],float(newlist[i][10]),float(newlist[i][11]))
                    if(ans=="YES"): 
                        Ganswer=GD(results,newlist[i][1],newlist[i][10],newlist[i][11],10,11,0) 
                    else: continue       
                    if(Ganswer=="NO"):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue 
                else: continue               
            if(buylist[7]!=''): #判斷死亡交叉
                if(newlist[i][10]==newlist[i][11]): #交叉
                    ans=check(buylist[6],float(newlist[i][10]),float(newlist[i][11]))
                    if(ans=="YES"): 
                        Ganswer=GD(results,newlist[i][1],newlist[i][10],newlist[i][11],10,11,1)
                    else: continue       
                    if(Ganswer=="NO"):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue 
                else: continue 
            if(buylist[8]!=''): #判斷日MACD
                DMACD,conbuyday[2]=KD(buylist[8],buylist[9],conbuyday[2],newlist[i][15]) 
                if(DMACD=='NO'):
                    conbuyday[2]=0 #天數歸零
                    totalday[2].append(newlist[i][1])
                    continue
            if(buylist[11]!=''): #判斷日DIF
                DDIF,conbuyday[3]=KD(buylist[11],buylist[12],conbuyday[3],newlist[i][22])
                if(DDIF=='NO'):
                    conbuyday[3]=0 #天數歸零
                    totalday[2].append(newlist[i][1])
                    continue
            if(buylist[14]!=''): #判斷日MACD落點
                palceanswer=Place(buylist[14],newlist[i][15],newlist[i][22]) 
                if(palceanswer=='NO'): #不成立
                    totalday[2].append(newlist[i][1])
                    continue
            if(buylist[15]!=''): #判斷DIF與MACD的黃金交叉或死亡交叉
                if(newlist[i][15]==newlist[i][22]): #若相同則繼續判斷
                    if(buylist[15]=='1'): #黃金
                        DManswer=GD(results,newlist[i][1],newlist[i][22],newlist[i][15],22,15,0)
                        if(DManswer=='NO'):
                            totalday[2].append(newlist[i][1])
                            continue
                    elif(buylist[15]=='2'): #死亡
                        DManswer=GD(results,newlist[i][1],newlist[i][22],newlist[i][15],22,15,1)
                        if(DManswer=='NO'):
                            totalday[2].append(newlist[i][1])
                            continue
                else:
                    continue
            if(buylist[16]!=''): #判斷日RSI(6)
                RSIsix,conbuyday[4]=KD(buylist[16],buylist[17],conbuyday[4],newlist[i][12])
                if(RSIsix=="NO"):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(buylist[19]!=''): #判斷日RSI(9)
                RSInine,conbuyday[5]=KD(buylist[19],buylist[20],conbuyday[5],newlist[i][13])
                if(RSInine=="NO"):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(buylist[22]!=''): #判斷日RSI(12)
                RSItwelve,conbuyday[6]=KD(buylist[22],buylist[23],conbuyday[6],newlist[i][14])
                if(RSItwelve=="NO"):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(buylist[25]!=''): #判斷日RSI黃金交叉
                if(newlist[i][12]==newlist[i][14]): #交叉
                    ans=check(buylist[25],float(newlist[i][12]),float(newlist[i][14]))
                    if(ans=="YES"): 
                        KGanswer=GD(results,newlist[i][1],newlist[i][12],newlist[i][14],12,14,0)
                    else: continue      
                    if(KGanswer=="NO"):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue 
                    else: continue 
            if(buylist[26]!=''): #判斷日RSI死亡交叉    
                if(newlist[i][12]==newlist[i][14]): #交叉
                    ans=check(buylist[26],float(newlist[i][12]),float(newlist[i][14]))
                    if(ans=="YES"): 
                        KGanswer=GD(results,newlist[i][1],newlist[i][12],newlist[i][14],12,14,1)
                    else: continue      
                    if(KGanswer=="NO"):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue 
                    else: continue
            if(buylist[27]!=''):#判斷均價線黃金交叉
                ganswer=VALUE(results,newlist[i][1],newlist[i][16],newlist[i][18],newlist[i][20],16,18,20,buylist[27],0)
                if(ganswer=="NO"):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(buylist[28]!=''):#判斷均價線死亡交叉
                danswer=VALUE(results,newlist[i][1],newlist[i][16],newlist[i][18],newlist[i][20],16,18,20,buylist[28],1)
                if(danswer=="NO"):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(buylist[29]!=''):#判斷均量線黃金交叉
                ganswer=VALUE(results,newlist[i][1],newlist[i][17],newlist[i][19],newlist[i][21],17,19,21,buylist[29],0)
                if(ganswer=="NO"):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(buylist[30]!=''):#判斷均量線死亡交叉
                danswer=VALUE(results,newlist[i][1],newlist[i][17],newlist[i][19],newlist[i][21],17,19,21,buylist[30],1)
                if(danswer=="NO"):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(buylist[31]!=''):#判斷日賣壓比例
                if(buylist[31]=='>'):
                    if(float(newlist[i][24])<buylist[32] or float(newlist[i][24])==buylist[32]):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue 
                elif(buylist[31]=='<'):
                    if(float(newlist[i][24])>buylist[32] or float(newlist[i][24])==buylist[32]):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue
                elif(buylist[31]=='='):
                    if(float(newlist[i][24])<buylist[32] or float(newlist[i][24])>buylist[32]):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue
            if(buylist[33]!=''):#判斷日MFI
                if(buylist[33]=='>'):
                    if(float(newlist[i][23])<buylist[34] or float(newlist[i][23])==buylist[34]):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue 
                elif(buylist[33]=='<'):
                    if(float(newlist[i][23])>buylist[34] or float(newlist[i][23])==buylist[34]):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue
                elif(buylist[33]=='='):
                    if(float(newlist[i][23])<buylist[34] or float(newlist[i][23])>buylist[34]):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue    
            if(buylist[35]!='' and buylist[36]!=''): #判斷日波動率
                number1=0.01*buylist[35]
                number2=0.01*buylist[36]      
                if(float(newlist[i][25])<number1 or float(newlist[i][25])==number1 or float(newlist[i][25])>number2 or float(newlist[i][25])==number2):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(buylist[37]!=''): #日成交量
                if(buylist[38]==1): #增加
                    volumeanswer,conbuyday[7]=VOLUME(results,newlist[i][1],2,newlist[i][2],conbuyday[7],1)
                    if(volumeanswer=="NO"):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
                if(buylist[38]==2):  #減少
                    volumeanswer,conbuyday[7]=VOLUME(results,newlist[i][1],2,newlist[i][2],conbuyday[7],2)
                    if(volumeanswer=="NO"):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            #週成交判斷            
            if(weeknumber!=0):
                if(record[weeknumber]!=record[weeknumber-1]): #不同代表下週了!
                    weekcount+=1
            #找前一周
            if(buylist[39]!=''): #判斷週K
                WKanswer,conbuyday[8]=KD(buylist[39],buylist[40],conbuyday[8],recordweek[weekcount][10]) 
                if(WKanswer=='NO'):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(buylist[39]!=''): #判斷週D
                WDanswer,conbuyday[9]=KD(buylist[42],buylist[43],conbuyday[9],recordweek[weekcount][11]) 
                if(WDanswer=='NO'):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue   
            if(buylist[45] != ''): #判斷黃金交叉 
                if(recordweek[weekcount][10]==recordweek[weekcount][11]): #交叉
                    ans=check(buylist[45],float(recordweek[weekcount][10]),float(recordweek[weekcount][11]))
                    if(ans=="YES"): 
                        KGanswer=GD(weekresults,recordweek[weekcount][1],recordweek[weekcount][10],recordweek[weekcount][11],10,11,0)
                    else: continue      
                    if(KGanswer=="NO"):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue 
                else: continue
            if(buylist[46] != ''): #判斷死亡交叉 
                if(recordweek[weekcount][10]==recordweek[weekcount][11]): #交叉
                    ans=check(buylist[46],float(recordweek[weekcount][10]),float(recordweek[weekcount][11]))
                    if(ans=="YES"): 
                        KGanswer=GD(weekresults,recordweek[weekcount][1],recordweek[weekcount][10],recordweek[weekcount][11],10,11,1)
                    else: continue             
                    if(KGanswer=="NO"):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue 
                else: continue 
            if(buylist[47]!=''): #判斷週MACD
                WMACD,conbuyday[10]=KD(buylist[47],buylist[48],conbuyday[10],recordweek[weekcount][15]) 
                if(WMACD=='NO'):
                    totalday[2].append(newlist[i][1])
                    continue
            if(buylist[50]!=''): #判斷週DIF
                WDIF,conbuyday[11]=KD(buylist[50],buylist[51],conbuyday[11],recordweek[weekcount][22])
                if(WDIF=='NO'):
                    totalday[2].append(newlist[i][1])
                    continue
            if(buylist[53]!=''): #判斷週MACD落點
                Wpalceanswer=Place(buylist[53],recordweek[weekcount][15],recordweek[weekcount][22]) 
                if(Wpalceanswer=='NO'): #不成立
                    totalday[2].append(newlist[i][1])
                    continue
            if(buylist[54]!=''): #判斷DIF與MACD的黃金交叉或死亡交叉
                if(recordweek[weekcount][15]==recordweek[weekcount][22]): #若相同則繼續判斷
                    if(buylist[54]=='1'): #黃金
                        WManswer=GD(weekresults,recordweek[weekcount][1],recordweek[weekcount][22],recordweek[weekcount][15],22,15,0)
                        if(WManswer=='NO'):
                            totalday[2].append(newlist[i][1])
                            continue
                    elif(buylist[54]=='2'): #死亡
                        WManswer=GD(weekresults,recordweek[weekcount][1],recordweek[weekcount][22],recordweek[weekcount][15],22,15,1)
                        if(WManswer=='NO'):
                            totalday[2].append(newlist[i][1])
                            continue
                else:
                    continue
            if(buylist[55]!=''): #判斷週RSI(6)
                RSIsix,conbuyday[12]=KD(buylist[55],buylist[56],conbuyday[12],recordweek[weekcount][12])
                if(RSIsix=="NO"):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(buylist[58]!=''): #判斷週RSI(9)
                RSInine,conbuyday[13]=KD(buylist[58],buylist[59],conbuyday[13],recordweek[weekcount][13])
                if(RSInine=="NO"):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(buylist[61]!=''): #判斷週RSI(12)
                RSItwelve,conbuyday[14]=KD(buylist[61],buylist[62],conbuyday[14],recordweek[weekcount][14])
                if(RSItwelve=="NO"):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(buylist[64]!=''): #判斷週RSI黃金交叉
                if(recordweek[weekcount][12]==recordweek[weekcount][14]): #交叉
                    ans=check(buylist[64],float(recordweek[weekcount][12]),float(recordweek[weekcount][14]))
                    if(ans=="YES"): 
                        KGanswer=GD(weekresults,recordweek[weekcount][1],recordweek[weekcount][12],recordweek[weekcount][14],12,14,0)
                    else: continue      
                    if(KGanswer=="NO"):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue 
                    else: continue
            if(buylist[65]!=''): #判斷週RSI死亡交叉
                if(recordweek[weekcount][12]==recordweek[weekcount][14]): #交叉
                    ans=check(buylist[64],float(recordweek[weekcount][12]),float(recordweek[weekcount][14]))
                    if(ans=="YES"): 
                        KGanswer=GD(weekresults,recordweek[weekcount][1],recordweek[weekcount][12],recordweek[weekcount][14],12,14,1)
                    else: continue      
                    if(KGanswer=="NO"):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue 
                    else: continue
            if(buylist[66]!=''):#判斷均價線黃金交叉
                Wganswer=VALUE(weekresults,recordweek[weekcount][1],recordweek[weekcount][16],recordweek[weekcount][18],recordweek[weekcount][20],16,18,20,buylist[66],0)
                if(Wganswer=="NO"):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(buylist[67]!=''):#判斷均價線死亡交叉
                Wdanswer=VALUE(weekresults,recordweek[weekcount][1],recordweek[weekcount][16],recordweek[weekcount][18],recordweek[weekcount][20],16,18,20,buylist[67],1)
                if(Wdanswer=="NO"):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(buylist[68]!=''):#判斷均量線黃金交叉
                Wganswer=VALUE(weekresults,recordweek[weekcount][1],recordweek[weekcount][17],recordweek[weekcount][19],recordweek[weekcount][21],17,19,21,buylist[68],0)
                if(ganswer=="NO"):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(buylist[69]!=''):#判斷均量線死亡交叉
                Wdanswer=VALUE(weekresults,recordweek[weekcount][1],recordweek[weekcount][17],recordweek[weekcount][19],recordweek[weekcount][21],17,19,21,buylist[69],1)
                if(danswer=="NO"):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(buylist[70]!=''):#判斷週賣壓比例
                if(buylist[70]=='>'):
                    if(float(recordweek[weekcount][24])<buylist[71] or float(recordweek[weekcount][24])==buylist[71]):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue 
                elif(buylist[70]=='<'):
                    if(float(recordweek[weekcount][24])>buylist[71] or float(recordweek[weekcount][24])==buylist[71]):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue
                elif(buylist[70]=='='):
                    if(float(recordweek[weekcount][24])<buylist[71] or float(recordweek[weekcount][24])>buylist[71]):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue
            if(buylist[72]!=''):#判斷週MFI
                if(buylist[72]=='>'):
                    if(float(recordweek[weekcount][23])<buylist[73] or float(recordweek[weekcount][23])==buylist[73]):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue 
                elif(buylist[72]=='<'):
                    if(float(recordweek[weekcount][23])>buylist[73] or float(recordweek[weekcount][23])==buylist[73]):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue
                elif(buylist[72]=='='):
                    if(float(recordweek[weekcount][23])<buylist[73] or float(recordweek[weekcount][23])>buylist[73]):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue 
            if(buylist[74]!='' and buylist[75]!=''): #判斷週波動率
                number1=0.01*buylist[74]
                number2=0.01*buylist[75]      
                if(float(recordweek[weekcount][25])<number1 or float(recordweek[weekcount][25])==number1 or float(recordweek[weekcount][25])>number2 or float(recordweek[weekcount][25])==number2):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(buylist[76]!=''): #週成交量
                if(buylist[77]==1): #增加
                    Wvolumeanswer,conbuyday[15]=VOLUME(weekresults,recordweek[weekcount][1],2,recordweek[weekcount][2],conbuyday[15],1)
                    if(Wvolumeanswer=="NO"):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
                if(buylist[77]==2):  #減少
                    Wvolumeanswer,conbuyday[15]=VOLUME(weekresults,recordweek[weekcount][1],2,recordweek[weekcount][2],conbuyday[15],2)
                    if(Wvolumeanswer=="NO"):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            #月成交判斷
            if(weeknumber!=0):
                if(record[weeknumber]!=record[weeknumber-1]): #不同代表下個月了!
                    monthcount+=1
            if(buylist[78]!=''): #判斷月K
                MKanswer,conbuyday[16]=KD(buylist[78],buylist[79],conbuyday[16],recordmonth[monthcount][10]) 
                if(MKanswer=='NO'):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(buylist[81]!=''): #判斷月D
                MDanswer,conbuyday[17]=KD(buylist[81],buylist[82],conbuyday[17],recordmonth[monthcount][11]) 
                if(MDanswer=='NO'):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue  
            if(buylist[84] != ''): #判斷黃金交叉 
                if(recordmonth[monthcount][10]==recordmonth[monthcount][11]): #交叉
                    ans=check(buylist[84],float(recordmonth[monthcount][10]),float(recordmonth[monthcount][11]))
                    if(ans=="YES"): 
                        MGanswer=GD(monthresults,recordmonth[monthcount][1],recordmonth[monthcount][10],recordmonth[monthcount][11],10,11,0)
                    else: continue      
                    if(MGanswer=="NO"):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue 
                else: continue
            if(buylist[85] != ''): #判斷死亡交叉 
                if(recordmonth[monthcount][10]==recordmonth[monthcount][11]): #交叉
                    ans=check(buylist[85],float(recordmonth[monthcount][10]),float(recordmonth[monthcount][11]))
                    if(ans=="YES"): 
                        MGanswer=GD(monthresults,recordmonth[monthcount][1],recordmonth[monthcount][10],recordmonth[monthcount][11],10,11,1)
                    else: continue      
                    if(MGanswer=="NO"):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue 
                else: continue
            if(buylist[86]!=''): #判斷月MACD
                MMACD,conbuyday[18]=KD(buylist[86],buylist[87],conbuyday[18],recordmonth[monthcount][15]) 
                if(MMACD=='NO'):
                    totalday[2].append(newlist[i][1])
                    continue
            if(buylist[89]!=''): #判斷週DIF
                MDIF,conbuyday[19]=KD(buylist[89],buylist[90],conbuyday[19],recordmonth[monthcount][22])
                if(MDIF=='NO'):
                    totalday[2].append(newlist[i][1])
                    continue
            if(buylist[92]!=''): #判斷月MACD落點
                Mpalceanswer=Place(buylist[92],recordmonth[monthcount][15],recordmonth[monthcount][22]) 
                if(Mpalceanswer=='NO'): #不成立
                    totalday[2].append(newlist[i][1])
                    continue
            if(buylist[93]!=''): #判斷DIF與MACD的黃金交叉或死亡交叉
                if(recordmonth[monthcount][15]==recordmonth[monthcount][22]): #若相同則繼續判斷
                    if(buylist[93]=='1'): #黃金
                        MManswer=GD(monthresults,recordmonth[monthcount][1],recordmonth[monthcount][22],recordmonth[monthcount][15],22,15,0)
                        if(MManswer=='NO'):
                            totalday[2].append(newlist[i][1])
                            continue
                    elif(buylist[93]=='2'): #死亡
                        MManswer=GD(monthresults,recordmonth[monthcount][1],recordmonth[monthcount][22],recordmonth[monthcount][15],22,15,1)
                        if(MManswer=='NO'):
                            totalday[2].append(newlist[i][1])
                            continue
                else: continue
            if(buylist[94]!=''): #判斷月RSI(6)
                RSIsix,conbuyday[20]=KD(buylist[94],buylist[95],conbuyday[20],recordmonth[monthcount][20])
                if(RSIsix=="NO"):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(buylist[97]!=''): #判斷月RSI(9)
                RSInine,conbuyday[21]=KD(buylist[97],buylist[98],conbuyday[21],recordmonth[monthcount][13])
                if(RSInine=="NO"):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(buylist[100]!=''): #判斷月RSI(12)
                RSItwelve,conbuyday[22]=KD(buylist[100],buylist[101],conbuyday[22],recordmonth[monthcount][14])
                if(RSItwelve=="NO"):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(buylist[103]!=''): #判斷月RSI黃金交叉
                if(recordmonth[monthcount][12]==recordmonth[monthcount][14]): #交叉
                    ans=check(buylist[103],float(recordmonth[monthcount][12]),float(recordmonth[monthcount][14]))
                    if(ans=="YES"): 
                        KGanswer=GD(monthresults,recordmonth[monthcount][1],recordmonth[monthcount][12],recordmonth[monthcount][14],12,14,0)
                    else: continue      
                    if(KGanswer=="NO"):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue 
                    else: continue
            if(buylist[104]!=''): #判斷月RSI死亡交叉
                if(recordmonth[monthcount][12]==recordmonth[monthcount][14]): #交叉
                    ans=check(buylist[104],float(recordmonth[monthcount][12]),float(recordmonth[monthcount][14]))
                    if(ans=="YES"): 
                        KGanswer=GD(monthresults,recordmonth[monthcount][1],recordmonth[monthcount][12],recordmonth[monthcount][14],12,14,1)
                    else: continue      
                    if(KGanswer=="NO"):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue 
                    else: continue
            if(buylist[105]!=''):#判斷均價線黃金交叉
                Wganswer=VALUE(monthresults,recordmonth[monthcount][1],recordmonth[monthcount][16],recordmonth[monthcount][18],recordmonth[monthcount][20],16,18,20,buylist[105],0)
                if(Wganswer=="NO"):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(buylist[106]!=''):#判斷均價線死亡交叉
                Wdanswer=VALUE(monthresults,recordmonth[monthcount][1],recordmonth[monthcount][16],recordmonth[monthcount][18],recordmonth[monthcount][20],16,18,20,buylist[106],1)
                if(Wdanswer=="NO"):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(buylist[107]!=''):#判斷均量線黃金交叉
                Wganswer=VALUE(monthresults,recordmonth[monthcount][1],recordmonth[monthcount][17],recordmonth[monthcount][19],recordmonth[monthcount][21],17,19,21,buylist[107],0)
                if(ganswer=="NO"):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(buylist[108]!=''):#判斷均量線死亡交叉
                Wdanswer=VALUE(monthresults,recordmonth[monthcount][1],recordmonth[monthcount][17],recordmonth[monthcount][19],recordmonth[monthcount][21],17,19,21,buylist[108],1)
                if(danswer=="NO"):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(buylist[109]!=''):#判斷月賣壓比例
                if(buylist[109]=='>'):
                    if(float(recordmonth[monthcount][24])<buylist[110] or float(recordmonth[monthcount][24])==buylist[110]):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue 
                elif(buylist[109]=='<'):
                    if(float(recordmonth[monthcount][24])>buylist[110] or float(recordmonth[monthcount][24])==buylist[110]):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue
                elif(buylist[109]=='='):
                    if(float(recordmonth[monthcount][24])<buylist[110] or float(recordmonth[monthcount][24])>buylist[110]):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue
            if(buylist[111]!=''):#判斷月MFI
                if(buylist[111]=='>'):
                    if(float(recordmonth[monthcount][23])<buylist[112] or float(recordmonth[monthcount][23])==buylist[112]):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue 
                elif(buylist[111]=='<'):
                    if(float(recordmonth[monthcount][23])>buylist[112] or float(recordmonth[monthcount][23])==buylist[112]):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue
                elif(buylist[111]=='='):
                    if(float(recordmonth[monthcount][23])<buylist[112] or float(recordmonth[monthcount][23])>buylist[112]):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue
            if(buylist[113]!='' and buylist[114]!=''): #判斷月波動率
                number1=0.01*buylist[113]
                number2=0.01*buylist[114]      
                if(float(recordmonth[monthcount][25])<number1 or float(recordmonth[monthcount][25])==number1 or float(recordmonth[monthcount][25])>number2 or float(recordmonth[monthcount][25])==number2):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(buylist[115]!=''): #月成交量
                if(buylist[116]==1): #增加
                    Wvolumeanswer,conbuyday[23]=VOLUME(monthresults,recordmonth[monthcount][1],2,recordmonth[monthcount][2],conbuyday[23],1)
                    if(Wvolumeanswer=="NO"):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
                if(buylist[116]==2):  #減少
                    Wvolumeanswer,conbuyday[23]=VOLUME(monthresults,recordmonth[monthcount][1],2,recordmonth[monthcount][2],conbuyday[23],2)
                    if(Wvolumeanswer=="NO"):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            for j in range(len(conbuyday)):
                if(buydaysmemory[j]!=''): 
                    if(conbuyday[j]==int(buydaysmemory[j])):     
                        if(j==(len(conbuyday)-1)):
                            count=1 #代表買了
                            weekcount=0
                            monthcount=0
                            for g in range(len(conbuyday)):
                                conbuyday[g]=0
                            totalday[0].append(newlist[i][1])
                            buymoney.append(newlist[i][7]) #紀錄收盤價
                            break
                        else:
                            continue
                    else: 
                        totalday[2].append(newlist[i][1])
                        break
                else: #不成立
                    continue
            continue
        if(count==1): #只需關心賣出條件
            if(selllist[0]!=''): #判斷日K
                DKanswer,consellday[0]=KD(selllist[0],selllist[1],consellday[0],newlist[i][10])
                if(DKanswer=="NO"):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(selllist[3]!=''): #判斷日D
                (DDanswer,consellday[1])=KD(selllist[3],selllist[4],consellday[1],newlist[i][11])
                if(DDanswer=="NO"):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(selllist[6] != ''): #判斷黃金交叉 
                if(newlist[i][10]==newlist[i][11]): #交叉
                    ans=check(int(selllist[6]),float(newlist[i][10]),float(newlist[i][11]))
                    if(ans=="YES"): 
                        Ganswer=GD(results,newlist[i][1],newlist[i][10],newlist[i][11],10,11,0) 
                    else: continue       
                    if(Ganswer=="NO"):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue 
                else: continue               
            if(selllist[7]!=''): #判斷死亡交叉
                if(newlist[i][10]==newlist[i][11]): #交叉
                    ans=check(int(selllist[6]),float(newlist[i][10]),float(newlist[i][11]))
                    if(ans=="YES"): 
                        Ganswer=GD(results,newlist[i][1],newlist[i][10],newlist[i][11],10,11,1)
                    else: continue       
                    if(Ganswer=="NO"):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue 
                else: continue 
            if(selllist[8]!=''): #判斷日MACD
                DMACD,consellday[2]=KD(selllist[8],buylist[9],consellday[2],newlist[i][15]) 
                if(DMACD=='NO'):
                    totalday[2].append(newlist[i][1])
                    continue
            if(selllist[11]!=''): #判斷日DIF
                DDIF,consellday[3]=KD(buylist[11],buylist[12],consellday[3],newlist[i][22])
                if(DDIF=='NO'):
                    totalday[2].append(newlist[i][1])
                    continue
            if(selllist[14]!=''): #判斷日MACD落點
                palceanswer=Place(selllist[14],newlist[i][15],newlist[i][22]) 
                if(palceanswer=='NO'): #不成立
                    totalday[2].append(newlist[i][1])
                    continue
            if(selllist[15]!=''): #判斷DIF與MACD的黃金交叉或死亡交叉
                if(newlist[i][15]==newlist[i][22]): #若相同則繼續判斷
                    if(selllist[15]=='1'): #黃金
                        DManswer=GD(results,newlist[i][1],newlist[i][22],newlist[i][15],22,15,0)
                        if(DManswer=='NO'):
                            totalday[2].append(newlist[i][1])
                            continue
                    elif(selllist[15]=='2'): #死亡
                        DManswer=GD(results,newlist[i][1],newlist[i][22],newlist[i][15],22,15,1)
                        if(DManswer=='NO'):
                            totalday[2].append(newlist[i][1])
                            continue
                else:
                    continue
            if(selllist[16]!=''): #判斷日RSI(6)
                RSIsix,consellday[4]=KD(selllist[16],selllist[17],consellday[4],newlist[i][12])
                if(RSIsix=="NO"):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(selllist[19]!=''): #判斷日RSI(9)
                RSInine,consellday[5]=KD(selllist[19],selllist[20],consellday[5],newlist[i][13])
                if(RSInine=="NO"):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(selllist[22]!=''): #判斷日RSI(12)
                RSItwelve,consellday[6]=KD(selllist[22],selllist[23],consellday[6],newlist[i][14])
                if(RSItwelve=="NO"):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(selllist[25]!=''): #判斷日RSI黃金交叉
                if(newlist[i][12]==newlist[i][14]): #交叉
                    ans=check(selllist[25],float(newlist[i][12]),float(newlist[i][14]))
                    if(ans=="YES"): 
                        KGanswer=GD(results,newlist[i][1],newlist[i][12],newlist[i][14],12,14,0)
                    else: continue      
                    if(KGanswer=="NO"):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue 
                    else: continue 
            if(selllist[26]!=''): #判斷日RSI死亡交叉    
                if(newlist[i][12]==newlist[i][14]): #交叉
                    ans=check(selllist[26],float(newlist[i][12]),float(newlist[i][14]))
                    if(ans=="YES"): 
                        KGanswer=GD(results,newlist[i][1],newlist[i][12],newlist[i][14],12,14,1)
                    else: continue      
                    if(KGanswer=="NO"):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue 
                    else: continue
            if(selllist[27]!=''):#判斷均價線黃金交叉
                ganswer=VALUE(results,newlist[i][1],newlist[i][16],newlist[i][18],newlist[i][20],16,18,20,selllist[27],0)
                if(ganswer=="NO"):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(selllist[28]!=''):#判斷均價線死亡交叉
                danswer=VALUE(results,newlist[i][1],newlist[i][16],newlist[i][18],newlist[i][20],16,18,20,selllist[28],1)
                if(danswer=="NO"):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(selllist[29]!=''):#判斷均量線黃金交叉
                ganswer=VALUE(results,newlist[i][1],newlist[i][17],newlist[i][19],newlist[i][21],17,19,21,selllist[29],0)
                if(ganswer=="NO"):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(selllist[30]!=''):#判斷均量線死亡交叉
                danswer=VALUE(results,newlist[i][1],newlist[i][17],newlist[i][19],newlist[i][21],17,19,21,selllist[30],1)
                if(danswer=="NO"):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(selllist[31]!=''):#判斷日賣壓比例
                if(selllist[31]=='>'):
                    if(float(newlist[i][24])<float(selllist[32]) or float(newlist[i][24])==float(selllist[32])):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue 
                elif(selllist[31]=='<'):
                    if(float(newlist[i][24])>float(selllist[32]) or float(newlist[i][24])==float(selllist[32])):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue
                elif(selllist[31]=='='):
                    if(float(newlist[i][24])<float(selllist[32]) or float(newlist[i][24])>float(selllist[32])):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue
            if(selllist[33]!=''):#判斷日MFI
                if(selllist[33]=='>'):
                    if(float(newlist[i][23])<float(selllist[34]) or float(newlist[i][23])==float(selllist[34])):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue 
                elif(selllist[33]=='<'):
                    if(float(newlist[i][23])>float(selllist[34]) or float(newlist[i][23])==float(selllist[34])):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue
                elif(selllist[33]=='='):
                    if(float(newlist[i][23])<float(selllist[34]) or float(newlist[i][23])>float(selllist[34])):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue    
            if(selllist[35]!='' and selllist[36]!=''): #判斷日波動率
                number1=0.01*int(selllist[35])
                number2=0.01*int(selllist[36])      
                if(float(newlist[i][25])<number1 or float(newlist[i][25])==number1 or float(newlist[i][25])>number2 or float(newlist[i][25])==number2):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(selllist[37]!=''): #日成交量
                if(selllist[38]=='1'): #增加
                    volumeanswer,consellday[7]=VOLUME(results,newlist[i][1],2,newlist[i][2],consellday[7],1)
                    if(volumeanswer=="NO"):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
                if(selllist[38]=='2'):  #減少
                    volumeanswer,conbuyday[7]=VOLUME(results,newlist[i][1],2,newlist[i][2],consellday[7],2)
                    if(volumeanswer=="NO"):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            #週成交判斷            
            if(weeknumber!=0):
                if(record[weeknumber]!=record[weeknumber-1]): #不同代表下週了!
                    weekcount+=1
            #找前一周
            if(selllist[39]!=''): #判斷週K
                WKanswer,consellday[8]=KD(selllist[39],selllist[40],consellday[8],recordweek[weekcount][10]) 
                if(WKanswer=='NO'):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(selllist[39]!=''): #判斷週D
                WDanswer,consellday[9]=KD(selllist[42],selllist[43],consellday[9],recordweek[weekcount][11]) 
                if(WDanswer=='NO'):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue   
            if(selllist[45] != ''): #判斷黃金交叉 
                if(recordweek[weekcount][10]==recordweek[weekcount][11]): #交叉
                    ans=check(selllist[45],float(recordweek[weekcount][10]),float(recordweek[weekcount][11]))
                    if(ans=="YES"): 
                        KGanswer=GD(weekresults,recordweek[weekcount][1],recordweek[weekcount][10],recordweek[weekcount][11],10,11,0)
                    else: continue      
                    if(KGanswer=="NO"):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue 
                else: continue
            if(selllist[46] != ''): #判斷死亡交叉 
                if(recordweek[weekcount][10]==recordweek[weekcount][11]): #交叉
                    ans=check(selllist[46],float(recordweek[weekcount][10]),float(recordweek[weekcount][11]))
                    if(ans=="YES"): 
                        KGanswer=GD(weekresults,recordweek[weekcount][1],recordweek[weekcount][10],recordweek[weekcount][11],10,11,1)
                    else: continue             
                    if(KGanswer=="NO"):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue 
                else: continue 
            if(selllist[47]!=''): #判斷週MACD
                WMACD,consellday[10]=KD(selllist[47],selllist[48],consellday[10],recordweek[weekcount][15]) 
                if(WMACD=='NO'):
                    totalday[2].append(newlist[i][1])
                    continue
            if(selllist[50]!=''): #判斷週DIF
                WDIF,consellday[11]=KD(selllist[50],selllist[51],consellday[11],recordweek[weekcount][22])
                if(WDIF=='NO'):
                    totalday[2].append(newlist[i][1])
                    continue
            if(selllist[53]!=''): #判斷週MACD落點
                Wpalceanswer=Place(selllist[53],recordweek[weekcount][15],recordweek[weekcount][22]) 
                if(Wpalceanswer=='NO'): #不成立
                    totalday[2].append(newlist[i][1])
                    continue
            if(selllist[54]!=''): #判斷DIF與MACD的黃金交叉或死亡交叉
                if(recordweek[weekcount][15]==recordweek[weekcount][22]): #若相同則繼續判斷
                    if(selllist[54]=='1'): #黃金
                        WManswer=GD(weekresults,recordweek[weekcount][1],recordweek[weekcount][22],recordweek[weekcount][15],22,15,0)
                        if(WManswer=='NO'):
                            totalday[2].append(newlist[i][1])
                            continue
                    elif(selllist[54]=='2'): #死亡
                        WManswer=GD(weekresults,recordweek[weekcount][1],recordweek[weekcount][22],recordweek[weekcount][15],22,15,1)
                        if(WManswer=='NO'):
                            totalday[2].append(newlist[i][1])
                            continue
                else:
                    continue
            if(selllist[55]!=''): #判斷週RSI(6)
                RSIsix,consellday[12]=KD(selllist[55],selllist[56],consellday[12],recordweek[weekcount][12])
                if(RSIsix=="NO"):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(selllist[58]!=''): #判斷週RSI(9)
                RSInine,consellday[13]=KD(selllist[58],selllist[59],consellday[13],recordweek[weekcount][13])
                if(RSInine=="NO"):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(selllist[61]!=''): #判斷週RSI(12)
                RSItwelve,consellday[14]=KD(selllist[61],selllist[62],consellday[14],recordweek[weekcount][14])
                if(RSItwelve=="NO"):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(selllist[64]!=''): #判斷週RSI黃金交叉
                if(recordweek[weekcount][12]==recordweek[weekcount][14]): #交叉
                    ans=check(selllist[64],float(recordweek[weekcount][12]),float(recordweek[weekcount][14]))
                    if(ans=="YES"): 
                        KGanswer=GD(weekresults,recordweek[weekcount][1],recordweek[weekcount][12],recordweek[weekcount][14],12,14,0)
                    else: continue      
                    if(KGanswer=="NO"):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue 
                    else: continue
            if(selllist[65]!=''): #判斷週RSI死亡交叉
                if(recordweek[weekcount][12]==recordweek[weekcount][14]): #交叉
                    ans=check(selllist[64],float(recordweek[weekcount][12]),float(recordweek[weekcount][14]))
                    if(ans=="YES"): 
                        KGanswer=GD(weekresults,recordweek[weekcount][1],recordweek[weekcount][12],recordweek[weekcount][14],12,14,1)
                    else: continue      
                    if(KGanswer=="NO"):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue 
                    else: continue
            if(selllist[66]!=''):#判斷均價線黃金交叉
                Wganswer=VALUE(weekresults,recordweek[weekcount][1],recordweek[weekcount][16],recordweek[weekcount][18],recordweek[weekcount][20],16,18,20,selllist[66],0)
                if(Wganswer=="NO"):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(selllist[67]!=''):#判斷均價線死亡交叉
                Wdanswer=VALUE(weekresults,recordweek[weekcount][1],recordweek[weekcount][16],recordweek[weekcount][18],recordweek[weekcount][20],16,18,20,selllist[67],1)
                if(Wdanswer=="NO"):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(selllist[68]!=''):#判斷均量線黃金交叉
                Wganswer=VALUE(weekresults,recordweek[weekcount][1],recordweek[weekcount][17],recordweek[weekcount][19],recordweek[weekcount][21],17,19,21,selllist[68],0)
                if(ganswer=="NO"):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(selllist[69]!=''):#判斷均量線死亡交叉
                Wdanswer=VALUE(weekresults,recordweek[weekcount][1],recordweek[weekcount][17],recordweek[weekcount][19],recordweek[weekcount][21],17,19,21,selllist[69],1)
                if(danswer=="NO"):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(selllist[70]!=''):#判斷週賣壓比例
                if(selllist[70]=='>'):
                    if(float(recordweek[weekcount][24])<float(selllist[71]) or float(recordweek[weekcount][24])==float(selllist[71])):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue 
                elif(selllist[70]=='<'):
                    if(float(recordweek[weekcount][24])>float(selllist[71]) or float(recordweek[weekcount][24])==float(selllist[71])):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue
                elif(selllist[70]=='='):
                    if(float(recordweek[weekcount][24])<float(selllist[71]) or float(recordweek[weekcount][24])>float(selllist[71])):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue
            if(selllist[72]!=''):#判斷週MFI
                if(selllist[72]=='>'):
                    if(float(recordweek[weekcount][23])<float(selllist[73]) or float(recordweek[weekcount][23])==float(selllist[73])):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue 
                elif(selllist[72]=='<'):
                    if(float(recordweek[weekcount][23])>float(selllist[73]) or float(recordweek[weekcount][23])==float(selllist[73])):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue
                elif(selllist[72]=='='):
                    if(float(recordweek[weekcount][23])<float(selllist[73]) or float(recordweek[weekcount][23])>float(selllist[73])):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue 
            if(selllist[74]!='' and selllist[75]!=''): #判斷週波動率
                number1=0.01*int(selllist[74])
                number2=0.01*int(selllist[75])      
                if(float(recordweek[weekcount][25])<number1 or float(recordweek[weekcount][25])==number1 or float(recordweek[weekcount][25])>number2 or float(recordweek[weekcount][25])==number2):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(buylist[76]!=''): #週成交量
                if(buylist[77]=='1'): #增加
                    Wvolumeanswer,consellday[15]=VOLUME(weekresults,recordweek[weekcount][1],2,recordweek[weekcount][2],consellday[15],1)
                    if(Wvolumeanswer=="NO"):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
                if(buylist[77]=='2'):  #減少
                    Wvolumeanswer,consellday[15]=VOLUME(weekresults,recordweek[weekcount][1],2,recordweek[weekcount][2],consellday[15],2)
                    if(Wvolumeanswer=="NO"):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            #月成交判斷
            if(weeknumber!=0):
                if(record[weeknumber]!=record[weeknumber-1]): #不同代表下個月了!
                    monthcount+=1
            if(selllist[78]!=''): #判斷月K
                MKanswer,consellday[16]=KD(selllist[78],selllist[79],consellday[16],recordmonth[monthcount][10]) 
                if(MKanswer=='NO'):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(selllist[81]!=''): #判斷月D
                MDanswer,consellday[17]=KD(selllist[81],selllist[82],consellday[17],recordmonth[monthcount][11]) 
                if(MDanswer=='NO'):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue  
            if(selllist[84] != ''): #判斷黃金交叉 
                if(recordmonth[monthcount][10]==recordmonth[monthcount][11]): #交叉
                    ans=check(selllist[84],float(recordmonth[monthcount][10]),float(recordmonth[monthcount][11]))
                    if(ans=="YES"): 
                        MGanswer=GD(monthresults,recordmonth[monthcount][1],recordmonth[monthcount][10],recordmonth[monthcount][11],10,11,0)
                    else: continue      
                    if(MGanswer=="NO"):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue 
                else: continue
            if(selllist[85] != ''): #判斷死亡交叉 
                if(recordmonth[monthcount][10]==recordmonth[monthcount][11]): #交叉
                    ans=check(selllist[85],float(recordmonth[monthcount][10]),float(recordmonth[monthcount][11]))
                    if(ans=="YES"): 
                        MGanswer=GD(monthresults,recordmonth[monthcount][1],recordmonth[monthcount][10],recordmonth[monthcount][11],10,11,1)
                    else: continue      
                    if(MGanswer=="NO"):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue 
                else: continue
            if(selllist[86]!=''): #判斷月MACD
                MMACD,consellday[18]=KD(selllist[86],selllist[87],consellday[18],recordmonth[monthcount][15]) 
                if(MMACD=='NO'):
                    totalday[2].append(newlist[i][1])
                    continue
            if(selllist[89]!=''): #判斷週DIF
                MDIF,consellday[19]=KD(selllist[89],selllist[90],consellday[19],recordmonth[monthcount][22])
                if(MDIF=='NO'):
                    totalday[2].append(newlist[i][1])
                    continue
            if(selllist[92]!=''): #判斷月MACD落點
                Mpalceanswer=Place(selllist[92],recordmonth[monthcount][15],recordmonth[monthcount][22]) 
                if(Mpalceanswer=='NO'): #不成立
                    totalday[2].append(newlist[i][1])
                    continue
            if(selllist[93]!=''): #判斷DIF與MACD的黃金交叉或死亡交叉
                if(recordmonth[monthcount][15]==recordmonth[monthcount][22]): #若相同則繼續判斷
                    if(selllist[93]=='1'): #黃金
                        MManswer=GD(monthresults,recordmonth[monthcount][1],recordmonth[monthcount][22],recordmonth[monthcount][15],22,15,0)
                        if(MManswer=='NO'):
                            totalday[2].append(newlist[i][1])
                            continue
                    elif(selllist[93]=='2'): #死亡
                        MManswer=GD(monthresults,recordmonth[monthcount][1],recordmonth[monthcount][22],recordmonth[monthcount][15],22,15,1)
                        if(MManswer=='NO'):
                            totalday[2].append(newlist[i][1])
                            continue
                else: continue
            if(selllist[94]!=''): #判斷月RSI(6)
                RSIsix,consellday[20]=KD(selllist[94],selllist[95],consellday[20],recordmonth[monthcount][20])
                if(RSIsix=="NO"):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(selllist[97]!=''): #判斷月RSI(9)
                RSInine,consellday[21]=KD(selllist[97],selllist[98],consellday[21],recordmonth[monthcount][13])
                if(RSInine=="NO"):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(selllist[100]!=''): #判斷月RSI(12)
                RSItwelve,consellday[22]=KD(selllist[100],selllist[101],consellday[22],recordmonth[monthcount][14])
                if(RSItwelve=="NO"):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(selllist[103]!=''): #判斷月RSI黃金交叉
                if(recordmonth[monthcount][12]==recordmonth[monthcount][14]): #交叉
                    ans=check(buylist[103],float(recordmonth[monthcount][12]),float(recordmonth[monthcount][14]))
                    if(ans=="YES"): 
                        KGanswer=GD(monthresults,recordmonth[monthcount][1],recordmonth[monthcount][12],recordmonth[monthcount][14],12,14,0)
                    else: continue      
                    if(KGanswer=="NO"):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue 
                    else: continue
            if(selllist[104]!=''): #判斷月RSI死亡交叉
                if(recordmonth[monthcount][12]==recordmonth[monthcount][14]): #交叉
                    ans=check(selllist[104],float(recordmonth[monthcount][12]),float(recordmonth[monthcount][14]))
                    if(ans=="YES"): 
                        KGanswer=GD(monthresults,recordmonth[monthcount][1],recordmonth[monthcount][12],recordmonth[monthcount][14],12,14,1)
                    else: continue      
                    if(KGanswer=="NO"):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue 
                    else: continue
            if(selllist[105]!=''):#判斷均價線黃金交叉
                Wganswer=VALUE(monthresults,recordmonth[monthcount][1],recordmonth[monthcount][16],recordmonth[monthcount][18],recordmonth[monthcount][20],16,18,20,selllist[105],0)
                if(Wganswer=="NO"):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(selllist[106]!=''):#判斷均價線死亡交叉
                Wdanswer=VALUE(monthresults,recordmonth[monthcount][1],recordmonth[monthcount][16],recordmonth[monthcount][18],recordmonth[monthcount][20],16,18,20,selllist[106],1)
                if(Wdanswer=="NO"):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(selllist[107]!=''):#判斷均量線黃金交叉
                Wganswer=VALUE(monthresults,recordmonth[monthcount][1],recordmonth[monthcount][17],recordmonth[monthcount][19],recordmonth[monthcount][21],17,19,21,selllist[107],0)
                if(ganswer=="NO"):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(selllist[108]!=''):#判斷均量線死亡交叉
                Wdanswer=VALUE(monthresults,recordmonth[monthcount][1],recordmonth[monthcount][17],recordmonth[monthcount][19],recordmonth[monthcount][21],17,19,21,selllist[108],1)
                if(danswer=="NO"):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(selllist[109]!=''):#判斷月賣壓比例
                if(selllist[109]=='>'):
                    if(float(recordmonth[monthcount][24])<float(selllist[110]) or float(recordmonth[monthcount][24])==float(selllist[110])):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue 
                elif(selllist[109]=='<'):
                    if(float(recordmonth[monthcount][24])>float(selllist[110]) or float(recordmonth[monthcount][24])==float(selllist[110])):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue
                elif(selllist[109]=='='):
                    if(float(recordmonth[monthcount][24])<float(selllist[110]) or float(recordmonth[monthcount][24])>float(selllist[110])):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue
            if(selllist[111]!=''):#判斷月MFI
                if(selllist[111]=='>'):
                    if(float(recordmonth[monthcount][23])<float(selllist[112]) or float(recordmonth[monthcount][23])==float(selllist[112])):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue 
                elif(selllist[111]=='<'):
                    if(float(recordmonth[monthcount][23])>float(selllist[112]) or float(recordmonth[monthcount][23])==float(selllist[112])):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue
                elif(selllist[111]=='='):
                    if(float(recordmonth[monthcount][23])<float(selllist[112]) or float(recordmonth[monthcount][23])>float(selllist[112])):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                        continue
            if(selllist[113]!='' and selllist[114]!=''): #判斷月波動率
                number1=0.01*int(buylist[113])
                number2=0.01*int(buylist[114])      
                if(float(recordmonth[monthcount][25])<number1 or float(recordmonth[monthcount][25])==number1 or float(recordmonth[monthcount][25])>number2 or float(recordmonth[monthcount][25])==number2):
                    totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            if(selllist[115]!=''): #月成交量
                if(selllist[116]==1): #增加
                    Wvolumeanswer,consellday[23]=VOLUME(monthresults,recordmonth[monthcount][1],2,recordmonth[monthcount][2],consellday[23],1)
                    if(Wvolumeanswer=="NO"):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
                if(selllist[116]==2):  #減少
                    Wvolumeanswer,consellday[23]=VOLUME(monthresults,recordmonth[monthcount][1],2,recordmonth[monthcount][2],consellday[23],2)
                    if(Wvolumeanswer=="NO"):
                        totalday[2].append(newlist[i][1]) #輸入未交易
                    continue
            for j in range(len(consellday)):
                if(selldaysmemory[j]!=''): 
                    if(consellday[j]==int(selldaysmemory[j])):     
                        if(j==(len(consellday)-1)):
                            count=0 #代表賣了
                            weekcount=0
                            monthcount=0
                            for r in range(len(consellday)):
                                consellday[r]=0
                            totalday[1].append(newlist[i][1])
                            buymoney.append(newlist[i][7]) #紀錄收盤價
                            break
                        else:
                            continue
                    else:
                        totalday[2].append(newlist[i][1]) 
                        break
                else: #不成立
                    continue
            
    return totalday,buymoney,count
def KD(operator,value,days,getvalue):
    if(operator=='>'):
        if(float(getvalue)>float(value)):
            days+=1
            return "OK",days
        else:
            return "NO",0
    elif(operator=='<'):
        if(float(getvalue) < float(value)):
            days+=1
            return "OK",days
        else:
            return "NO",0
    elif(operator=='='):
        if(float(getvalue)==float(value)):
            days+=1
            return "OK",days
        else:
            return "NO",0
def GD(results,newlistvalue,value1,value2,number1,number2,key):#資料list、要確認的日期、要確認的值
    for i in range(len(results)):
        if(newlistvalue==results[i][1]):
            temp1=results[i-1][number1] #找前一天的值
            temp2=results[i-1][number2] #找前一天的值
            break
    if(key==0): #要檢查黃金交叉
        if(temp1<temp2 and temp1<value1 and temp2<value2):
            return "YES"
        else:
            return "NO"
    elif(key==1): #要檢查死亡交叉
        if(temp1>temp2 and temp1>value1 and temp2>value2):
            return "YES"
        else:
            return "NO"
def Place(operator,MACDvalue,DIFvalue):
    if(operator=='>'):
        if(float(MACDvalue)>0 and float(DIFvalue)>0):
            return "OK"
        else:
            return "NO"
    elif(operator=='<'):
        if(float(MACDvalue)<0 and float(DIFvalue)<0):
            return "OK"
        else:
            return "NO"
    elif(operator=='='):
        if(float(MACDvalue)==0.0 and float(DIFvalue)==0.0):
            return "OK"
        else:
            return "NO"
def VOLUME(results,valuedate,number,value,days,key):
    for i in range(len(results)):
        if(valuedate==results[i][1]):
            temp1=results[i-1][number] #找前一天的值
            break
    if(key==1): #增加
        if(float(value)>temp1):
            days+=1
            return "OK",days
        else:
            return "NO",0
    if(key==2): #減少
        if(float(value)<temp1):
            days+=1
            return "OK",days
        else:
            return "NO",0
def RSIGD(results,newlistvalue,RSIsvalue,RSItvalue,key):
    for i in range(len(results)):
        if(newlistvalue==results[i][1]):
            temp1=results[i-1][12] #找前一天的RSI(6)
            temp2=results[i-1][14] #找前一天的RSI(12)
            break
    if(key==0): #要檢查黃金交叉
        if(temp1<temp2 and temp1<RSIsvalue and temp2<RSItvalue):
            return "YES"
        else:
            return "NO"
    elif(key==1): #要檢查死亡交叉
        if(temp1>temp2 and temp1>RSIsvalue and temp2>RSItvalue):
            return "YES"
        else:
            return "NO"
def VALUE(results,newlistvalue,number5,number20,number60,value5,value20,value60,key,gd):
    for i in range(len(results)):
        if(newlistvalue==results[i][1]):
            temp1=results[i-1][value5] #找前一天的成交價/量均值(5)
            temp2=results[i-1][value20] #找前一天的成交價/量均值(20)
            temp3=results[i-1][value60] #找前一天的成交價/量均值(60)
            break
    if(key=='1' and number5==number20): #5/20
        if(gd==0): #黃金
            if(temp1<temp2 and temp1<number5 and temp2<number20):
                return "YES"
            else:
                return "NO"
        else:      #死亡
            if(temp1>temp2 and temp1>number5 and temp2>number20):
                return "YES"
            else:
                return "NO"
    else:
        return "NO"
    if(key=='2' and number5==number60): #5/60
        if(gd==0): #黃金
            if(temp1<temp3 and temp1<number5 and temp3<number60):
                return "YES"
            else:
                return "NO"
        else:      #死亡
            if(temp1>temp3 and temp1>number5 and temp3>number60):
                return "YES"
            else:
                return "NO"
    else:
        return "NO" 
    if(key=='3' and number20==number60): #20/60
        if(gd==0): #黃金
            if(temp2<temp3 and temp2<number20 and temp3<number60):
                return "YES"
            else:
                return "NO"
        else:      #死亡
            if(temp2>temp3 and temp2>number20 and temp3>number60):
                return "YES"
            else:
                return "NO" 
    else:
        return "NO"
def check(number,value1,value2):
    if(int(number)==1): #黃金
        return "YES"
    elif(int(number)==2):#小於20
        if(value1<20 and value2<20):
            return "YES"
    elif(int(number)==3):#20~50
        if(value1>20 and value2>20 and value1<50 and value2<50):      
            return "YES"       
    elif(int(number)==4):#50~80
        if(value1>50 and value2>50 and value1<80 and value2<80):      
            return "YES"
    elif(int(number)==5):#大於80
        if(value1>80 and value2>80):      
            return "YES"                 
    else:
        return "NO"     






buylist=['>','20','1','','','','','','<','1','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','>','-1','1','','','','','','','','','','','','','','','','','','','','','','','','','']
selllist=['>','30','3','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','2','1','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','']
datelist=[2020,6,30,2020,8,20]
ssid=1101


(daterecord,moneylist,count)=historytest(buylist,selllist,datelist,ssid)
money=0
if(len(moneylist)==1):
    money=0
else:
    for i in range(1,len(moneylist)-1,2):
        money=money+float(moneylist[i])-float(moneylist[i-1])
if(count==0):
    print("目前無持股")
else:
    print("目前有持股")

print("報酬:",money)
print("買入日期:")
for i in range(len(daterecord[0])):
    print(daterecord[0][i])
print("賣出日期:")
for i in range(len(daterecord[1])):
    print(daterecord[1][i])
print("未交易日期:")
for i in range(len(daterecord[2])):
    print(daterecord[2][i])


