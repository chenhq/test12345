# coding: utf-8
import numpy as np
import pandas as pd


def position2return(ohlcv, position, price="close"):
    pct_changes = ohlcv[price] / ohlcv[price].shift(1) - 1
    returns = pct_changes * position
    return returns


def signal2postion(open_signal, close_signal):
    # 在信号下一日交易
    position_changes = open_signal.shift(1).fillna(0).cumsum() + close_signal.shift(1).fillna(0).cumsum()
    position = position_changes.cumsum()
    return position


def signal2return(ohlcv, open_signal, close_signal):
    position = signal2postion(open_signal, close_signal)
    returns = position2return(ohlcv, position)
    return returns


# 全量信号转变为增量信号
def signal_full2increment(full_signal):
    increment_signal = full_signal.copy()
    # 信号前值
    old_value = np.nan
    for idx, value in increment_signal.iteritems():
        # 前值为NaN或者反向信号，则当前信号为新信号
        if np.isnan(old_value) or old_value * value < 0:
            full_value = value
        # 如果信号和前值信号相同， 则新增信号为两者之差
        else:
            full_value = value - old_value

        increment_signal[idx] = full_value
        old_value = value
    return increment_signal


# 增量信号转化为全量信号
def signal_increment2full(increment_signal):
    full_signal = increment_signal.copy()
    # 信号前值
    old_value = np.nan

    for idx, value in full_signal.iteritems():
        # 前值为NaN或者反向信号，则当前信号为新信号
        if np.isnan(old_value) or old_value * value < 0:
            full_value = value
        # 如果信号和前值信号相同， 则全量信号为两者之和
        else:
            full_value = value + old_value

        full_signal[idx] = full_value
        old_value = full_value
    return full_signal


def close_signal_generate(ohlcv, open_signal, computing_func, **kwargs):
    open_signal.name = "open_signal"
    df = pd.concat([ohlcv, open_signal], axis=1)
    df['close_signal'] = np.nan

    # 初始化
    i_open_idx = 0
    length = len(df)
    while i_open_idx < length:
        open_idx = df.index[i_open_idx]
        # print("i_open_idx: {}, open_idx: {}".format(i_open_idx, open_idx))
        open_signal = df.loc[open_idx]['open_signal']
        if np.isnan(open_signal):
            open_signal = 0

        if open_signal != 0:
            i_close_idx = i_open_idx
            while i_close_idx < length:
                close_idx = df.index[i_close_idx]
                close_signal = computing_func(df, open_idx, close_idx, open_signal, **kwargs)
                if np.isnan(close_signal):
                    i_close_idx += 1
                    continue

                if np.isnan(df.loc[close_idx]['close_signal']):
                    df.loc[close_idx, 'close_signal'] = close_signal
                else:
                    df.loc[close_idx]['close_signal'] = df.loc[close_idx]['close_signal'] + close_signal

                open_signal = open_signal + close_signal

                if abs(open_signal) <= 0.001:
                    break

        i_open_idx += 1

    # df.to_csv("sss3.csv")
    return df['close_signal']


# def dummy_close_signal(open_signal):
#     close_signal = pd.Series(index=open_signal.index)
#     close_signal[open_signal == 0] = -open_signal.shift(1)
#     close_signal[(close_signal == 0)] = np.nan
#     close_signal = close_signal.fillna(method='ffill')
#     close_signal.loc[(open_signal.fillna(0) != 0)] = 0
#     close_signal = close_signal.fillna(0)
#     return close_signal



# def compose_open_close_signal(open_siganl, close_signal):
#     signals = pd.concat([open_signal, close_signal], axis=1).copy()
#     signals.columns = ["open_signal", "close_signal"]
#     new_signal = pd.Series(index=signals.index)
#
#     signal = 0
#     for idx, row in signals.iterrows():
#         # long
#         if row["open_signal"] > 0:
#             if row["close_signal"] < 0:
#                 sum_signal = row["open_signal"] + row["close_signal"]
#                 if sum_signal < 0:
#                     new_signal.loc[idx, 'open_signal'] = 0
#                 else:
#                     signals.loc[idx, 'open_signal'] = sum_signal
#         else if row["open_signal"] < 0:
#             if row["close_signal"] > 0:
#                 sum_signal = row["open_signal"] + row["close_signal"]
#                 if sum_signal < 0:
#                     signals.loc[idx, 'open_signal'] = 0
#                 else:
#                     signals.loc[idx, 'open_signal'] = sum_signal

