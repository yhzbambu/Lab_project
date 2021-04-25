#! /usr/bin/python
# coding=utf-8
from time import sleep
def Filter(submit):
    import pymysql
    db=pymysql.connect(
        host='163.18.104.164',
        user='bambu',
        password='test123',
        database="stock",
        port=3306
    )
    cursor=db.cursor()
    

    sqls=[]
    # __________________________________
    
    for I  in submit:
        # 處理顯示結果
        if I[0] =='T0' and I[1]=='New':
            sqls.append(
                "(SELECT stock.sid,stock.s_name,DayStockInformation.TradeDate,DayStockInformation.OpeningPrice,DayStockInformation.HighestPrice,DayStockInformation.LowestPrice,DayStockInformation.ClosingPrice,DayStockInformation.Change_,DayStockInformation.Transation_ FROM DayStockInformation,stock WHERE TradeDate='{0[2]}' and stock.sid=DayStockInformation.sid) ".format(I)
            )
        if I[0] =='T0' and I[1]=='RSI':
            sqls.append(
                "(SELECT stock.sid,stock.s_name,WeekStockInformation.RSI6,WeekStockInformation.RSI9,WeekStockInformation.RSI12 FROM  WeekStockInformation,stock WHERE TradingWeek='{0[3]}' and stock.sid=WeekStockInformation.sid) as T0_1 INNER JOIN (SELECT stock.sid,stock.s_name,MonthStockInformation.RSI6,MonthStockInformation.RSI9,MonthStockInformation.RSI12 FROM  MonthStockInformation,stock WHERE TradingMonth='{0[4]}' and stock.sid=MonthStockInformation.sid) as T0_2 INNER JOIN (SELECT stock.sid,stock.s_name,DayStockInformation.TradeDate,DayStockInformation.ClosingPrice,DayStockInformation.Change_,DayStockInformation.RSI6,DayStockInformation.RSI9,DayStockInformation.RSI12 FROM DayStockInformation,stock WHERE TradeDate='{0[2]}' and stock.sid=DayStockInformation.sid)  ".format(I)
            )
        if I[0] =='T0' and I[1]=='KD':
            sqls.append(
                "(SELECT stock.sid,stock.s_name,WeekStockInformation.K9_,WeekStockInformation.D9 FROM  WeekStockInformation,stock WHERE TradingWeek='{0[3]}' and stock.sid=WeekStockInformation.sid) as T0_1 INNER JOIN (SELECT stock.sid,stock.s_name,MonthStockInformation.K9_,MonthStockInformation.D9 FROM  MonthStockInformation,stock WHERE TradingMonth='{0[4]}' and stock.sid=MonthStockInformation.sid) as T0_2 INNER JOIN (SELECT stock.sid,stock.s_name,DayStockInformation.TradeDate,DayStockInformation.ClosingPrice,DayStockInformation.Change_,DayStockInformation.K9_,DayStockInformation.D9 FROM DayStockInformation,stock WHERE TradeDate='{0[2]}' and stock.sid=DayStockInformation.sid)  ".format(I)
            )
            # 
        if I[0] =='T0' and I[1] =='institutional_investors':

            sqls.append(
                "(SELECT stock.sid,stock.s_name,DayStockInformation.TradeDate,DayStockInformation.ClosingPrice,institutional_investors.sumForeignNoDealer,institutional_investors.sumForeignWithDealer,institutional_investors.sumING,institutional_investors.sumDealerBySelf,institutional_investors.sumDealerHedging,institutional_investors.Sum FROM institutional_investors,stock,DayStockInformation WHERE DayStockInformation.TradeDate='{0[2]}' and  institutional_investors.TradeDate='{0[2]}' and institutional_investors.TradeDate=DayStockInformation.TradeDate and stock.sid=institutional_investors.sid and stock.sid=DayStockInformation.sid) ".format(I)
            )
        else:
            # 表日期
            if len(I)<=6 or (I[0]=='T13' or I[0]=='T14' or I[0]=='T15'):
                if I[1]=='DayStockInformation':
                    Day="TradeDate='{0[5]}'".format(I)
                if  I[1]=='MarginPurchase_ShortSale':
                    Day="TradeDate='{0[5]}'".format(I)
                if  I[1]=='institutional_investors':
                    Day="TradeDate='{0[5]}'".format(I)
                if  I[1]=='MonthlyRevenue':
                    Day="Month='{0[5]}'".format(I)
                if  I[1]=='SeasonalChart':
                    Day="Quarterly='{0[5]}'".format(I)
                if  I[1]=='EntitlementSchedule':
                    Day="DividendPaymentYear='{0[5]}'".format(I)
                if  I[1]=='OperatingPerformance':
                    Day="Quarterly='{0[5]}'".format(I)
                if  I[1]=='WeekStockInformation':
                    Day="TradingWeek='{0[5]}'".format(I)
                if  I[1]=='MonthStockInformation':
                    Day="TradingMonth='{0[5]}'".format(I)
            if len(I)==7:
                if I[1]=='DayStockInformation':
                    Day="TradeDate='{0[6]}'".format(I)
                if  I[1]=='WeekStockInformation':
                    Day="TradingWeek='{0[6]}'".format(I)
                if  I[1]=='MonthStockInformation':
                    Day="TradingMonth='{0[6]}'".format(I)
            if len(I)>12 and I[8]=='DayStockInformation':
                Day2="TradeDate='{0[12]}'".format(I)
            # ['T13','DayStockInformation','HighestPrice','1','2','2021-03-29','>','CT13','DayStockInformation','K9_','1','2','2023-01-29'],
            # 處理條件一到六
            if I[0] =='T1' or I[0] =='T2' or I[0] =='T3' or I[0] =='T4' or I[0] =='T5' or I[0] =='T6':
                if '.' in I[4][0]:
                    sqls.append(
                        """(SELECT sid,{0[2]} FROM {0[1]} WHERE CONVERT(REPLACE({0[2]},',',''),DECIMAL(9,2)) {0[3]} BETWEEN CONVERT(REPLACE('{0[4][0]}',',',''),DECIMAL(9,2)) AND CONVERT(REPLACE('{0[4][1]}',',',''),DECIMAL(9,2)) AND {1})""".format(I,Day)
                        ) 
                else:
                    sqls.append(
                        """(SELECT sid,{0[2]} FROM {0[1]} WHERE REPLACE({0[2]},',','') {0[3]} BETWEEN CONVERT(REPLACE('{0[4][0]}',',',''),SIGNED) AND CONVERT(REPLACE('{0[4][1]}',',',''),SIGNED)  AND {1})""".format(I,Day)
                        )
            # 處理特殊篩選7~9
            if I[0] =='T7' or   I[0] =='T8' or  I[0] =='T9':
                if I[1] == 'classification':
                    sqls.append(
                        "(SELECT {0[2]} FROM {0[1]} WHERE {0[2]}{0[3]}='{0[4]}') AS {0[1]} INNER JOIN (SELECT * FROM stock )".format(I)
                    )
                # 落點
                if (I[1] == 'DayStockInformation' or  I[1] =='WeekStockInformation' or I[1] =='MonthStockInformation') and I[2]!='MACD9':
                    
                    sqls.append(
                        """(SELECT sid,{0[2]} FROM {0[1]} WHERE CONVERT(REPLACE({0[2]},',',''),DECIMAL(9,2)) {0[3]} BETWEEN CONVERT(REPLACE('{0[4][0]}',',',''),SIGNED) AND CONVERT(REPLACE('{0[4][1]}',',',''),SIGNED)  AND {1})""".format(I,Day)
                    )
                # MACD落點
                if I[2]=='MACD9' and (I[1] == 'DayStockInformation' or  I[1] =='WeekStockInformation' or I[1] =='MonthStockInformation'):
                    sqls.append(
                        """(SELECT sid,{0[2]},{0[3]} FROM {0[1]} WHERE CONVERT(REPLACE({0[2]},',',''),DECIMAL(9,2)) {0[4]} BETWEEN CONVERT(REPLACE('{0[5][0]}',',',''),SIGNED) AND CONVERT(REPLACE('{0[5][1]}',',',''),SIGNED) AND CONVERT(REPLACE({0[3]},',',''),DECIMAL(9,2)) {0[4]} BETWEEN CONVERT(REPLACE('{0[5][0]}',',',''),SIGNED) AND CONVERT(REPLACE('{0[5][1]}',',',''),SIGNED)  AND {1}) """.format(I,Day)
                    )
                # 黃金交叉
                if I[1] == 'KDGoldenCross' or I[1]=='RSIGoldenCross':
                    if I[4]=='DayStockInformation':
                        extra=" and CONVERT(REPLACE({0[2]},',',''),DECIMAL(9,2))  CONVERT(REPLACE({0[8][0]},',',''),DECIMAL(9,2)) AND CONVERT(REPLACE({0[2]},',',''),DECIMAL(9,2)))".format(I)
                        
                        sqls.append(
                            "(SELECT sid,{0[2]},{0[3]} FROM {0[4]} WHERE {0[9]} {0[2]}<{0[3]} and TradeDate='{0[6]}' {1}) AS {0[5]} INNER JOIN (SELECT sid,{0[2]},{0[3]} FROM {0[4]} WHERE {0[9]} {0[2]}>{0[3]} and TradeDate='{0[7]}' {1})".format(I,extra)
                        )
                    if I[4]=='WeekStockInformation':
                        extra=" and CONVERT(REPLACE({0[2]},',',''),DECIMAL(9,2))  CONVERT(REPLACE({0[8][0]},',',''),DECIMAL(9,2)) AND CONVERT(REPLACE({0[2]},',',''),DECIMAL(9,2)))".format(I)
                        
                        sqls.append(
                            "(SELECT sid,{0[2]},{0[3]} FROM {0[4]} WHERE {0[9]} {0[2]}<{0[3]} and  TradingWeek='{0[6]}' {1}) AS {0[5]} INNER JOIN (SELECT sid,{0[2]},{0[3]} FROM {0[4]} WHERE {0[9]} {0[2]}>{0[3]} and TradingWeek='{0[7]}' {1})".format(I,extra)
                        )
                    if I[4]=='MonthStockInformation':
                        extra=" and CONVERT(REPLACE({0[2]},',',''),DECIMAL(9,2))  CONVERT(REPLACE({0[8][0]},',',''),DECIMAL(9,2)) AND CONVERT(REPLACE({0[2]},',',''),DECIMAL(9,2)))".format(I)
                
                        sqls.append(
                            "(SELECT sid,{0[2]},{0[3]} FROM {0[4]} WHERE {0[9]} {0[2]}<{0[3]} and TradingMonth='{0[6]}' {1}) AS {0[5]} INNER JOIN (SELECT sid,{0[2]},{0[3]} FROM {0[4]} WHERE {0[9]} {0[2]}>{0[3]} and TradingMonth='{0[7]}' {1})".format(I,extra)
                        )
                # 死亡交叉
                if I[1] == 'KDGDeathCross' or I[1]=='RSIDeathCross':
                    if I[4]=='DayStockInformation':
                        extra=" and CONVERT(REPLACE({0[2]},',',''),DECIMAL(9,2))  CONVERT(REPLACE({0[8][0]},',',''),DECIMAL(9,2)) AND CONVERT(REPLACE({0[2]},',',''),DECIMAL(9,2)))".format(I)
                        
                        sqls.append(
                            "(SELECT sid,{0[2]},{0[3]} FROM {0[4]} WHERE  {0[9]} {0[2]}>{0[3]} and TradeDate='{0[6]}' {1}) AS {0[5]} INNER JOIN (SELECT sid,{0[2]},{0[3]} FROM {0[4]} WHERE {0[9]} {0[2]}<{0[3]} and TradeDate='{0[7]}' {1})".format(I,extra)
                        )
                    if I[4]=='WeekStockInformation':
                        extra=" and CONVERT(REPLACE({0[2]},',',''),DECIMAL(9,2))  CONVERT(REPLACE({0[8][0]},',',''),DECIMAL(9,2)) AND CONVERT(REPLACE({0[2]},',',''),DECIMAL(9,2)))".format(I)
                    
                        sqls.append(
                            "(SELECT sid,{0[2]},{0[3]} FROM {0[4]} WHERE {0[9]} {0[2]}>{0[3]} and  TradingWeek='{0[6]}' {1}) AS {0[5]} INNER JOIN (SELECT sid,{0[2]},{0[3]} FROM {0[4]} WHERE {0[9]} {0[2]}<{0[3]} and TradingWeek='{0[7]}' {1})".format(I,extra)
                        )
                    if I[4]=='MonthStockInformation':
                        extra=" and CONVERT(REPLACE({0[2]},',',''),DECIMAL(9,2))  CONVERT(REPLACE({0[8][0]},',',''),DECIMAL(9,2)) AND CONVERT(REPLACE({0[2]},',',''),DECIMAL(9,2)))".format(I)
                        
                        sqls.append(
                            "(SELECT sid,{0[2]},{0[3]} FROM {0[4]} WHERE  {0[9]} {0[2]}>{0[3]} and TradingMonth='{0[6]}' {1}) AS {0[5]} INNER JOIN (SELECT sid,{0[2]},{0[3]} FROM {0[4]} WHERE {0[9]} {0[2]}<{0[3]} and TradingMonth='{0[7]}' {1})".format(I,extra)
                        )
                # 向上突破
                if I[1]=='Breakupward':
                    if I[4]=='DayStockInformation':
                        extra=" and REPLACE({0[3]},',','')  CONVERT(REPLACE({0[8][0]},',',''),DECIMAL(9,2)) AND CONVERT(REPLACE({0[2]},',',''),DECIMAL(9,2)))".format(I)
                
                        sqls.append(
                            "(SELECT sid,{0[2]},{0[3]} FROM {0[4]} WHERE {0[9]} {0[2]}<{0[3]} and  TradeDate='{0[6]}') AS {0[5]} INNER JOIN (SELECT sid,{0[2]},{0[3]} FROM {0[4]} WHERE {0[9]} {0[2]}>{0[3]} and TradeDate='{0[7]}')".format(I)
                        )
                    if I[4]=='WeekStockInformation':
                        extra=" and REPLACE({0[3]},',','')  CONVERT(REPLACE({0[8][0]},',',''),DECIMAL(9,2)) AND CONVERT(REPLACE({0[2]},',',''),DECIMAL(9,2)))".format(I)
                
                        sqls.append(
                            "(SELECT sid,{0[2]},{0[3]} FROM {0[4]} WHERE {0[9]} {0[2]}<{0[3]} and  TradingWeek='{0[6]}') AS {0[5]} INNER JOIN (SELECT sid,{0[2]},{0[3]} FROM {0[4]} WHERE {0[9]} {0[2]}>{0[3]} and TradingWeek='{0[7]}')".format(I)
                        ) 
                    if I[4]=='MonthStockInformation':
                        extra=" and REPLACE({0[3]},',','')  CONVERT(REPLACE({0[8][0]},',',''),DECIMAL(9,2)) AND CONVERT(REPLACE({0[2]},',',''),DECIMAL(9,2)))".format(I)
        
                        sqls.append(
                            "(SELECT sid,{0[2]},{0[3]} FROM {0[4]} WHERE {0[9]} {0[2]}<{0[3]} and  TradingMonth='{0[6]}') AS {0[5]} INNER JOIN (SELECT sid,{0[2]},{0[3]} FROM {0[4]} WHERE {0[9]} {0[2]}>{0[3]} and TradingMonth='{0[7]}')".format(I)
                        ) 
                # 向下突破
                if I[1]=='Downwardbreak':
                    if I[4]=='DayStockInformation':
                        extra=" and REPLACE({0[3]},',','')  CONVERT(REPLACE({0[8][0]},',',''),DECIMAL(9,2)) AND CONVERT(REPLACE({0[2]},',',''),DECIMAL(9,2)))".format(I)
                
                        sqls.append(
                            "(SELECT sid,{0[2]},{0[3]} FROM {0[4]} WHERE {0[9]} {0[2]}>{0[3]} and  TradeDate='{0[6]}') AS {0[5]} INNER JOIN (SELECT sid,{0[2]},{0[3]} FROM {0[4]} WHERE {0[9]} {0[2]}<{0[3]} and TradeDate='{0[7]}')".format(I)
                        )
                    if I[4]=='WeekStockInformation':
                        extra=" and REPLACE({0[3]},',','')  CONVERT(REPLACE({0[8][0]},',',''),DECIMAL(9,2)) AND CONVERT(REPLACE({0[2]},',',''),DECIMAL(9,2)))".format(I)
                
                        sqls.append(
                            "(SELECT sid,{0[2]},{0[3]} FROM {0[4]} WHERE {0[9]} {0[2]}>{0[3]} and  TradingWeek='{0[6]}') AS {0[5]} INNER JOIN (SELECT sid,{0[2]},{0[3]} FROM {0[4]} WHERE {0[9]} {0[2]}<{0[3]} and TradingWeek='{0[7]}')".format(I)
                        ) 
                    if I[4]=='MonthStockInformation':
                        extra=" and REPLACE({0[3]},',','')  CONVERT(REPLACE({0[8][0]},',',''),DECIMAL(9,2)) AND CONVERT(REPLACE({0[2]},',',''),DECIMAL(9,2)))".format(I)
                
                        sqls.append(
                            "(SELECT sid,{0[2]},{0[3]} FROM {0[4]} WHERE {0[9]} {0[2]}>{0[3]} and TradingMonth='{0[6]}') AS {0[5]} INNER JOIN (SELECT sid,{0[2]},{0[3]} FROM {0[4]} WHERE {0[9]} {0[2]}<{0[3]} and TradingMonth='{0[7]}')".format(I)
                        ) 
                # OSC由負轉正
                if I[1]=='FromNegativeToPositive':
                    # ['T8','FromNegativeToPositive','DIF12and26','MACD9','DayStockInformation','Y8',PreviousDay,LastDay,'',''],

                    if I[4]=='DayStockInformation':
                        sqls.append(
                            "(SELECT sid,{0[2]},{0[3]} FROM {0[4]} WHERE ({0[2]}-{0[3]})<0 and TradeDate='{0[6]}') AS {0[5]} INNER JOIN (SELECT sid,{0[2]},{0[3]} FROM {0[4]} WHERE ({0[2]}-{0[3]})>0 and TradeDate='{0[7]}')".format(I)
                        )
                    if I[4]=='WeekStockInformation':
                        sqls.append(
                            "(SELECT sid,{0[2]},{0[3]} FROM {0[4]} WHERE ({0[2]}-{0[3]})<0 and TradingWeek='{0[6]}') AS {0[5]} INNER JOIN (SELECT sid,{0[2]},{0[3]} FROM {0[4]} WHERE ({0[2]}-{0[3]})>0 and TradingWeek='{0[7]}')".format(I)
                        )
                    if I[4]=='MonthStockInformation':
                        sqls.append(
                            "(SELECT sid,{0[2]},{0[3]} FROM {0[4]} WHERE ({0[2]}-{0[3]})<0 and TradingMonth='{0[6]}') AS {0[5]} INNER JOIN (SELECT sid,{0[2]},{0[3]} FROM {0[4]} WHERE ({0[2]}-{0[3]})>0 and TradingMonth='{0[7]}')".format(I)
                        )
                # OSC由正轉負
                if I[1]=='FromPositiveToNegative':
                    # ['T8','FromNegativeToPositive','DIF12and26','MACD9','DayStockInformation','Y8',PreviousDay,LastDay,'',''],
                    if I[4]=='DayStockInformation':
                        sqls.append(
                            "(SELECT sid,{0[2]},{0[3]} FROM {0[4]} WHERE ({0[2]}-{0[3]})>0 and TradeDate='{0[6]}') AS {0[5]} INNER JOIN (SELECT sid,{0[2]},{0[3]} FROM {0[4]} WHERE ({0[2]}-{0[3]})<0 and TradeDate='{0[7]}')".format(I)
                        )
                    if I[4]=='WeekStockInformation':
                        sqls.append(
                            "(SELECT sid,{0[2]},{0[3]} FROM {0[4]} WHERE ({0[2]}-{0[3]})>0 and TradingWeek='{0[6]}') AS {0[5]} INNER JOIN (SELECT sid,{0[2]},{0[3]} FROM {0[4]} WHERE ({0[2]}-{0[3]})<0 and TradingWeek='{0[7]}')".format(I)
                        )
                    if I[4]=='MonthStockInformation':
                        sqls.append(
                            "(SELECT sid,{0[2]},{0[3]} FROM {0[4]} WHERE ({0[2]}-{0[3]})>0 and TradingMonth='{0[6]}') AS {0[5]} INNER JOIN (SELECT sid,{0[2]},{0[3]} FROM {0[4]} WHERE ({0[2]}-{0[3]})<0 and TradingMonth='{0[7]}')".format(I)
                        )
                
            # 處理排名篩選10~12
            if I[0] =='T10' or I[0] =='T11' or I[0] =='T12':
                sqls.append(
                    "(SELECT sid,{0[2]} FROM {0[1]} WHERE {1} ORDER BY CONVERT(REPLACE({0[2]},',',''),DECIMAL(9,2)) {0[3]} LIMIT {0[4]})".format(I,Day)
                )

            # 比較
            if I[0] =='T13' or I[0]== 'T14' or I[0] == 'T15':
                sqls.append(
                    "(SELECT sid,CONVERT(REPLACE({0[9]},',',''),DECIMAL(9,2)) as C2 FROM {0[8]} WHERE {1}) AS {0[7]}  INNER JOIN (SELECT sid,CONVERT(REPLACE({0[2]},',',''),DECIMAL(9,2)) as C1 FROM {0[1]} WHERE {2})".format(I,Day,Day2)

                )
            # 上市櫃選擇
            if I[0] == 'T16':
                if I[1] == 'market':
                    sqls.append(
                        "(SELECT {0[2]} FROM {0[1]} WHERE {0[2]}{0[3]}='{0[4]}') AS {0[1]} INNER JOIN (SELECT * FROM stock )".format(I)
                    )
            # 150戰法
            if I[0] == 'KD150':
                sqls.append(
"(SELECT sid,K9_,D9 FROM DayStockInformation WHERE K9_>D9 and K9_>50 and TradeDate='{0[3]}') AS D150 INNER JOIN \
(SELECT sid,K9_,D9 FROM DayStockInformation WHERE TradeDate='{0[4]}') AS DY150 INNER JOIN \
(SELECT sid,K9_,D9 FROM WeekStockInformation WHERE K9_>D9 and K9_>50  and TradingWeek='{0[5]}') AS W150 INNER JOIN \
(SELECT sid,K9_,D9 FROM WeekStockInformation WHERE  TradingWeek='{0[6]}') AS WY150 INNER JOIN \
(SELECT sid,K9_,D9 FROM MonthStockInformation WHERE K9_>D9 and K9_>50 and TradingMonth='{0[7]}') AS M150 INNER JOIN \
(SELECT sid,K9_,D9 FROM MonthStockInformation WHERE TradingMonth='{0[8]}') \
".format(I)
                )
            if I[0]== '20MV':
                sqls.append(
                    # (SELECT MAX(ClosingPrice) FROM DayStockInformation  TradeDate<='{0[1]}' and TradeDate>='{0[2]}') AS ND INNER JOIN
" \
(SELECT sid,PriceMA60,PriceMA20,HighestPrice FROM WeekStockInformation WHERE TradingWeek='{0[3]}') AS LW INNER JOIN \
(SELECT sid,PriceMA60,PriceMA20,HighestPrice FROM WeekStockInformation WHERE TradingWeek='{0[4]}') AS PW INNER JOIN \
(SELECT sid,PriceMA60,PriceMA20 FROM WeekStockInformation WHERE TradingWeek='{0[5]}') AS TW INNER JOIN \
(SELECT sid,ClosingPrice FROM DayStockInformation WHERE TradeDate='{0[1]}') \
".format(I)
                )
        # JOIN
        index=0
        sql=""
        for s in sqls:
            sql=sql+s+" AS {0} INNER JOIN ".format(submit[index][0])

            index+=1
        # 切除多餘

        sql=sql[:-11]
        # 關聯
        on_count=0
        for I in submit:
            if on_count==0:
                sql=sql+" ON "
            for T in submit:
                sql=sql+" {0[0]}.sid={1[0]}.sid AND".format(I,T)
            if I[1]=='RSI' or I[1]=='KD':
                sql=sql +" T0_1.sid=T0.sid AND T0_2.sid=T0.sid AND "
            if I[1] == 'classification':
                sql=sql +" classification.cid={0[0]}.cid AND " .format(I)
            if I[1] == 'market':
                sql=sql +" market.mid={0[0]}.mid AND " .format(I)
            if I[1] == 'KDGoldenCross':
                sql=sql +" {0[0]}.sid={0[5]}.sid AND " .format(I)
                # sql=sql +" Y8.sid=T8.sid AND {0[9]} T8.K9_>Y8.K9_ AND " .format(I)
            if I[1]== 'RSIGoldenCross':
                sql=sql +" {0[0]}.sid={0[5]}.sid AND " .format(I)
                # sql=sql +" Y8.sid=T8.sid AND {0[9]} T8.RSI6>Y8.RSI9 AND " .format(I)
            if I[1] == 'KDDeathCross':
                sql=sql +" {0[0]}.sid={0[5]}.sid AND " .format(I)
                # sql=sql +" Y8.sid=T8.sid AND {0[9]} T8.K9_<Y8.K9_ AND " .format(I)
            if I[1]== 'RSIDeathCross':
                sql=sql +" {0[0]}.sid={0[5]}.sid AND " .format(I)
                # sql=sql +" Y8.sid=T8.sid AND {0[9]} T8.RSI6<Y8.RSI9 AND " .format(I)
            if I[1] == 'Breakupward':
                sql=sql +" {0[0]}.sid={0[5]}.sid AND " .format(I)
                # sql=sql +" Y8.sid=T8.sid AND {0[9]} T8.ClosingPrice>Y8.ClosingPrice AND " .format(I)
            if I[1] == 'Downwardbreak': 
                sql=sql +" {0[0]}.sid={0[5]}.sid AND " .format(I)
                # sql=sql +" Y8.sid=T8.sid AND {0[9]} T8.ClosingPrice>Y8.ClosingPrice AND " .format(I)
            if I[1] =='FromNegativeToPositive' or I[1]=='FromPositiveToNegative':
                sql=sql +" {0[0]}.sid={0[5]}.sid AND " .format(I)
            if I[0] == "T13" or I[0] == "T14" or I[0] == "T15":
                sql=sql +" {0[0]}.C1{0[3]}{0[4]}{0[6]}{0[7]}.C2{0[10]}{0[11]} AND {0[0]}.sid={0[7]}.sid AND".format(I)
            if I[0] =='KD150':
                sql=sql+" D150.sid=DY150.sid AND W150.sid=WY150.sid AND M150.sid=KD150.sid AND D150.sid=T0.sid AND DY150.sid=T0.sid AND W150.sid=T0.sid AND WY150.sid=T0.sid AND M150.sid=T0.sid AND KD150.sid=T0.sid AND D150.K9_>DY150.D9 AND W150.K9_>WY150.D9 AND M150.K9_>KD150.D9 AND"
            if I[0]=='20MV':
            # D ND LW PW TW
                sql=sql+" 20MV.sid=LW.sid AND 20MV.sid=PW.sid AND 20MV.sid=TW.sid AND (20MV.ClosingPrice>LW.HighestPrice OR 20MV.ClosingPrice>PW.HighestPrice) AND PW.PriceMA60<=TW.PriceMA60 AND LW.PriceMA60>=PW.PriceMA60 AND PW.PriceMA20>TW.PriceMA20 AND LW.PriceMA20>PW.PriceMA20 AND "
            on_count+=1

    # 切除多餘
    sql=sql[:-4]
    
    # 顯示結果
    if submit[0][1] == 'New':
        sql="SELECT T0.* FROM "+sql+" ORDER BY T0.sid;"
    if submit[0][1] == 'RSI':
        sql="SELECT T0.*,T0_1.RSI6,T0_1.RSI9,T0_1.RSI12,T0_2.RSI6,T0_2.RSI9,T0_2.RSI12 FROM "+sql+" ORDER BY T0.sid;"
    if submit[0][1] == 'KD':
        sql="SELECT T0.*,T0_1.K9_,T0_1.D9,T0_2.K9_,T0_2.D9 FROM "+sql+" ORDER BY T0.sid;"
    if submit[0][1] =='institutional_investors':
        sql="SELECT T0.* FROM "+sql+" ORDER BY T0.sid;"
    print(sql)
    Quantity=cursor.execute(sql)
    information=cursor.fetchall()
    return information
