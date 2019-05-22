#!/usr/bin/env python3

"""
Arctos is a stock market price and technical indicator charting program. The
data is provided by IEX Cloud.
"""


from sys import argv
import json
import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import techs
from candlestick import candlestick_ohlc

plt.style.use('ggplot')


STOCK = argv[1]
TIME = argv[2]
TECH = argv[3]
if len(argv) > 4:
    TECHARG = argv[4]
else:
    TECHARG = None

def get_stock_data_frame(time, stock):

    """
    Requests data from the IEX API and creates Pandas DataFrame
    """

    print("Getting", time, "stock data for", stock)
    url = 'https://api.iextrading.com/1.0/stock/'+stock+'/chart/'+time
    req = requests.get(url)
    print(url)

    print("Parsing data.")
    rjson = req.text

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
    _open = pd.Series(openprices, index=index)
    high = pd.Series(highprices, index=index)
    low = pd.Series(lowprices, index=index)
    close = pd.Series(closeprices, index=index)
    data_frame_data = {'Open' : _open, 'High' : high, 'Low' : low, 'Close' : close}

    return pd.DataFrame(data_frame_data)


def plot_data(data):

    """
    Takes Pandas DataFrame with prices information and plots onto graph.
    """

    print("Plotting.")

    # Changing dates to floating point, also moves Date out of index
    df_ohlc = data.reset_index()
    df_ohlc['index'] = df_ohlc['index'].map(mdates.date2num)
    df_ohlc.rename(columns={'index': 'Date'}, inplace=True)

    # Rearrange columns for ohlc
    columns = ['Date', 'Open', 'High', 'Low', 'Close']
    df_ohlc = df_ohlc[columns]

    fig = plt.figure()
    ax1 = plt.subplot()
    ax1.xaxis_date()

    candlestick_ohlc(ax1, df_ohlc.values, width=.5, colorup='g', colordown='r')

    plt.ylabel("Price")
    plt.xlabel("Date")


def plot_tech(data, tech, techarg=None):

    """
    Plots technical indicator.
    """

    index = data.index
    lines = []
    if TECH == 'SMA':
        days = int(techarg)
        vals = techs.SMA(data["Close"].tolist()).calc(days)
        lines.append(pd.Series(vals, index=index))
    elif TECH == 'EMA':
        days = int(techarg)
        vals = techs.EMA(data["Close"].tolist()).calc(days)
        lines.append(pd.Series(vals, index=index))
    elif TECH == 'MACD':
        macdvals, macdsignal = techs.MACD(data['Close'].tolist()).calc()
        lines.append(pd.Series(macdvals, index=index))
        lines.append(pd.Series(macdsignal, index=index))

    for line in lines:
        line.plot()


data = get_stock_data_frame(TIME, STOCK)

plot_data(data)
plot_tech(data, TECH, TECHARG)

plt.show()