# # increment(增量)
# def signals_to_position(ohlcv, open_signal, close_signal, signal_type='full'):
#     pct_chg = (ohlcv['close'] / ohlcv['close'].shift(1)) - 1
#     returns = pd.Series(index=pct_chg.index)


# def open_signal_generate(ohlcv, computing_func, **kwargs):
#     pass

#
# def max_return(df, open_idx, current_idx, open_signal, return_pct, return_value=0):
#     if open_signal == 0:
#         return 0
#     elif open_signal > 0:
#         direction = 1.0  # long
#     else:
#         derection = -1.0  # short
#
#     init_value = df.loc[open_idx]['open']
#     cur_value = df.loc[current_idx]['close']
#     cur_return = (cur_value - init_value) * derection
#
#     if return_pct == 0:
#         return_pct = return_value * 1.0 / init_value
#     if return_value == 0:
#         return_value = init_value * return_pct
#     if cur_return > return_value and cur_return / init_value > return_pct:
#         return -open_signal
#     else:
#         return 0
#
#
#
# def close_signal_compose(open_signal, close_signal_1, close_signal_2, how):
#     df = pd.concat([open_signal, close_signal_1, close_signal_2], axis=1)
#     df.columns = ['open_signal', 'close_signal_1', 'close_signal_2']
#     df['new_close_signal'] = 0
#
#     open_status = False
#     open_signal = 0
#     signal_1 = 0
#     signal_2 = 0
#     for idx, row in df.iterrows():
#         if open_status:
#             if (df.loc[idx]['close_signal_1'] * open_signal < 0):
#                 signal_1 = df.loc[idx]['close_signal_1']
#             if (df.loc[idx]['close_signal_2'] * open_signal < 0):
#                 signal_2 = df.loc[idx]['close_signal_2']
#
#             if how == "or":
#                 if signal_1 != 0 or signal_2 != 0:
#                     open_status = False
#                     df.loc[idx]['new_close_signal'] = max(signal_1, signal_2)
#
#             if how == "and":
#                 if df.loc[idx]['close_signal_1'] > 0 and df.loc[idx]['close_signal_2'] > 0:
#                     open_status = False
#                     df.loc[idx]['new_close_signal'] = min(signal_1, signal_2)
#         else:
#             if df.loc[idx, 'open_signal'] != 0:
#                 open_status = True
#                 open_signal = df.loc[idx, 'open_signal']
#                 signal_1 = 0
#                 signal_2 = 0
#     return df['new_close_signal']
#
#
# # In[ ]:
#
#

#
#
# # In[ ]:
#
#
# def stop_by_kline_moon(df, open_idx, current_idx):
#     if position <= 0:
#         return 0
#
#     if df.loc[current_idx]['close'] < df.loc[current_idx]['open']:
#         return -position
#
#
# # In[ ]:
#
#
# def stop_by_breakthrough(market, open_signal):
#     pass
#
#
# # In[ ]:
#
#
# def stop_loss_by_std(market, open_signal, std_times):
#     pass
#
#
# # In[ ]:
#
#
# def stop_loss_by_ma(market, open_signal, n_ma):
#     pass
#
#
# # In[ ]:
#
#
# def stop_loss_by_kline(market, open_signal, k_line_features):
#     pass
#
#
# # In[ ]:
#
#
# def stop_loss_by_macd(market, open_signal):
#     pass
#
#
# # In[ ]:
#
#
# def stop_loss_by_kdj(market, open_signal):
#     pass
#
#
# # In[ ]:
#
#
# def stop_lost_by_sar(ma):
#     pass
#
# # In[ ]:
#
#
#
