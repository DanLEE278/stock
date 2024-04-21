# PYTHON BASE 
import argparse
import pandas as pd
import FinanceDataReader as fdr
import matplotlib.pyplot as plt
from tqdm import tqdm

# CUSTOM MODULE
from stock.base import USStock   

if __name__ == "__main__":
    stretegy = USStock("usa")
    # stretegy.run()
    stretegy.strategy_aggresive()