# PYTHON BASE 
import argparse
import pandas as pd
import FinanceDataReader as fdr
import matplotlib.pyplot as plt

# CUSTOM MODULE
from utils import avg_move_line

class GetStrategy():
    def __init__(self):
        self.kr_stocks = fdr.StockListing('KRX')
        self.stocks = self._get_stocks()
        pass
    
    def _get_stocks(self) -> list:
        kospi = fdr.StockListing('KOSPI')
        kosdaq = fdr.StockListing('KOSDAQ')
        stocks = pd.concat([kospi, kosdaq])
        return stocks
    
    def strategy_aggresive(self):
        for idx, code in enumerate(self.stocks['Code']):
            stock = fdr.DataReader(f'{code}').reset_index()
            name = self.stocks.iloc[idx]['Name']
            stock['60_avg_moving'] = stock['Close'].rolling(window=60).mean()
            stock['120_avg_moving'] = stock['Close'].rolling(window=120).mean()
            stock['150_avg_moving'] = stock['Close'].rolling(window=150).mean()
            stock['200_avg_moving'] = stock['Close'].rolling(window=200).mean()

            plt.figure(figsize=(15,10))
            plt.plot(stock['Date'], stock['Close'], 'd', label='price days')
            plt.plot(stock['Date'], stock['60_avg_moving'], 'b', label='60 days')
            plt.plot(stock['Date'], stock['120_avg_moving'], 'k', label='120 days')
            plt.plot(stock['Date'], stock['150_avg_moving'], 'c', label='150 days')
            plt.plot(stock['Date'], stock['200_avg_moving'], 'm', label='200 days')
            
            plt.legend()
            plt.show()
    
    def strategy_conservative(self):
        pass
    
    def strategy_neutral(self):
        pass    
    


if __name__ == "__main__":
    stretegy = GetStrategy()
    stretegy.strategy_aggresive()