# ___
import pymysql
db=pymysql.connect(
    host='163.18.104.164',
    user='bambu',
    password='test123',
    database="stock",
    port=3306
)
cursor=db.cursor()
def IsLastDay():
    cursor.execute("SELECT TradeDate FROM {} WHERE sid='{}';".format('DayStockInformation','9958'))
    check=cursor.fetchall()
    LastDay=check[-1][0]
    return LastDay
def IsPreviousDay():
    cursor.execute("SELECT TradeDate FROM {} WHERE sid='{}';".format('DayStockInformation','9958'))
    check=cursor.fetchall()
    PreviousDay=check[-2][0]
    return PreviousDay
def IsLastWeek():
    cursor.execute("SELECT TradingWeek FROM {} WHERE sid='{}';".format('WeekStockInformation','9958'))
    check=cursor.fetchall()
    LastWeek=check[-1][0]
    return LastWeek
def IsPreviousWeek():
    cursor.execute("SELECT TradingWeek FROM {} WHERE sid='{}';".format('WeekStockInformation','9958'))
    check=cursor.fetchall()
    PreviousWeek=check[-2][0]
    return PreviousWeek
def IsLastMonth():
    cursor.execute("SELECT TradingMonth FROM {} WHERE sid='{}';".format('MonthStockInformation','9958'))
    check=cursor.fetchall()
    LastMonth=check[-1][0]
    return LastMonth
