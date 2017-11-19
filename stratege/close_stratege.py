# coding: utf-8
import numpy as np
from talib.abstract import *


def max_loss(ohlcv, open_idx, current_idx, open_signal, loss_pct, loss_value=0):
    if open_signal == 0:
        return 0
    elif open_signal > 0:
        direction = 1.0  # long
    else:
        direction = -1.0  # short

    init_value = ohlcv.loc[open_idx]['close']
    cur_value = ohlcv.loc[current_idx]['close']
    cur_return = (cur_value - init_value) * direction

    if loss_pct == 0:
        loss_pct = loss_value * 1.0 / init_value
    if loss_value == 0:
        loss_value = init_value * loss_pct
    if cur_return < - loss_value and cur_return / init_value < -loss_pct:
        return -open_signal, True
    else:
        return np.nan, False


def close_by_atr(ohlcv, open_idx, current_idx, open_signal, atr_times, atr_timeperiod =14):
    direction = 0
    if open_signal == 0:
        return 0
    elif open_signal > 0:
        direction = 1.0  # long
    else:
        direction = -1.0  # short

    length = len(ohlcv[:current_idx]) + 1
    if length >= atr_timeperiod:
        atr = ATR(ohlcv.iloc[length - atr_timeperiod:length], atr_timeperiod)[-1]
    else:
        atr = ATR(ohlcv.iloc[:length], length)[-1]

    if direction > 0:
        max_value = ohlcv[open_idx:current_idx]['close'].max()

        if ohlcv.loc[current_idx]['close'] < max_value - atr_times * atr:
            return -open_signal, True
        else:
            return np.nan, False

    elif direction < 0:
        min_value = ohlcv[open_idx:current_idx]['close'].min()

        if ohlcv.loc[current_idx]['close'] > min_value + atr_times * atr:
            return -open_signal, True
        else:
            return np.nan, False


def close_MaxLoss_ATR(ohlcv, open_idx, current_idx, open_signal, loss_pct, atr_times, atr_timeperiod=14):
    close_signal, end = max_loss(ohlcv, open_idx, current_idx, open_signal, loss_pct)
    if end:
        return close_signal, end

    close_signal, end = close_by_atr(ohlcv, open_idx, current_idx, open_signal, atr_times, atr_timeperiod)
    return close_signal, end