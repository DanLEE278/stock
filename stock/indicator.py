import pandas as pd

# Relative Strength Index
def rsi(price:list)-> float:
    pass
    rsi = 0
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
def eps_growth(income_stmt: list)-> tuple[dict,bool]:
    eps = {}
    if len(income_stmt.columns) != 0:
        for item in income_stmt.columns: 
            eps.update({item: income_stmt[item]['Basic EPS']})
            
        # year1 = int(income_stmt['2023-12-31']['Basic EPS'])
        # year2 = int(income_stmt['2022-12-31']['Basic EPS'])
        # year3 = int(income_stmt['2021-12-31']['Basic EPS'])
        # eps.update({"2023": year1})
        # eps.update({"2022": year2})
        # eps.update({"2021": year3})
    else:
        return False

# Moving Average
# def moving(average):