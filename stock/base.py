# PYTHON BASE 
import argparse
from multiprocessing import Pool

# EXTERNAL
import pandas as pd
import FinanceDataReader as fdr
import yfinance as yf
from tqdm import tqdm
from matplotlib import pyplot as plt

# CUSTOM MODULE
from .indicator import buystrength, eps_growth, rsi
from .utils import mapping

import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)

# mother class
class Stock:
    def __init__(self, country:str)-> None:
        self.stocks, self.market = self._get_stock(country) # get stocks and market
        
    # Return Stock lists
    def _get_stock(self, country:str) -> pd.DataFrame:
        country = country.lower()
        if country == "korea" or country == "kor":
            kospi = fdr.StockListing('KOSPI')
            kosdaq = fdr.StockListing('KOSDAQ')
            stocks = pd.concat([kospi, kosdaq])
            kospi = fdr.DataReader('KS11') # KOSPI 지수 (KRX)
            # kosdaq = fdr.DataReader('KQ11') # KOSDAQ 지수 (KRX)
            market = kospi
        elif country == "usa" or "america":
            # TODO: RSI should be calculated differently where the stock is included
            snp = fdr.StockListing('S&P500')
            nasdaq = fdr.StockListing('NASDAQ')
            stocks = pd.concat([snp, nasdaq])
            snp500 = yf.Ticker("^GSPC").history(period="1mo") # snp500 price data
            # nasdaq = yf.Ticker("^IXIC").history(period="1mo") # nasdaq price data
            market = snp500 # for now calculate the RSI solely by snp500 index
        return stocks, market
    
    # get stock length
    def _get_total(self)-> int:
        return len(self.stocks['Symbol'])

