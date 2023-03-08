from calendar import c
import pandas as  pd
import numpy as np
import math
from datetime import date, datetime, time, timedelta
import utility as myutil
from yfDownloadOptionStock import yfDownloadStock
# from autoOption import getStrikePrice

# get stock information to date=dateStr around periodDays days
def getStockInfo(dfs, dateStr, periodDays):
    dfs = dfs.reset_index()
    periodDays = periodDays
    df1 = dfs
    df2 = pd.DataFrame()
    data = {           
                'stockMean': 0, 
                'stockStd': 0, 
                'gapUnit': 0,
                'ref2': 0,
                'marketPrice': 0, 
                'date': '9999-99-99',
                'periodDays': 0,
                'mean2std': 0,
                'marketHigh' : 0, 
                'marketLow' : 0
                }
    
    dtDate = datetime.strptime(dateStr, '%Y-%m-%d').date()
    #dateIndex = df1.index[(df1.Close > 160.54)& (df1.Close < 160.56)].tolist()
    try:
        dateIndex = df1.index[(df1.Date == dateStr)].tolist()[0]
        minIndex = df1.index.min()
        maxIndex = df1.index.max()    
        # print(minIndex, maxIndex)
        if (dateIndex):        
            endIndex = dateIndex - periodDays
            if((endIndex <= maxIndex) and (endIndex >= minIndex)):
                df2 = df1[endIndex:dateIndex+1]
        
        if (len(df2)>0):
            df3 = df2.reset_index()
            # stockMean = round(df3["Adj Close"].mean(), 2)   
            # stockStd = round(df3["Adj Close"].std(), 2) 
            # marketHigh = df3["Adj Close"].max()
            # marketLow = df3["Adj Close"].min()
            # marketPrice = df3["Adj Close"].iloc[-1]
            stockMean = round(df3["Close"].mean(), 2)   
            stockStd = round(df3["Close"].std(), 2) 
            marketHigh = df3["Close"].max()
            marketLow = df3["Close"].min()
            marketPrice = df3["Close"].iloc[-1]
            priceDate =  df3["Date"].iloc[-1]            
            mean2std = round((marketPrice-stockMean)/(stockStd/2), 1)
            #print(marketPrice)
            priceGap = round((marketHigh-marketLow), 2)
            
            if(stockStd<1.5):
                gapUnit = 1
            elif(stockStd>=1.5 and stockStd<3):
                gapUnit = 2.5
            elif (stockStd>=3 and stockStd<=15):
                gapUnit = 5      
            elif(stockStd>15):
                gapUnit = 10 
            
            ref2 = gapUnit*math.ceil(2*stockStd/gapUnit)
            
            data = {           
                'stockMean': stockMean, 
                'stockStd': stockStd, 
                'gapUnit': gapUnit,
                'ref2': ref2,
                'marketPrice': marketPrice, 
                'date': priceDate,
                'periodDays': periodDays,
                'mean2std' : mean2std,
                'marketHigh' : marketHigh, 
                'marketLow' : marketLow
                }
            
            #print(data)                  
                
    except:
        print('out StockData')
        data = {           
            'stockMean': 0, 
            'stockStd': 0, 
            'gapUnit': 0,
            'ref2': 0,
            'marketPrice': 0, 
            'date': '9999-99-99',
            'periodDays': 0,
            'mean2std': 0,
            'marketHigh' : 0, 
            'marketLow' : 0
            }
        

    return data


def regrouprst(df):
    columnNames = df.columns
    callColumns = ['strikePrice']
    putColumns = ['strikePrice']
    for nameitm in columnNames:
        if ('call' in nameitm):
            callColumns.append(nameitm)
        elif ('put' in nameitm):
            putColumns.append(nameitm)
    
    dfcall = df[callColumns]
    dfput = df[putColumns]
    #print(len(dfcall), dfcall.head()) 
    dfrst = dfcall.append(dfput, sort=False) 
    #print(len(dfrst))
    return dfrst


