#!/usr/bin/env python3


from sys import argv
import json
import requests
import pandas as pd
import numpy as np
from mpl_finance import candlestick_ohlc
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import techs


plt.style.use('ggplot')

stock = argv[1]
time = argv[2]
tech = argv[3]
if len(argv) > 4:
    arg1 = argv[4]
else:
    arg1 = None


def GetStockDataFrame(time, stock):

    if False:
        pass
    else:
        print("Getting", time, "stock data for", stock)
        url = 'https://api.iextrading.com/1.0/stock/'+stock+'/chart/'+time
        r = requests.get(url)
        print(url)

        print("Parsing data.")
        rjson = r.text

        rdata = json.loads(rjson)

        dates = []
        openprices = []
        highprices = []
        lowprices = []
        closeprices = []
        volumes = []

        for i in rdata:
            date = i['date']
            dates.append(date)
            openprices.append(float(i['open']))
            highprices.append(float(i['high']))
            lowprices.append(float(i['low']))
            closeprices.append(float(i['close']))
            volumes.append(float(i['volume']))

        index = pd.DatetimeIndex(dates, dtype='datetime64[ns]')
        o = pd.Series(openprices, index=index)
        h = pd.Series(highprices, index=index)
        l = pd.Series(lowprices, index=index)
        c = pd.Series(closeprices, index=index)
        v = pd.Series(volumes, index=index)
        d = { 'Open' : o,
              'High' : h,
              'Low' : l,
              'Close' : c}

        return pd.DataFrame(d)


def Backtest(data, tech):
    pass


def PlotData(data):
    print("Plotting.")

    # Changing dates to floating point, also moves Date out of index
    df_ohlc = data.reset_index()
    df_ohlc['index'] = df_ohlc['index'].map(mdates.date2num)
    df_ohlc.rename(columns={'index': 'Date'}, inplace=True)

    # Rearrange columns for ohlc
    columns = ['Date', 'Open', 'High','Low','Close']
    df_ohlc = df_ohlc[columns]

    fig = plt.figure()
    ax1 = plt.subplot()
    ax1.xaxis_date()

    candlestick_ohlc(ax1, df_ohlc.values, width=.5, colorup='g', colordown='r')

    plt.ylabel("Price")
    plt.xlabel("Date")


def PlotTech(data, tech, arg1 = None):
    
    index = data.index
    lines = []
    if tech == 'SMA':
        days = int(arg1)
        vals = techs.SMA(data["Close"].tolist()).calc(days)
        lines.append(pd.Series(vals, index=index))
    elif tech == 'EMA':
        days = int(arg1)
        vals = techs.EMA(data["Close"].tolist()).calc(days)
        lines.append(pd.Series(vals, index=index))
    elif tech == 'MACD':
        macdvals, macdsignal = techs.MACD(data['Close'].tolist()).calc()
        lines.append(pd.Series(macdvals, index=index))
        lines.append(pd.Series(macdsignal, index=index))

        #mvs.plot()#secondary_y=True)
        #mss.plot()#secondary_y=True)
    for line in lines:
        line.plot()


data = GetStockDataFrame(time, stock)

PlotData(data)
PlotTech(data, tech, arg1)

plt.show()
