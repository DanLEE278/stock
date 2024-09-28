import pandas as pd

# Unofficial Stretegy: Relative Market Strength Index
def rmsi(market: pd.DataFrame, stockprice:pd.DataFrame)-> tuple[dict,bool]:
    # TODO: compare market performamce with individual stock price
    # TODO: calculate rsi price index, select market and calculate recent rsi score
    # TODO: is it worth coding for mid, long-term stock??
    market_index = round((market.shift(-1).Close - market.Close) / market.Close * 100,2)
    stock_index = round((stockprice[-23:].shift(-1).Close - stockprice[-23:].Close) / stockprice[-23:].Close * 100,2)
    rmsi = {}
    try:
        for idx, bool in enumerate(market_index > stock_index):
            if bool:
                fluctuation = -(market_index[idx]-stock_index[idx])
            else:
                fluctuation = stock_index[idx]-market_index[idx]
            date = str(stock_index.index.date[idx].year) + "_" + str(stock_index.index.date[idx].month) + "_" + str(stock_index.index.date[idx].day)
            rmsi.update({f"{date}": fluctuation})
    except:
        return 0
    
    return sum(1 for x in rmsi.values() if x > 0)

# Official Stretegy:
def rsi(stockprice: pd.DataFrame)-> tuple[dict, bool]:
    pass

# Official Stretegy: Expert Buy Opinion -> returns buy percentage
def buystrength(opinion: pd.DataFrame)-> tuple[dict,bool]:
    buy_strength = {}
    for idx in range(len(opinion)):
        if sum(opinion.loc[idx][1:6]) != 0:
            buy_strength.update({f"{idx}": int(sum(opinion.loc[idx][1:3]) / sum(opinion.loc[idx][1:6])*100)})
            # buy_strength.append(int(sum(opinion.loc[idx][1:3]) / sum(opinion.loc[idx][1:6])*100))
        else:
            buy_strength.update({f"{idx}": 0})
    return buy_strength

# Official Stretegy: EPS Growth -> returns Yearly EPS
def eps_growth(income_stmt: list)-> dict:
    eps = {}
    if len(income_stmt.columns) != 0:
        for item in income_stmt.columns: 
            try:
                eps.update({item: income_stmt[item]['Basic EPS']})
            except:
                pass
    return eps

# Moving Average
# def moving(average):