from gc import callbacks
from subprocess import call
import yfinance as yf
import pandas as  pd
import numpy as np
import datetime as dt
from datetime import date, datetime, time, timedelta
import io



import utility as myutil
todayDate = myutil.TodayDate
todayDateStr = myutil.TodayDateStr




def yfDownloadStock(stockSymbol, *period):    
    ticker = stockSymbol
    
    if (len(period) == 1):
        start = period[0]
        end = dt.datetime.now()
    elif (len(period) == 2):
        start = period[0]
        end = period[1]
    else:
        start = dt.datetime(myutil.LastYear, 1, 1)
        end = dt.datetime.now()
    df0 = pd.DataFrame()
    try:
        data = yf.download(ticker, start=start, end=end)
        df0 = pd.DataFrame(data)
        df0['stockSymbol'] = stockSymbol
        print(df0.tail())
    except:
        pass
        print(stockSymbol, 'Option download done')
    
    if(len(df0)>0): 
        rstpath = myutil.StockDownloadPath +stockSymbol +'.csv'
        df0.to_csv(rstpath)
        
    return  df0
        


def yfDownloadOption(stockSymbol):    
    stockInfo = yf.Ticker(stockSymbol)
    print(stockInfo)
    
    # get Friday date, only download weekday's option price
    fridayDate = todayDate
    if (todayDate.weekday()!=4):
        for i in range(7):            
            dateNew = todayDate + timedelta(days=i)
            if(dateNew.weekday()==4):
                fridayDate = dateNew
                break        

    fridayDateStr = dt.datetime.strftime(fridayDate, '%Y-%m-%d')
    df0 = pd.DataFrame()
    for i in range(0, 800, 7):
        newFridayDate = fridayDate + timedelta(days=i)
        newFridayDateStr = dt.datetime.strftime(newFridayDate, '%Y-%m-%d')
        try:
            opt = stockInfo.option_chain(newFridayDateStr)
            if (opt):
                dfput = pd.DataFrame(opt.puts)
                dfput['type'] = 'put'
                dfcall = pd.DataFrame(opt.calls)
                dfcall['type'] = 'call'
                df1 = pd.concat([dfput, dfcall])
                df1['expireDate'] = newFridayDateStr
                df2 = pd.concat([df0, df1])
                df0 = df2
        except:
            pass
    df0['quoteDate'] = todayDateStr
    if(len(df0)>0):
        rstpath = myutil.OptionDownloadPath+stockSymbol+'/'+stockSymbol+ '_option'+todayDateStr +'.csv'
        df0.to_csv(rstpath)
    print(stockSymbol, 'Option download done')
    return df0
        
if __name__ == "__main__":   
    stockList = myutil.StockList
    
    for stockSymbol in stockList:
        dfOption = yfDownloadOption(stockSymbol)
        if(len(dfOption)>0): 
            dfOption['quoteDate'] = todayDateStr
            rstpath = myutil.OptionDownloadPath+stockSymbol+'/'+stockSymbol+ '_option'+todayDateStr +'.csv'
            dfOption.to_csv(rstpath)

            dfStock = yfDownloadStock(stockSymbol)
            print(dfStock.tail())
            if(len(dfStock)>0): 
                rstpath = myutil.StockDownloadPath +stockSymbol +'.csv'
                dfStock.to_csv(rstpath)

   