# coding: utf-8
import numpy as np
import pandas as pd
from talib.abstract import *


def double_ma_stratege(ohlcv, ma_fast_window, ma_slow_window):
    ma_fast = SMA(ohlcv, timeperiod=ma_fast_window, price='close')
    ma_slow = SMA(ohlcv, timeperiod=ma_slow_window, price='close')
    signal = pd.Series(index=ohlcv.index)
    signal.loc[:] = np.nan
    signal.loc[ma_fast > ma_slow] = 1
    return signal