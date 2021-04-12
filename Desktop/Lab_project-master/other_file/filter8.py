def Filter(submit):
    import pymysql
    db=pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='',
        database="stock",
        port=3306
    )
    cursor=db.cursor()
    sqls=[]
    # __________________________________
    
    for I  in submit:

        # 處理顯示結果
        if I[0] =='T0' and I[1]=='DayStockInformation':
            sqls.append(
                "(SELECT stock.sid,stock.s_name,DayStockInformation.TradeDate,DayStockInformation.OpeningPrice,DayStockInformation.HighestPrice,DayStockInformation.LowestPrice,DayStockInformation.ClosingPrice,DayStockInformation.Change_,DayStockInformation.Transation_ FROM DayStockInformation,stock WHERE TradeDate='{0[2]}' and stock.sid=DayStockInformation.sid) ".format(I)
            )
            # 
        else:
            # 表日期
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
            if len(I)>7 and I[8]=='DayStockInformation':
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
                if I[1] == 'DayStockInformation':
                    sqls.append(
                        """(SELECT sid,{0[2]} FROM {0[1]} WHERE REPLACE({0[2]},',','') {0[3]} BETWEEN CONVERT(REPLACE('{0[4][0]}',',',''),SIGNED) AND CONVERT(REPLACE('{0[4][1]}',',',''),SIGNED)  AND {1})""".format(I,Day)
                    )
            # 處理排名篩選10~12
            if I[0] =='T10' or I[0] =='T11' or I[0] =='T12':
                sqls.append(
                    "(SELECT sid,{0[2]} FROM {0[1]} WHERE {1} ORDER BY CONVERT(REPLACE({0[2]},',',''),DECIMAL(9,2)) {0[3]} LIMIT {0[4]})".format(I,Day)
                )
            if I[0] =='T13':
                # sqls.append(
                #     "(SELECT sid,HighestPrice FROM DayStockInformation WHERE TradeDate='2021-03-29') AS C13 INNER JOIN (SELECT sid,K9_ FROM DayStockInformation WHERE TradeDate='2021-03-26')"
                # )                                                               
                # >index=6
                # ['T13','DayStockInformation','HighestPrice','1','2','2021-03-29','>','C13','DayStockInformation','K9_','1','2','2023-01-29'],
                sqls.append(
                    "(SELECT sid,{0[9]} FROM {0[8]} WHERE {1}) AS {0[7]}  INNER JOIN (SELECT sid,{0[2]} FROM {0[1]} WHERE {2})".format(I,Day,Day2)
                )
            # 上市櫃選擇
            if I[0] == 'T16':
                if I[1] == 'market':
                    sqls.append(
                        "(SELECT {0[2]} FROM {0[1]} WHERE {0[2]}{0[3]}='{0[4]}') AS {0[1]} INNER JOIN (SELECT * FROM stock )".format(I)
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
            if I[1] == 'classification':
                sql=sql +" classification.cid={0[0]}.cid AND " .format(I)
            if I[1] == 'market':
                sql=sql +" market.mid={0[0]}.mid AND " .format(I)
            if I[0] == "T13":
                sql=sql +" {0[0]}.{0[2]}{0[3]}{0[4]}{0[6]}{0[7]}.{0[9]}{0[10]}{0[11]} AND {0[0]}.sid={0[7]}.sid AND".format(I)
            on_count+=1

    # 切除多餘
    sql=sql[:-4]
    
    # 顯示結果
    sql="SELECT T0.* FROM "+sql+" ORDER BY T0.sid;"
    # print(sql)
    Quantity=cursor.execute(sql)
    information=cursor.fetchall()

    return information
# ___
def IsAfterHours():
    import pymysql
    db=pymysql.connect(
        host='163.18.104.164',
        user='bobo',
        password='bobo123',
        database="stock",
        port=3306
    )
    cursor=db.cursor()
    cursor.execute("SELECT TradeDate FROM {} WHERE sid='{}';".format('DayStockInformation','9958'))
    check=cursor.fetchall()
    time=check[-1][0]
    return time
if __name__=='__main__':
    time=IsAfterHours()
    print(time)
    # T0為顯示內容
    # T1~6為條件篩選
    # T7~T9為特殊篩選
    # T10~T12 排行篩選
    submit=[
            ['T0','DayStockInformation',time],
            # 成交股數
            ['T1','WeekStockInformation','HighestPrice','',('0','1500'),'21W01'],
            # # # 資券相抵
            ['T2','MarginPurchase_ShortSale','Equity_Balance','',('0','1220000000000000'),'2021-01-27'],
            #最高價
            ['T3','MonthStockInformation','HighestPrice','',('10','1500'),'21M03'],
            ['T4','institutional_investors','Sum','',('-24,957','222222222,224,957'),'2021-01-27'],
            # # 月營收
            ['T5','MonthlyRevenue','MonthRevenue','',('3,243','8111111118,853,244'),'2020-12-01'],

            ['T6','SeasonalChart','SecuritiesToEquityRatio','',('0.0','1000000000000000.0'),'21Q1'],
            
            ['T7','classification','cid','','^024'],

            ['T8','DayStockInformation','D9','',('20','40'),'2021-03-26'],

            ['T10','DayStockInformation','TradeVolume','DESC','100','2021-01-29'],

            ['T13','DayStockInformation','HighestPrice','*1','+2','2021-03-29','>=','C13','DayStockInformation','K9_','*1','+1','2021-03-29'],
            
            ['T16','market','mid','','1'],
    ]
    # SELECT sid,,TradeDate FROM DayStockInformation where TradeDate='' ORDER BY CONVERT(REPLACE(HighestPrice,',',''),DECIMAL(9,2))   )
    information=Filter(submit)
    count=1
    for i in information[:10]:
        print("___________",count)
        print(i)
        count+=1