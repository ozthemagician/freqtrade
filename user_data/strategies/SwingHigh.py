from freqtrade.strategy.interface import IStrategy
from typing import Dict, List
from functools import reduce
from pandas import DataFrame

import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
import numpy

__author__ = "Kevin Ossenbrück"
__copyright__ = "Free For Use"
__credits__ = ["Bloom Trading, Mohsen Hassan"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Kevin Ossenbrück"
__email__ = "kevin.ossenbrueck@pm.de"
__status__ = "Live"

# CCI timerperiods and values
cciBuyTP = 17
cciBuyVal = -82
cciSellTP = 11
cciSellVal = 140

# RSI timeperiods and values
rsiBuyTP = 49
rsiBuyVal = 78
rsiSellTP = 39
rsiSellVal = 28

class SwingHigh(IStrategy):
    timeframe = '15m'

    stoploss = -0.331

    # minimal_roi = {"0": 0.27058, "33": 0.0853, "64": 0.04093, "244": 0}
    minimal_roi = {
        "0": 0.283,
        "92": 0.087,
        "241": 0.04,
        "436": 0
    }

    trailing_stop = True
    trailing_stop_positive = 0.34
    trailing_stop_positive_offset = 0.361
    trailing_only_offset_is_reached = True

    def informative_pairs(self):
        return []

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['cci-' + str(cciBuyTP)] = ta.CCI(dataframe, timeperiod=cciBuyTP)
        dataframe['cci-' + str(cciSellTP)] = ta.CCI(dataframe, timeperiod=cciSellTP)

        dataframe['rsi-' + str(rsiBuyTP)] = ta.RSI(dataframe, timeperiod=rsiBuyTP)
        dataframe['rsi-' + str(rsiSellTP)] = ta.RSI(dataframe, timeperiod=rsiSellTP)

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                    (dataframe['cci-' + str(cciBuyTP)] < cciBuyVal) &
                    (dataframe['rsi-' + str(rsiBuyTP)] < rsiBuyVal)
            ),
            'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                    (dataframe['cci-' + str(cciSellTP)] > cciSellVal) &
                    (dataframe['rsi-' + str(rsiSellTP)] > rsiSellVal)
            ),
            'sell'] = 1

        return dataframe