def getyfoption(stockSymbol, expireDate):
    stockCsvPath = myutil.readStockcsvPath + stockSymbol +'.csv'
    dfStock = pd.read_csv(stockCsvPath, delimiter = ",")  
    # dfStock['Date'] = pd.to_datetime(dfStock['Date'], format='%Y-%m-%d')
    # dfStock.index = dfStock['Date']
    meanPrice = dfStock.Close.mean()
    stdPrice = dfStock.Close.std()
    refPrice = getStrikePrice(meanPrice, stdPrice)
    refPriceLow = refPrice.get('putStrike') - 4*refPrice.get('step')
    refPriceHigh = refPrice.get('putStrike') + 4*refPrice.get('step')
    print(stockSymbol, 'highRange', refPriceHigh, 'lowRange', refPriceLow)
    
    quoteDateStr = '2022-01-25'
    dtQuoteDate = datetime.strptime(quoteDateStr, '%Y-%m-%d')
    dtExpireDate = datetime.strptime(expireDate, '%Y-%m-%d')
    dtExpireDateStr = datetime.strftime(dtExpireDate, '%Y-%m-%d')
    days = myutil.days_between(quoteDateStr)+10
    print('days--', days)
    
    dfrst = pd.DataFrame()
    for i in range(days):
        dtQuoteDateNext = dtQuoteDate + timedelta(days=1)
        quoteDateNextStr =  datetime.strftime(dtQuoteDateNext, '%Y-%m-%d')    
        weekDayOfQuoteDate = dtQuoteDateNext.weekday()
        if (weekDayOfQuoteDate < 5 ):
            try:
                # optionCsvPath = r'file:///users/lan/Documents/pyproj38/TEST/output/optionPrice2022/'+stockSymbol + '/'+ stockSymbol +'_option' +quoteDateNextStr + '.csv'
                optionCsvPath = myutil.readOptioncsvPath +stockSymbol + '/'+ stockSymbol +'_option' +quoteDateNextStr + '.csv'
                df0 = pd.read_csv(optionCsvPath, delimiter = ",")                  
                
                orgColumnNames = df0.columns
                if('optionDate' in orgColumnNames):
                    df0 = df0.rename(columns={'optionDate':'quoteDate'})
                    
                df0['expireDate'] = pd.to_datetime(df0['expireDate']).dt.strftime('%Y-%m-%d')
                df0['quoteDate'] = pd.to_datetime(df0['quoteDate']).dt.strftime('%Y-%m-%d')
                df1 = df0[(df0['expireDate']== dtExpireDateStr)]                
                
                if(len(df0)>0):
                    orgColumnNames = df0.columns
                    df00 = df0.rename(columns={'strike':'strikePrice'})
                    if('optionDate' in orgColumnNames):
                        df00 = df00.rename(columns={'optionDate':'quoteDate'})
                    df1 = df00[(df00['expireDate']== dtExpireDateStr) & (df00['strikePrice'] >= refPriceLow) & (df00['strikePrice'] <= refPriceHigh)][['quoteDate', 'expireDate', 'strikePrice', 'lastPrice', 'type']]
                    dfput = df1[df1['type']=='put' ]
                    dfput = dfput.rename(columns={'lastPrice':'put'})
                    dfcall = df1[df1['type']=='call' ]
                    dfcall = dfcall.rename(columns={'lastPrice':'call'})
                    df0 = pd.merge(dfput, dfcall, on=['quoteDate', 'expireDate', 'strikePrice'], how='inner') 
                    df1 = df0[['quoteDate',  'expireDate',  'strikePrice',   'put',   'call']]     
                    dfs = dfStock.rename(columns={'Date':'quoteDate', 'Close':'marketPrice'}) 

                    df2 = pd.merge(df1, dfs, on='quoteDate', how='inner')
                    # df0 = df2[["stockSymbol", "quoteDate", "expireDate", "marketPrice",  "strikePrice", "call","put"]]
                    df0 = df2[["quoteDate", "expireDate", "strikePrice", "call", "put", "marketPrice"]]
                    # df0['stockSymbol'] = stockSymbol
                    
                    df0.insert(0, 'stockSymbol', stockSymbol)
                    
                if(len(dfrst)==0 and len(df0)>0):
                    dfrst = df0                        
                if(len(dfrst)>0 and len(df0)>0):
                    df1 = dfrst.append(df0, ignore_index=True)
                    df1.reset_index()
                    dfrst = df1
                
            except Exception as ex:
                pass
            
        dtQuoteDate = dtQuoteDateNext    
            
    # rstpath = '/users/lan/Documents/pyproj38/TEST/output/yfoption/'+ stockSymbol+expireDate.replace('-', '')+'yf.csv'
    rstpath = myutil.midOptionCsvPath + stockSymbol+expireDate.replace('-', '')+'yf.csv'
    if(len(dfrst)>0):
        dfrst.to_csv(rstpath)
    return dfrst

