import pandas as pd
import csv
import os

def CalculateMFI(day=14):
    #Calculate TP
    TP = []
    for i in range(1, len(data)):
        if data[i][5]=='--' or data[i][6]=='--' or data[i][7]=='--':
            TP.append("#")
        else:
            TP.append((float(data[i][5].replace(",", ""))+float(data[i][6].replace(",", ""))+float(data[i][7].replace(",", "")))/3)

    #Calculate RMF
    RMF = []
    for i in range(0, len(TP)):
        if TP[i]=="#":
            RMF.append("#")
        else:
            RMF.append(TP[i]*float(data[i+1][2].replace(",", "")))

    #Calculate PMF
    PMF = ['#']
    for i in range(1, len(TP)):
        if TP[i]=="#" or TP[i-1]=='#':
            PMF.append("#")
        else:
            if TP[i]>TP[i-1]:
                PMF.append(RMF[i])
            else:
                PMF.append(0)

    #Calculate NMF
    NMF = ['#']
    for i in range(1, len(TP)):
        if TP[i]=="#" or TP[i-1]=='#':
            NMF.append("#")
        else:
            if TP[i]<=TP[i-1]:
                NMF.append(RMF[i])
            else:
                NMF.append(0)

    #Calculate MFR
    MFR = ['#']*day
    for i in range(day, len(PMF)):
        period14_PMF = 0
        period14_NMF = 0
        for j in range(i-day+1, i+1):
            if PMF[j]=='#' or NMF[j]=='#':
                period14_PMF = -1
                period14_NMF = -1
                break
            else:
                period14_PMF = period14_PMF+PMF[j]
                period14_NMF = period14_NMF+NMF[j]
        if (period14_PMF==-1 and period14_NMF==-1) or period14_NMF==0:
            MFR.append("#")
        else:
            MFR.append(period14_PMF/period14_NMF)

    #Calculate MFI
    MFI = []
    for i in range(0, len(MFR)):
        if MFR[i]=='#':
            MFI.append('#')
        else:
            MFI.append(100-(100/(1+MFR[i])))
    return MFI

def CalculateKD(day=9):
    #Calculate RSV
    RSV = ['#']*(day-1)
    for i in range(day, len(data)):
        low_min = 10000
        high_min = -10000
        for j in range(i-day+1, i+1):
            if data[j][5] == '--' or data[j][6] == '--':
                continue
            if float(data[j][6].replace(',','')) < low_min:
                low_min = float(data[j][6].replace(',',''))
            if float(data[j][5].replace(',','')) > high_min:
                high_min = float(data[j][5].replace(',',''))
        if data[i][7] == '--' or high_min-low_min == 0:
            RSV.append('#')
        else:
            RSV.append((float(data[i][7].replace(',','')) - low_min) / (high_min - low_min) * 100)

    #Calculate KD
    K = []
    D = []
    for i in range(0, len(RSV)):
        if RSV[i]=='#':
            K.append(50)
            D.append(50)
        else:
            K.append(2.0/3.0*K[len(K)-1]+1.0/3.0*RSV[i])
            D.append(2.0/3.0*D[len(D)-1]+1.0/3.0*K[i])
    return K, D

def CalculateRSI(day=9):
    #Calculate RSI
    RSI = ['#']*day
    for i in range(day+1, len(data)):
        up = 0.0
        down = 0.0
        for j in range(i-day+1, i+1):
            if data[j][7] == '--' or data[j-1][7] == '--':
                continue
            elif float(data[j][7].replace(',','')) > float(data[j-1][7].replace(',','')):
                up = up + float(data[j][7].replace(',','')) - float(data[j-1][7].replace(',',''))
            else:
                down = down + float(data[j-1][7].replace(',','')) - float(data[j][7].replace(',',''))
        up = up / day
        down = down / day
        if up+down != 0:
            RSI.append(up/(up+down)*100)
        else:
            RSI.append('#')
    return RSI

