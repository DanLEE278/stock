import pandas as pd

# Relative Strength Index
def rsi(market: pd.DataFrame, stockprice:pd.DataFrame)-> tuple[dict,bool]:
    # TODO: compare market performamce with individual stock price
    # TODO: calculate rsi price index, select market and calculate recent rsi score
    # TODO: is it worth coding for mid, long-term stock??
    
    import pdb
    pdb.set_trace()
    return rsi

# Expert Buy Opinion -> returns buy percentage
def buystrength(opinion: pd.DataFrame)-> tuple[dict,bool]:
    buy_strength = {}
    for idx in range(len(opinion)):
        if sum(opinion.loc[idx][1:6]) != 0:
            buy_strength.update({f"{idx}": int(sum(opinion.loc[idx][1:3]) / sum(opinion.loc[idx][1:6])*100)})
            # buy_strength.append(int(sum(opinion.loc[idx][1:3]) / sum(opinion.loc[idx][1:6])*100))
        else:
            buy_strength.update({f"{idx}": 0})
    return buy_strength

# EPS Growth -> returns Yearly EPS
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