###keep 
def getOptionPriceAtExpireDate(stockSymbol, expireDate):  
    stockCsvPath = myutil.readStockcsvPath + stockSymbol +'.csv'
    dfStock0 = pd.read_csv(stockCsvPath, delimiter = ",") 
    slcColumns = ['Date', "Close"]
    dfStock = dfStock0[slcColumns]

    dfyf0 = getyfoption(stockSymbol, expireDate )
        # dftd = dftd0[dftd0['quoteDate']<'2022-02-01']
    dfyf = dfyf0[dfyf0['quoteDate']>='2022-02-01']
    
    if(len(dfyf)>0):
        df0 = dfyf
        df =  df0[["stockSymbol", "quoteDate", "expireDate", "marketPrice",  "strikePrice", "call", "put"]]
        df1 = arrangeOption(df) 
        df1['Date']  = df1.index 
        stockInfoList = []
        for stockDate in df1.index.tolist():
            rst = getStockInfo(dfStock, stockDate, 21) 
            stockInfoList.append([rst.get('date'), rst.get('marketPrice'), rst.get('stockMean'), rst.get('stockStd'),  rst.get('mean2std')])

        dfStockInfo  =  pd.DataFrame(stockInfoList)
        dfStockInfo.columns = ['Date', 'stockPrice', 'stockMean', 'stockStd', 'mean2Std']  
        df2 = pd.merge(dfStockInfo, df1, on='Date', how='inner')
        rstpath = myutil.OptionExpireDateRptPath + stockSymbol+expireDate.replace('-', '')+'.csv'
        df2.to_csv(rstpath)   
     

def arrangeOption(df):   
    df0 = df 
    strikePrices = df0.strikePrice.unique()
    dictOption = {}
    for strikePrice in strikePrices:        
        npCall = df0[df0['strikePrice']==strikePrice][['quoteDate', 'call']].to_numpy()
        dictCall = {npCall[i][0]:npCall[i][1] for i in range(0, len(npCall))}
        dictOption[str(strikePrice)+'call'] = dictCall
        npPut = df0[df0['strikePrice']==strikePrice][['quoteDate', 'put']].to_numpy()
        dictPut = {npPut[i][0]:npPut[i][1] for i in range(0, len(npPut))}
        dictOption[str(strikePrice)+'put'] =  dictPut
    
    df1 = pd.DataFrame(dictOption)

    return df1

