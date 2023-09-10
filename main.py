# PYTHON BASE 
import FinanceDataReader as fdr

# CUSTOM MODULE
from utils import avg_move_line

class GetStrategy():
    def __init__(self):
        self.kr_stocks = fdr.StockListing('KRX')
        print(self.kr_stocks)
        pass
        
    def strategy_aggresive(self):
        
        pass
        
    def strategy_conservative(self):
        pass
    
    def strategy_neutral(self):
        pass    
    

df_krx = fdr.StockListing('KRX')
df_krx.head()

print(df_krx.head())

if __name__ == "__main__":
    stretegy = GetStrategy()
    