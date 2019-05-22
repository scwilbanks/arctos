
"""
This module provides the classes for each technical indicator.
"""

from operator import sub
import random
import numpy as np
import pandas as pd


class SMA:

    """
    Simple Moving Average
    """

    def __init__(self, prices):
        self.prices = prices

    def calc(self, day):

        """
        Returns list of Simple Moving Average of past "days" number of days.
        """

        prices = self.prices
        values = []
        nancount = 0
        for i in range(0, len(prices)):
            if np.isnan(prices[i]):
                values.append(np.nan)
                nancount += 1
            elif i < day-1+nancount:
                values.append(np.nan)
            elif i >= day-1+nancount:
                val = sum(prices[i-day+1:i+1])/float(day)
                values.append(val)
            else:
                return "ERROR"
        return values

class EMA:

    """
    Exponential Moving Average
    """
    
    def __init__(self, prices):
        self.prices = prices

    def calc(self, day):

        """
        Returns list of Exponential Moving Average of past "days" number of days.
        """

        prices = self.prices

        values = []
        multiplier = (2.0/(float(day)+1.0))
        nancount = 0

        for i in range(0, len(prices)):
            if np.isnan(prices[i]):
                values.append(np.nan)
                nancount += 1
            elif i < day-1+nancount:
                values.append(np.nan)
            elif i < day+nancount:
                start = sum(prices[i-day+1:i+1])/float(day)
                values.append(start)
            elif i >= day+nancount:
                values.append((prices[i] - values[i-1]) * multiplier + values[i-1])
            else:
                return "ERROR"
        return values

class MACD:

    """"
    Moving Average Convergence Divergence
    """

    def __init__(self, prices):
        self.prices = prices

    def calc(self):
        """
        Returns two lists:
            1) Differences between EMA12 and EMA26
            2) EMA9, "Signal line"
        The crossover between the two shows buy and sell signals
        """
        prices = self.prices
        values = list(map(sub, EMA(prices).calc(12), EMA(prices).calc(26)))
        signal = EMA(values).calc(9)
        return values, signal