def getOptionPriceForStockPriceInExpiredPeriod(stockSymbol, stockPrice, expireInMonths):
    stockPath = myutil.readStockcsvPath + stockSymbol +'.csv'
    dfStock = pd.read_csv(stockPath)  
    lastestDate = dfStock.Date.max()
    stockinfo = getStockInfo(dfStock, lastestDate, 30)
    priceLow = math.floor(stockPrice - stockinfo.get('gapUnit')/2)
    priceHigh = math.ceil(stockPrice + stockinfo.get('gapUnit')/2)  
    
    stockDatelist =  dfStock[(dfStock['Close'] <= priceHigh) & (dfStock['Close'] >= priceLow)].Date.tolist()
      
    
    optionPath = myutil.OptionDownloadPath+stockSymbol+'/*.csv'
    latestOptionFileName = myutil.getLatestFileInPath(optionPath)
    dfOptionL = pd.read_csv(latestOptionFileName)
    optionExpireDateListL = dfOptionL.expireDate.unique()
    earlistOptionFileName = myutil.getEarlistFileInPath(optionPath)
    dfOptionE = pd.read_csv(earlistOptionFileName)
    optionExpireDateListE = dfOptionE.expireDate.unique()

    refDateList = []
    for optionDate in optionExpireDateListE:
        for refDate in optionExpireDateListL:
            days = myutil.days_between(refDate, optionDate)
            if(days):
                if(days> math.floor(expireInMonths*31-30) and math.ceil(expireInMonths*31+20) ):
                    if refDate not in refDateList:
                        refDateList.append(refDate)
    
    optionDownloadList = []
    if (len(refDateList)>0):
        for optionExpiredDate in refDateList:
            for downloadDate in stockDatelist:                
                days = myutil.days_between(str(downloadDate), str(optionExpiredDate))
                if(days>0):
                    if(days>expireInMonths*31-30 and days<expireInMonths*31+20):                    
                        optionDownloadList.append([downloadDate, optionExpiredDate])
    
    stockinfoList = []     
    dfrst = pd.DataFrame()              
    if(len(optionDownloadList)>0):         
        dateList = []
        for optioncsv in optionDownloadList:
            rst = readOptionCsvFile(optioncsv[0], optioncsv[1], stockSymbol, dfStock)
            df0 = rst[0]
            if(len(dfrst)==0 and len(df0)>0):
                dfrst = df0                        
            if(len(dfrst)>0 and len(df0)>0):
                df1 = dfrst.append(df0, ignore_index=True)
                df1.reset_index()
                dfrst = df1
                if (rst[1].get('date') not in dateList):
                    stockinfoList.append([rst[1].get('date'), rst[1].get('marketPrice'), rst[1].get('stockMean'), rst[1].get('stockStd'),  rst[1].get('mean2std')])
                    dateList.append(rst[1].get('date'))
    if(len(stockinfoList)>0):
        dfStockInfo  =  pd.DataFrame(stockinfoList)
        dfStockInfo.columns = ['Date', 'stockPrice', 'stockMean', 'stockStd', 'mean2Std']
    if(len(dfrst)>0):
        rstpath = myutil.optionStrikeRptPath + stockSymbol+'_'+str(stockPrice)+'_yfOption.csv'
        rstpathf = myutil.optionStrikeRptPath+ stockSymbol+'Strike'+str(stockPrice)+'expireIn' + str(expireInMonths) +'m.csv'
        
        df1 = optionPriceExpiredInAYear(dfrst)
        df1['download_expire']  = df1.index
        df1['Date'] = df1['download_expire'].apply(lambda x: x[:10])
        df1['expireDate'] = df1['download_expire'].apply(lambda x: x[-10:])        
        df2 = pd.merge(dfStockInfo, df1, on='Date', how='inner')
        orgColumns = df2.columns.tolist()
        selColumns = orgColumns[:-2]
        finColumns = ['expireDate']
        finColumns.extend(selColumns)
        dff = df2[finColumns]
        dff.to_csv(rstpathf)
     

def optionPriceExpiredInAYear(df):   
    df0 = df 
    strikePrices = df0.strikePrice.unique()
    dictOption = {}
    for strikePrice in strikePrices:        
        npCall = df0[df0['strikePrice']==strikePrice][['quoteDate', 'expireDate', 'call']].to_numpy()
        # dictCall = {npCall[i][0]:npCall[i][2] for i in range(0, len(npCall))}
        dictCall = {npCall[i][0]+'_'+ npCall[i][1]:npCall[i][2] for i in range(0, len(npCall))}
        dictOption[str(strikePrice)+'call'] = dictCall
        npPut = df0[df0['strikePrice']==strikePrice][['quoteDate', 'expireDate', 'put']].to_numpy()
        # dictPut = {npPut[i][0]:npPut[i][2] for i in range(0, len(npPut))}
        dictPut = {npPut[i][0]+'_'+npPut[i][1]:npPut[i][2] for i in range(0, len(npPut))}
        dictOption[str(strikePrice)+'put'] =  dictPut
        
    df1 = pd.DataFrame(dictOption)
    return df1        
        
