import numpy as np
import pandas as pd
import pandas_datareader.data as web 
import datetime as dt
from datetime import date, datetime, time, timedelta
import math

import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as md
import os, glob

ColorList = ['r', 'g', 'c', 'y', 'm', 'b']
TodayDate = date.today()
TodayDateStr = dt.datetime.strftime(TodayDate, '%Y-%m-%d')
Today = datetime.today()
datem = datetime(Today.year-1, Today.month, 1)
YearAgoStr =  dt.datetime.strftime(datem, '%Y-%m-%d')

LastYear = dt.datetime.now().year-1
StockList = ['AAPL', 'JPM', 'TSLA', 'MSFT', 'SPY']
StockList = ['AAPL']
StockDownloadPath = '../output/stockPrice/' 
# + stockSymbol +'.csv'
OptionDownloadPath = '../output/optionPrice2022/' 
# + stockSymbol +'/+stockSymbol+'_optionDownloadDate.csv'

readStockcsvPath = r'../output/stockPrice/'
#stockSymbol +'.csv'
readOptioncsvPath = r'../output/optionPrice2022/'
# + stockSymbol+expireDate.replace('-', '')+'yf.csv'

OptionExpireDateRptPath = '../output/optionPriceAtExpireDate/'
optionStrikeRptPath = '../output/optionPriceByStrikePrice/'
midOptionCsvPath = '../output/yfoption/'
readMidOptionCsvPath = r'../output/yfoption/'

# two dates days difference, default days in between date to today's  in dateString
def days_between(d1, *d2):
    days = -1
    try:
        # print(d1, "-", d2)
        d1 = dt.datetime.strptime(d1, "%Y-%m-%d")
        if(len(d2)==0):
            d3 = dt.datetime.strptime(TodayDateStr, "%Y-%m-%d")
            days = abs(d1 - d3 ).days
        else:
            d20 = dt.datetime.strptime(d2[0], "%Y-%m-%d")
            days = abs((d20 - d1).days)
    except Exception as ex:
        days = -1
        # print(ex)        
        
    return days

def firstDayOfNmonthAgo(aDateStr, nMonth):
    selectDt = dt.datetime.strptime(aDateStr, '%Y-%m-%d')
    y = math.floor((nMonth+selectDt.month)/12.0)
    dtNmonthAgoStr = "error: date not exist "
    if y<0:
        print(dtNmonthAgoStr)        
    elif y>0 :
        m = (nMonth+selectDt.month) - y*12
    elif y==0:
        if(selectDt.month-nMonth>0):
            m = selectDt.month - nMonth
        else:
            y=1
            m = 12 + selectDt.month - nMonth
         
    print(y, m)
    # dtOneYearAgo  = dt.datetime(selectDt.year-y, m, 1)
    # dtOneYearAgoStr = dt.datetime.strftime(dtOneYearAgo, '%Y-%m-%d')
    dtNmonthAgo = dt.datetime(selectDt.year-y, m, 1)
    dtNmonthAgoStr = dt.datetime.strftime(dtNmonthAgo, '%Y-%m-%d')
    print(dtNmonthAgoStr)
    
    return dtNmonthAgoStr

def getLatestFileInPath(path):
    list_of_files = glob.glob(path, recursive=True)
    if(len(list_of_files)>0):
        latest_file = max(list_of_files, key=os.path.getctime)
    else:
        latest_file = ''
    return latest_file

def getEarlistFileInPath(path):
    list_of_files = glob.glob(path, recursive=True)
    if(len(list_of_files)>0):
        earlist_file = min(list_of_files, key=os.path.getctime)
    else:
        earlist_file = ''
    return earlist_file

if __name__ == "__main__":    
    quoteDateStr = '2022-01-25'
    # dtQuoteDate = datetime.strptime(quoteDateStr, '%Y-%m-%d')
    today = str(date.today())
    days = days_between(quoteDateStr, '2021-09-09')
    

