def Connect():
    import pymysql.cursors
    config = {
    'host':'163.18.104.164',
    'port':3306,
    'user':'bobo',
    'password':'bobo123',
    'charset':'utf8',
    'cursorclass':pymysql.cursors.DictCursor,
    'database':'stock'
    }
    # Connect to the database
    connection = pymysql.connect(**config)
    cursor = connection.cursor()
    ## cursor.execute("SHOW TABLES")
    cursor.execute("SELECT * FROM StockSelectionFactor")
    datas = cursor.fetchall() ## it returns list of tables present in the database
    return datas

## Data Preprocessing And MinMax
def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
    
def Preprocess(data, submit):
    ROR = []
    #Store t+2 information
    for row in data:
        if isfloat(row['StockReturn']):
            ROR.append(row['StockReturn'])
        else:
            ROR.append("--")
    #Merge two data
    for i in range(0, len(ROR)-1):
        if data[i]['sid'] != data[i+1]['sid']:
            data[i]['t+2_StockReturn'] = '--'
        else:
            data[i]['t+2_StockReturn'] = ROR[i+1]
    data[len(data)-1]['t+2_StockReturn'] = '--'
    #Data Cleansing
    for i in range(0, len(data)):
        del data[i]['T2StockReturn']
        del data[i]['T3StockReturn']
    for i in range(0, len(submit)-3):
         for j in range(0, len(data)):
                del data[j][submit[i]]
    index = 0
    while 1:
        if index == len(data):
            break
        for key, value in data[index].items():
            if value == '-' or value == '--':
                del data[index]
                index = index-1
                break
        index = index+1
    return data

def minmax(datas):
    from sklearn import preprocessing
    scaler = preprocessing.MinMaxScaler()
    scaler.fit(datas)
    return scaler.transform(datas)

## Data Normalization
def normalization(datas, submit):
    Q = int(submit[-2])
    Y = int(submit[-3])
    valid = []
    listdata = []
    info = []
    if Q <= 3:
        Q = 3
        Y = Y-1
    elif Q <= 6:
        Q = 4
        Y = Y-1
    elif Q <= 9:
        Q = 1
    else:
        Q = 2
    for i in range(len(datas)):
        listdata.append([])
        info.append([])
        for key, value in datas[i].items():
            if key == 'sid' or key == 'Quarterly':
                info[len(info)-1].append(value)
                continue
            listdata[len(listdata)-1].append(value)
    l = 0
    r = 0
    while r != len(listdata):
        if info[r][0] != info[l][0]:
            listdata[l:r] = minmax(listdata[l:r]).tolist()
            l = r
        else:
            r = r+1
    listdata[l:] = (minmax(listdata[l:])).tolist()
    for i in range(0, len(info)):
        listdata[i].insert(0, info[i][1])
        listdata[i].insert(0, info[i][0])
    index = 0
    while 1:
        if index == len(listdata):
            break
        if int(listdata[index][1][0:4]) == Y and int(listdata[index][1][-1]) == Q:
            valid.append(listdata[index])
            del listdata[index]
            index = index-1
        index = index+1
    return listdata, valid

def writeToFile(datas, csv_file):
    import csv
    try:
        with open(csv_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(datas)
    except IOError:
        print("I/O error")

def callCFunc():
    import ctypes
    func = ctypes.CDLL("libfunc.so")
    func.main()

def getFinalResult():
    with open("stocklist.txt", 'r') as f:
        contents = f.read()
        ret = contents.split("\n")
        ret.pop()
        return ret
def main(submit):
    datas = Connect()
    datas = Preprocess(datas, submit)
    datas, valid = normalization(datas, submit)
    writeToFile(datas, "Train.csv")
    writeToFile(valid, "Valid.csv")
    callCFunc()
    ret = getFinalResult()
    return ret
## main([2021, 4, 11])