def readOptionCsvFile(optionDownloadDate, optionExpireDate, stockSymbol, dfStock):
    df0 = pd.DataFrame()    
    info = {}
    try:
        # optionCsvPath = r'file:///users/lan/Documents/pyproj38/TEST/output/optionPrice2022/'+stockSymbol + '/'+ stockSymbol  +'_option' +quoteDateNextStr + '.csv'
        optionCsvPath = myutil.readOptioncsvPath +stockSymbol + '/'+ stockSymbol +'_option' +optionDownloadDate + '.csv'
        df0 = pd.read_csv(optionCsvPath, delimiter = ",")  
        orgColumnNames = df0.columns
        if('optionDate' in orgColumnNames):
            df0 = df0.rename(columns={'optionDate':'quoteDate'})
            
        df0['expireDate'] = pd.to_datetime(df0['expireDate']).dt.strftime('%Y-%m-%d')
        df0['quoteDate'] = pd.to_datetime(df0['quoteDate']).dt.strftime('%Y-%m-%d')
        df1 = df0[(df0['expireDate']== optionExpireDate)]
        if(len(df0)>0):
            orgColumnNames = df0.columns
            df00 = df0.rename(columns={'strike':'strikePrice'})
            if('optionDate' in orgColumnNames):
                df00 = df00.rename(columns={'optionDate':'quoteDate'})
            df1 = df00[(df00['expireDate']== optionExpireDate) & (df00['strikePrice'] >= 120) & (df00['strikePrice'] <= 200)][['quoteDate', 'expireDate', 'strikePrice', 'lastPrice', 'type']]
            dfput = df1[df1['type']=='put' ]
            dfput = dfput.rename(columns={'lastPrice':'put'})
            dfcall = df1[df1['type']=='call' ]
            dfcall = dfcall.rename(columns={'lastPrice':'call'})
            df0 = pd.merge(dfput, dfcall, on=['quoteDate', 'expireDate', 'strikePrice'], how='inner') 
            df1 = df0[['quoteDate',  'expireDate',  'strikePrice',   'put',   'call']]     
            dfs = dfStock.rename(columns={'Date':'quoteDate', 'Close':'marketPrice'}) 

            df2 = pd.merge(df1, dfs, on='quoteDate', how='inner')
            # df0 = df2[["stockSymbol", "quoteDate", "expireDate", "marketPrice",  "strikePrice", "call","put"]]
            df0 = df2[["quoteDate", "expireDate", "strikePrice", "call", "put", "marketPrice"]]
            # df0['stockSymbol'] = stockSymbol
            df0.insert(0, 'stockSymbol', stockSymbol)
            
            info = getStockInfo(dfStock, optionDownloadDate, 21)
        
    except Exception as ex:
                pass
    return [df0, info]

def getStrikePrice(mean, std):  
    if(std<5):
        std = 5
    elif(std>10):
        std = 10
    putStrike = 0
    callStrike = 0

    putOrg = mean - std
    putList = []
    
    putFloor = math.floor(round(putOrg)/10)*10
    putCeil = math.ceil(round(putOrg)/10)*10
    putMid = (putFloor + putCeil)/2
    putList.append([putFloor, abs(putOrg-putFloor)])
    putList.append([putCeil, abs(putOrg-putCeil)])
    putList.append([putMid, abs(putOrg-putMid)])
    putvalues = putList[:][-1]
    putStrike = putList[putvalues.index(min(putvalues))][0]
    
    callOrg = mean + std
    callList = []
    
    callFloor = math.floor(round(callOrg)/10)*10
    callCeil = math.ceil(round(callOrg)/10)*10
    callMid = (callFloor + callCeil)/2
    callList.append([callFloor, abs(callOrg-callFloor)])
    callList.append([callCeil, abs(callOrg-callCeil)])
    callList.append([callMid, abs(callOrg-callMid)])
    callvalues = callList[:][-1]
    callStrike = callList[callvalues.index(min(callvalues))][0]
    
    step = int((callStrike - putStrike)/2)
    
    return {'putStrike': putStrike, 'callStrike': callStrike, 'step': step}



if __name__ == "__main__":       
    gapUnit = 5
    stockSymbol = 'AAPL'
    expireDate = '2024-01-19'
    expireInMonths = 12
    strikePrice = 160
    getOptionPriceAtExpireDate(stockSymbol, expireDate)
    getOptionPriceForStockPriceInExpiredPeriod(stockSymbol, strikePrice, expireInMonths)