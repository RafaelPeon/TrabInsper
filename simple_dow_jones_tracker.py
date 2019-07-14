from fhdataapi import BBG
import pandas as pd
from datetime import date, timedelta
from pandas.tseries.offsets import BDay
import matplotlib.pyplot as plt
import math
import numpy as np

bbg = BBG()

start_date = pd.to_datetime('2000-01-01').date()
end_date = pd.to_datetime('today')
ann_factor = 252

stocks = [
    "MMM",
    "AXP",
    "AAPL",
    "BA",
    "CAT",
    "CVX",
    "CSCO",
    "KO",
    "DOW",
    "XOM",
    "GS",
    "HD",
    "IBM",
    "INTC",
    "JNJ",
    "JPM",
    "MCD",
    "MRK",
    "MSFT",
    "NKE",
    "PFE",
    "PG",
    "TRV",
    "UNH",
    "UTX",
    "VZ",
    "V",
    "WMT",
    "WBA",
    "DIS",
]

for stock_prices in stocks:
    bbg = bbg.fetch_series(securities = stock_prices + 'USDCR CMPN Curncy',
                            fields='LAST_PRICE',
                            startdate=start_date,
                            enddate=end_date)
    print(bbg)