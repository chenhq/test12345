import numpy as np
import pandas as pd
from tag_wave_direction import *
import matplotlib.pyplot as plt


# market = pd.read_csv("~/cs_market.csv", parse_dates=["date"], dtype={"code": str})
market = pd.read_csv("E:\market_data/cs_market.csv", parse_dates=["date"], dtype={"code": str})

ohlcv = market.drop(["Unnamed: 0", "total_turnover", "limit_up", "limit_down"], axis=1)

ohlcv = ohlcv.set_index('date')

test_data = ohlcv[ohlcv["code"] == "000725.XSHE"].drop("code", axis=1).tail(50)
test_data['close'].plot(figsize=(21, 7))
plt.show()

max_return_threshold = 0.1
return_per_count_threshold = 0.01
withdraw_threshold = 0.03
tag_wave_direction(test_data, max_return_threshold, return_per_count_threshold, withdraw_threshold)


# fig, ax = plt.subplots(1, figsize=(21, 7))
# test1.plot(x='index', y='close', figsize=(21, 7), ax=ax)
# test1[test1['result']>0].plot.scatter(x='index', y='close', s=30, c='r', figsize=(21, 7), ax=ax)
# test1[test1['result']<0].plot.scatter(x='index', y='close', s=30, c='g', figsize=(21, 7), ax=ax)