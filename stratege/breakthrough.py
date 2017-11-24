# coding: utf-8
import numpy as np
import pandas as pd


def break_extremal_point(ohlcv, timeperiod=60, prices=['open', 'high', 'low', 'close'], close_price='close'):
    extremal_point = pd.DataFrame(index=ohlcv.index)
    extremal_point['max'] = ohlcv.loc[:, prices].max(axis=1)
    extremal_point['min'] = ohlcv.loc[:, prices].max(axis=1)

    extremal_point["rolling_max"] = extremal_point['max'].rolling(timeperiod).apply(lambda x: np.max(x[:-1]))
    extremal_point["rolling_min"] = extremal_point['min'].rolling(timeperiod).apply(lambda x: np.min(x[:-1]))

    signal = pd.Series(index=ohlcv.index)

    signal[ohlcv[close_price] > extremal_point["rolling_max"]] = 1
    signal[ohlcv[close_price] < extremal_point["rolling_min"]] = -1
    return signal
