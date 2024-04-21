# PYTHON BASE 
import argparse
import pandas as pd
import FinanceDataReader as fdr
import matplotlib.pyplot as plt
from tqdm import tqdm



class KorStock():
    def __init__(self):
        self.kr_stocks = fdr.StockListing('KRX')
        self.stocks = self._get_stocks()
        
    def _get_stocks(self)-> list:
        kospi = fdr.StockListing('KOSPI')
        kosdaq = fdr.StockListing('KOSDAQ')
        snp = fdr.StockListing('S&P500')
        nasdaq = fdr.StockListing('NASDAQ')
        stocks = pd.concat([snp, nasdaq])
        # stocks = pd.concat([kospi, kosdaq])
        return stocks
    
    def strategy_aggresive(self)-> None:
        # for idx, code in tqdm(enumerate(self.stocks['Code'])):
        for idx, code in tqdm(enumerate(self.stocks['Symbol']), total=len(self.stocks['Symbol'])):
        # for idx, code in enumerate([314930]):
            
            stock = fdr.DataReader(f'{code}').reset_index()
            name = self.stocks.iloc[idx]['Name']
            stock['50_avg_moving'] = stock['Close'].rolling(window=50).mean()
            stock['120_avg_moving'] = stock['Close'].rolling(window=120).mean()
            stock['150_avg_moving'] = stock['Close'].rolling(window=150).mean()
            stock['200_avg_moving'] = stock['Close'].rolling(window=200).mean()

            high_52 = stock['Close'][-260:].max() # 52 week high
            low_52 = stock['Close'][-260:].min() # 52 week low 

            
            # 추가 컨디션:
            # trending line 에 대한 true false 값이 나오기 때문에 특정 기간을 잡고 해당 기간동안 trued의 갯수가 일정 기간을 충족하는지 확인

            # plt.figure(figsize=(15,10))
            # plt.plot(stock['Date'], stock['Close'], 'd', label='price days')
            # plt.plot(stock['Date'], stock['50_avg_moving'], 'b', label='60 days')
            # plt.plot(stock['Date'], stock['120_avg_moving'], 'k', label='120 days')
            # plt.plot(stock['Date'], stock['150_avg_moving'], 'c', label='150 days')
            # plt.plot(stock['Date'], stock['200_avg_moving'], 'm', label='200 days')
            
            # plt.legend()
            # plt.show()
            
            file = open("result.txt", "w")

            # con 0) skip if the compnay is more than 10 years or less than 6 month
            if (len(stock['Close']) > 260 * 10) or (len(stock['Close']) < 130):
                continue

            # con 1) current price higher than 200 trending line
            condition1 = stock['Close'] > stock['200_avg_moving']
            
            if True in condition1[-66:].value_counts().index:
                if not(condition1[-66:].value_counts()[True] > 55):
                    continue
            else: continue

            # con 2) current price higher thatn 150 trending line
            condition2 = stock['Close'] > stock['150_avg_moving']
            if True in condition2[-44:].value_counts().index:
                if not(condition2[-44:].value_counts()[True] > 37):
                    continue
            else: continue
                
            # con 3) 150 trending line higher than 200 trending line
            condition3 = stock['150_avg_moving'] > stock['200_avg_moving']
            if True in condition3[-44:].value_counts().index:
                if not(condition3[-44:].value_counts()[True] > 30):
                    continue
            else: continue

            # con 4) 50 trending line higher than 200 & 150 trending line
            condition4_1 = stock['50_avg_moving'] > stock['150_avg_moving']
            if True in condition4_1[-44:].value_counts().index:
                if not(condition4_1[-44:].value_counts()[True] > 35):
                    continue
            else: continue

            condition4_2 = stock['50_avg_moving'] > stock['200_avg_moving']
            if True in condition4_2[-66:].value_counts().index:
                if not(condition4_2[-66:].value_counts()[True] > 55):
                    continue
            else: continue
            
            # con 5) current price higher than 50 avg moving line
            condition5 = stock['Close'] > stock['50_avg_moving']
            if True in condition5[-22:].value_counts().index:
                if not(condition5[-22:].value_counts()[True] > 11):
                    continue
            else: continue
            

            # con 5) 200 trending line at rising phase for at least 1 month
            for idx in range(66):
                if not(stock['200_avg_moving'][len(stock['200_avg_moving']) - 1 - idx] >= stock['200_avg_moving'][len(stock['200_avg_moving']) -2 -idx]):
                    continue

            # con 6) current price within  +- 30% of 52 week high
            if not(high_52 * 0.7 <= stock['Close'].iloc[-1] <= high_52 * 1.3):
                continue

            # con 7) cuurent price >= 52 week low * 0.7
            if not(low_52 * 1.3 <= stock['Close'].iloc[-1]):
                continue
                
            file.write(f"{name}\n")
            print(name)

    def strategy_conservative(self):
        pass
    
    def strategy_neutral(self):
        pass    
    


if __name__ == "__main__":
    stretegy = GetStrategy()
    stretegy.strategy_aggresive()