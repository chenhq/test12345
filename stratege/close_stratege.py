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
    # print("init_value: {0:.2f}, cur_value: {1:.2f}, cur_return: {2:.2f}".format(init_value, cur_value, cur_return))

    if loss_pct == 0:
        loss_pct = loss_value * 1.0 / init_value
    if loss_value == 0:
        loss_value = init_value * loss_pct
    if cur_return < - loss_value and cur_return / init_value < -loss_pct:
        # print("######### match ##########")
        return -open_signal
    else:
        return np.nan


def close_by_atr(ohlcv, open_idx, current_idx, open_signal, atr_times, atr_timeperiod=14):
    direction = 0
    if open_signal == 0:
        return 0
    elif open_signal > 0:
        direction = 1.0  # long
    else:
        direction = -1.0  # short

    # ATR指标跨天，数据量为atr_timeperiod + 1
    length = len(ohlcv.loc[:current_idx])
    atr_timeperiod = min(length-1, atr_timeperiod)
    start = max(length - atr_timeperiod - 1, 0)
    # print(ATR(ohlcv.iloc[start:length], atr_timeperiod))
    if len(ohlcv.iloc[start:length]) < 2:
        return np.nan

    atr = ATR(ohlcv.iloc[start:length], atr_timeperiod)[-1]

    # print("atr: {0:.2f}".format(atr))

    if direction > 0:
        max_value = ohlcv[open_idx:current_idx]['close'].max()

        if ohlcv.loc[current_idx]['close'] < max_value - atr_times * atr:
            # print("ohlcv.loc[current_idx]['close']: {0:.2f}, max_value: {1:.2f}, atr_times * atr: {2:.2f}".format(ohlcv.loc[current_idx]['close'], max_value, atr_times * atr))
            return -open_signal
        else:
            return np.nan

    elif direction < 0:
        min_value = ohlcv[open_idx:current_idx]['close'].min()

        if ohlcv.loc[current_idx]['close'] > min_value + atr_times * atr:
            return -open_signal
        else:
            return np.nan


def close_MaxLoss_ATR(ohlcv, open_idx, current_idx, open_signal, loss_pct, atr_times, atr_timeperiod=14):
    close_signal = max_loss(ohlcv, open_idx, current_idx, open_signal, loss_pct)
    if close_signal + open_signal < 0.01:
        return close_signal

    close_signal = close_by_atr(ohlcv, open_idx, current_idx, open_signal, atr_times, atr_timeperiod)
    return close_signal