def IsPreviousMonth():
    cursor.execute("SELECT TradingMonth FROM {} WHERE sid='{}';".format('MonthStockInformation','9958'))
    check=cursor.fetchall()
    PreviousMonth=check[-2][0]
    return PreviousMonth
def IsTwoWeeksAgo():
    cursor.execute("SELECT TradingWeek FROM {} WHERE sid='{}';".format('WeekStockInformation','9958'))
    check=cursor.fetchall()
    TwoWeeksAgo=check[-3][0]
    return TwoWeeksAgo
def IsNearlyAWeek():
    cursor.execute("SELECT TradeDate FROM {} WHERE sid='{}';".format('DayStockInformation','9958'))
    check=cursor.fetchall()
    NearlyAWeek=check[-7][0]
    return NearlyAWeek
if __name__=='__main__':
    LastDay=IsLastDay()
    PreviousDay=IsPreviousDay()
    LastWeek=IsLastWeek()
    PreviousWeek=IsPreviousWeek()
    LastMonth=IsLastMonth()
    PreviousMonth=IsPreviousMonth()
    TwoWeeksAgo=IsTwoWeeksAgo()
    NearlyAWeek=IsNearlyAWeek()
    print(LastDay)
    print(PreviousDay)
    # T0為顯示內容
    # T1~6為條件篩選
    # T7~T9為特殊篩選
    # T10~T12 排行篩選
    submit=[
            # ['T0','New',LastDay],
            # ['T0','institutional_investors',LastDay],
            # ['T0','RSI',LastDay,LastWeek,LastMonth],
            ['T0','KD',LastDay,LastWeek,LastMonth],
            # # 成交股數
            # ['T1', 'DayStockInformation', 'OpeningPrice', '', ('10', '20'), '2021/3/26'],
            # # # # 資券相抵
            # ['T2','MarginPurchase_ShortSale','Equity_Balance','',('0','1220000000000000'),'2021-01-27'],
            # #最高價
            # ['T3','MonthStockInformation','HighestPrice','',('10','1500'),'21M03'],
            # ['T4','institutional_investors','Sum','',('-24,957','222222222,224,957'),'2021-01-27'],
            # # # 月營收
            # ['T5','MonthlyRevenue','MonthRevenue','',('3,243','8111111118,853,244'),'2020-12-01'],

            # ['T6','SeasonalChart','SecuritiesToEquityRatio','',('0.0','1000000000000000.0'),'21Q1'],
            
            # ['T7','classification','cid','','^024'],

            # ['T8','DayStockInformation','RSI6','NOT',('-100000000','20'),LastDay],
            # ['T8','WeekStockInformation','RSI12','NOT',( '80', '1000000000'),LastWeek],
            # ['T8','DayStockInformation','SellingPressureRatio','',('-10000','80'),LastDay],
            # ['T8','DayStockInformation','SellingPressureRatio','',('80','90'),LastDay],
            # ['T8','DayStockInformation','SellingPressureRatio','',('90','100'),LastDay],
            # ['T8','DayStockInformation','SellingPressureRatio','',('100','110'),LastDay],
            # ['T8','DayStockInformation','SellingPressureRatio','',('110','120'),LastDay],
            # ['T8','DayStockInformation','SellingPressureRatio','',('120','100000'),LastDay],
            # ['T8','DayStockInformation','K9_','',('40','60'),time],
            # ['T8','DayStockInformation','K9_','',('60','80'),time],
            # ['T8','DayStockInformation','K9_','',('80','100000000'),time],
            # ['KD150','K9_','D9',LastDay,PreviousDay,LastWeek,PreviousWeek,LastMonth,PreviousMonth],
            # ['20MV',LastDay,NearlyAWeek,LastWeek,PreviousWeek,TwoWeeksAgo],
            # ['T9','KDGoldenCross','K9_','D9','WeekStockInformation','Y9',PreviousWeek,LastWeek,('-1000000','1000000'),''],
            # ['T8','KDGoldenCross','K9_','D9','DayStockInformation','Y8',PreviousDay,LastDay,('-10000','500000'),''],
            # ['T8','FromNegativeToPositive','DIF12and26','MACD9','DayStockInformation','Y8',PreviousDay,LastDay,'',''],
            # ['T8','FromPositiveToNegative','DIF12and26','MACD9','DayStockInformation','Y8',PreviousDay,LastDay,'',''],
            # ['T8','RSIGoldenCross','RSI6','RSI9','DayStockInformation','Y8',PreviousDay,LastDay,('20','50'),''],
            # ['T8','RSIDeathCross','RSI6','RSI9','DayStockInformation','Y8',PreviousDay,LastDay,('20','50'),''],
            # ['T8','WeekStockInformation','MACD9','DIF12and26','',('0','10000000'),LastWeek],
            # ['T8','Breakupward','ClosingPrice','SellingPressureRatio','DayStockInformation','Y8',PreviousDay,LastDay,('80','90'),'NOT'],
            # ['T8','Downwardbreak','ClosingPrice','PriceMA5','DayStockInformation','Y8',PreviousDay,LastDay,''],
            # ['T8','Downwardbreak','ClosingPrice','PriceMA20','WeekStockInformation','Y8',PreviousWeek,LastWeek, ''],
            # ['T8','Breakupward','ClosingPrice','PriceMA20','MonthStockInformation','Y8',PreviousMonth,LastMonth, ''],
            # ['T10','DayStockInformation','Transation_','DESC','100',LastDay],
            ['T13','DayStockInformation','HighestPrice','*1','+2','2021-03-29','>=','C13','DayStockInformation','K9_','*1','+1',LastDay],
            
            ['T16','market','mid','','1'],
    ]
    # SELECT sid,,TradeDate FROM DayStockInformation where TradeDate='' ORDER BY CONVERT(REPLACE(HighestPrice,',',''),DECIMAL(9,2))   )
    information=Filter(submit)
    count=1
    for i in information[:10]:
        print("___________",count)
        print(i)
        count+=1