class USStock(Stock):
    def __init__(self, country:str)-> None:
        print("usa stock intialize")
        super().__init__(country)
    
    def run(self):
        if False:
            with Pool(processes=10) as pool:
                pool.starmap(self.strategy_aggresive, zip(self.stocks['Symbol'], list(range(0,len(self.stocks['Symbol'])))))
        else:    
            for x,y in zip(self.stocks['Symbol'], list(range(0,len(self.stocks['Symbol'])))):
                self.strategy_aggresive(x,y)
    
    def strategy_aggresive(self, code, idx):
        name = mapping(code)
        stockinfo = yf.Ticker(name)
        stock = stockinfo.history(period="11y")
        
        # if len(stock) == 0 or len(stock) > 2517*3:
            # continue
        
        eps = eps_growth(stockinfo.income_stmt)
        bstrength = buystrength(stockinfo.recommendations)
        rsi_strength = rsi(self.market, stock)
        
        if len(bstrength) == 0:
            pass
        elif bstrength['0'] < 70 or bstrength['1'] < 70:
            return 0
        
        name = self.stocks.iloc[idx]['Name']
        stock['50_avg_moving'] = stock['Close'].rolling(window=50).mean()
        stock['120_avg_moving'] = stock['Close'].rolling(window=120).mean()
        stock['150_avg_moving'] = stock['Close'].rolling(window=150).mean()
        stock['200_avg_moving'] = stock['Close'].rolling(window=200).mean()
        high_52 = stock['Close'][-260:].max() # 52 week high
        low_52 = stock['Close'][-260:].min() # 52 week low 
        file = open("result.txt", "w")

        # con 0) skip if the compnay is more than 10 years or less than 6 month
        if (len(stock['Close']) > 260 * 10) or (len(stock['Close']) < 130):
            return 0

        # con 1) current price higher than 200 trending line
        condition1 = stock['Close'] > stock['200_avg_moving']
        
        if True in condition1[-66:].value_counts().index:
            if not(condition1[-66:].value_counts()[True] > 55):
                return 0
        else: return 0

        # con 2) current price higher thatn 150 trending line
        condition2 = stock['Close'] > stock['150_avg_moving']
        if True in condition2[-44:].value_counts().index:
            if not(condition2[-44:].value_counts()[True] > 37):
                return 0
        else: return 0
            
        # con 3) 150 trending line higher than 200 trending line
        condition3 = stock['150_avg_moving'] > stock['200_avg_moving']
        if True in condition3[-44:].value_counts().index:
            if not(condition3[-44:].value_counts()[True] > 30):
                return 0
        else: return 0

        # con 4) 50 trending line higher than 200 & 150 trending line
        condition4_1 = stock['50_avg_moving'] > stock['150_avg_moving']
        if True in condition4_1[-44:].value_counts().index:
            if not(condition4_1[-44:].value_counts()[True] > 35):
                return 0
        else: return 0

        condition4_2 = stock['50_avg_moving'] > stock['200_avg_moving']
        if True in condition4_2[-66:].value_counts().index:
            if not(condition4_2[-66:].value_counts()[True] > 55):
                return 0
        else: return 0
        
        # con 5) current price higher than 50 avg moving line
        condition5 = stock['Close'] > stock['50_avg_moving']
        if True in condition5[-22:].value_counts().index:
            if not(condition5[-22:].value_counts()[True] > 11):
                return 0
        else: return 0

        # con 5) 200 trending line at rising phase for at least 1 month
        for idx in range(66):
            if not(stock['200_avg_moving'][len(stock['200_avg_moving'])-1-idx] >= stock['200_avg_moving'][len(stock['200_avg_moving']) -2 -idx]):
                return 0

        # con 6) current price within  +- 30% of 52 week high
        if not(high_52 * 0.7 <= stock['Close'].iloc[-1] <= high_52 * 1.3):
            return 0

        # con 7) cuurent price >= 52 week low * 0.7
        if not(low_52 * 1.3 <= stock['Close'].iloc[-1] <= low_52 * 1.5):
            return 0
        
        data = stock['Close'][-260*2:]
        plt.plot(data, color='red', linewidth=2)
        plt.title(f'{code} Performance')
        plt.ylabel('Price ($)')
        plt.xlabel('Date')
        
        positions = [(0,y+0.5) for y in range(len(eps)+len(bstrength))]

        # for idx,x in enumerate(eps):
        #     text = plt.text(
        #         positions[idx][0],
        #         positions[idx][1],
        #         f'{x} {eps[x]}', 
        #         horizontalalignment='center', wrap=True)

        # for idx,x in enumerate(bstrength):
        #     text = plt.text(
        #         positions[idx+len(eps)][0], 
        #         positions[idx+len(eps)][1], 
        #         f'{x} {bstrength[x]}', 
        #         horizontalalignment='center', wrap=True)
        
        plt.tight_layout(rect=(0,.05,1,1)) 
        plt.savefig(f"result/{code}.png")
        print(code)
        print(eps)
        print(bstrength)

    def strategy_conservative(self):
        pass
    
    def strategy_neutral(self):
        pass    
    
class KorStock():
    def __init__(self):
        self.kr_stocks = fdr.StockListing('KRX')
        self.stocks = self._get_stocks()
        
    def _get_stocks(self) -> list:
        kospi = fdr.StockListing('KOSPI')
        kosdaq = fdr.StockListing('KOSDAQ')
        snp = fdr.StockListing('S&P500')
        nasdaq = fdr.StockListing('NASDAQ')
        stocks = pd.concat([snp, nasdaq])
        # stocks = pd.concat([kospi, kosdaq])
        return stocks
        
    def strategy_aggresive(self):
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

            #TODO: 외국인 수급 들어온 종목 추가
            #TODO: EPS 추가 종목
            #TODO: 눌림목 차트 위치
            #TODO: 매수의견 STRONG BUY 조건
            
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

    def strategy_conservative(self):
        pass
    
    def strategy_neutral(self):
        pass    

if __name__ == "__main__":
    stretegy = GetStrategy()
    stretegy.strategy_aggresive()