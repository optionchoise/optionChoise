from yfDownloadOptionStock import yfDownloadStock
from readTDOption import getOptionPriceForStockPriceInExpiredPeriod, getOptionPriceAtExpireDate
import utility as myutil


if __name__ == "__main__":     
    stockSymbol = 'JPM'
    expireDate = '2024-01-19'
    expireInMonths = 6
    stockPrice = 120
    yfDownloadStock(stockSymbol, '2021-01-01')
    getOptionPriceAtExpireDate(stockSymbol, expireDate)
    getOptionPriceForStockPriceInExpiredPeriod(stockSymbol, stockPrice, expireInMonths)