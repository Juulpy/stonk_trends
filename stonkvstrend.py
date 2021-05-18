"""
By u/Shrevel

requirements:
1. open cmd
2. copy paste:
    pip install pytrends matplotlib yfinance pandas numpy

"""

from pytrends.request import TrendReq
from collections import Counter
import datetime
from matplotlib import pyplot as plt
from matplotlib import dates as mpl_dates
import yfinance as yf
import pandas as pd
import numpy as np


ticker = "GME" #ticker to download from Yahoo. Check if ticker exists on yahoo finance
kw_list = ["wallstreetbets"] #only one item supported.
country = '' #leave empty for world, input is Alpha-2 country code: https://www.iban.com/country-codes

# accepted periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
#not recommended above 3mo due to downloading times
yticker = yf.Ticker(ticker)
ticker_hist = yticker.history(period="3mo")

df_dates = list(ticker_hist.index)
df_close = list(ticker_hist["Close"])
df_volume = list(ticker_hist["Volume"])
for i in range(0,len(df_dates)):
    pdt = df_dates[i].to_pydatetime()
    df_dates[i] = pdt

plt.style.use('seaborn')
pytrends = TrendReq(hl='en-US', tz=360)

pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='', gprop='')
trendsdata = pytrends.get_historical_interest(kw_list, year_start=df_dates[0].year, month_start=df_dates[0].month, day_start=df_dates[0].day, hour_start=df_dates[0].hour, year_end=df_dates[-1].year, month_end=df_dates[-1].month, day_end=df_dates[-1].day, hour_end=df_dates[-1].hour, cat=0, geo='', gprop='', sleep=0)


values = trendsdata[kw_list[0]].tolist() #not supporting multiple trends yet
dates = trendsdata.index.tolist()

#plot everything
fig,ax1 = plt.subplots()
color='tab:red'
ax1.set_xlabel('Date')
ax1.set_ylabel('Google Trends: {}'.format(kw_list[0]),color=color)
ax1.plot(np.array(dates),np.array(values),color=color)
ax2 = ax1.twinx()


color = 'tab:blue'
ax2.set_ylabel('{} price'.format(ticker), color=color)
ax2.plot(df_dates,df_close,color=color)

plt.show()