def CalculateDIFAndMACD(day1=12, day2=26, day3=9):
    #Calculate EMA day1
    EMA12 = ['#']*(day1-1)
    DI = 0.0
    for i in range(1, day1+1 if day1+1 < len(data) else len(data)):
        di = 0.0
        if data[i][5] != '--':
            di = di+(float(data[i][5].replace(',','')))
        if data[i][6] != '--':
            di = di+(float(data[i][6].replace(',','')))
        if data[i][7] != '--':
            di = di+2*(float(data[i][7].replace(',','')))
        di = di/4
        DI = DI+di
    EMA12.append(DI/day1)
    for i in range(day1+1, len(data)):
        if data[i][7] == '--':
            EMA12.append(EMA12[len(EMA12)-1])
        else:
            EMA12.append((EMA12[len(EMA12)-1]*(day1-1)+float(data[i][7].replace(',',''))*2)/(day1+1))
    #Calculate EMA day2
    EMA26 = ['#']*(day2-1)
    DI = 0.0
    for i in range(1, day2+1 if day2+1 < len(data) else len(data)):
        di = 0.0
        if data[i][5] != '--':
            di = di+(float(data[i][5].replace(',','')))
        if data[i][6] != '--':
            di = di+(float(data[i][6].replace(',','')))
        if data[i][7] != '--':
            di = di+2*(float(data[i][7].replace(',','')))
        di = di/4
        DI = DI+di
    EMA26.append(DI/day2)
    for i in range(day2+1, len(data)):
        if data[i][7] == '--':
            EMA26.append(EMA26[len(EMA26)-1])
        else:
            EMA26.append((EMA26[len(EMA26)-1]*(day2-1)+float(data[i][7].replace(',',''))*2)/(day2+1))

    #Calculate DIF
    DIF = []
    for i in range(0, len(EMA12)):
        if EMA12[i]=='#' or EMA26[i]=='#':
            DIF.append('#')
        else:
            DIF.append(EMA12[i]-EMA26[i])

    #Calculate MACD
    MACD = ['#']*(day2+day3-1)
    FirstMACD = 0.0
    for i in range(day2-1, day2+day3 if day2+day3 < len(DIF) else len(DIF)):
        FirstMACD = FirstMACD + DIF[i]
    FirstMACD = FirstMACD/day3
    MACD.append(FirstMACD)
    for i in range(day2+day3, len(DIF)):
        MACD.append(MACD[len(MACD)-1]+2/(1+day3)*(DIF[i]-MACD[len(MACD)-1]))
    return DIF, MACD

# file list
files = os.listdir("C:\\Users\\happy\\Desktop\\stock")
for file in files:
    # open csv file
    if file[0:4]!="twse":
        continue
    with open(file, newline='', encoding="UTF-8") as csvfile:

        # read csv file
        rows = csv.reader(csvfile)

        #transform into list
        data = list(rows)

        #Calculate Index
        MFI = CalculateMFI()
        K, D = CalculateKD()
        RSI = CalculateRSI()
        DIF, MACD = CalculateDIFAndMACD()
        while len(MFI) > len(data)-1:
            MFI.pop(0)
        while len(K) > len(data)-1:
            K.pop(0)
        while len(D) > len(data)-1:
            D.pop(0)
        while len(RSI) > len(data)-1:
            RSI.pop(0)
        while len(DIF) > len(data)-1:
            DIF.pop(0)
        while len(MACD) > len(data)-1:
            MACD.pop(0) """有些資料筆數較少，這段程式碼是為了平衡各個指標的數量"""

        #Write to File
        name = file[-8:-4]
        dict = {'MFI':MFI, 'K':K, 'D':D, 'RSI':RSI, 'DIF':DIF, 'MACD':MACD}
        df = pd.DataFrame(dict)
        df.to_csv(name+'.csv')
