import numpy as np
import pandas as pd
from physics_model import *
import matplotlib.pyplot as plt


market = pd.read_csv("~/cs_market.csv", parse_dates=["date"], dtype={"code": str})

# market = pd.read_csv("E:\market_data/cs_market.csv", parse_dates=["date"], dtype={"code": str})

ohlcv = market.drop(["Unnamed: 0", "total_turnover", "limit_up", "limit_down"], axis=1)

ohlcv = ohlcv.set_index('date')

zz500 = ohlcv[ohlcv["code"] == "000725.XSHE"].drop("code", axis=1).tail(50)
zz500['close'].plot(figsize=(21, 7))
plt.show()

pct_change = (zz500['close'] / zz500['close'].shift(1) - 1).fillna(0)
pct_change.name = "pct_chg"

test = pd.concat([zz500['close'], pct_change], axis=1)

degree = 30
v_init_timeperiod = 1.5
v_threshod = 1.5
window = 5

std = pct_change.std()
drag_ratio = np.tan(np.pi * degree / 360)
v_init = np.sqrt(2 * drag_ratio * std * v_init_timeperiod)
v0 = v_init

test1 = test.copy()
test1['result'] = np.nan
for idx, row in test1.iterrows():
    alpha = angle_size(row['pct_chg'], std)
    degree = int(360 * alpha/(2 * np.pi))
    print(degree)
    a = acceleration(alpha, drag_ratio)
    s = std/np.cos(alpha)
    vt = velocity(v0, a, s)
    if vt > v_threshod * v_init:
        test1.loc[idx, 'result'] = 1
        speed_ratio = vt / v0
        print(speed_ratio)
        v0 = vt
    elif vt > 0:
        test1.loc[idx, 'result'] = 0
        v0 = vt
        speed_ratio = vt / v0
        print(speed_ratio)
    else:
        test1.loc[idx, 'result'] = -1
        v0 = v_init

test1 = test1.reset_index().reset_index()

fig, ax = plt.subplots(1, figsize=(21, 7))
test1.plot(x='index', y='close', figsize=(21, 7), ax=ax)
test1[test1['result']>0].plot.scatter(x='index', y='close', s=30, c='r', figsize=(21, 7), ax=ax)
test1[test1['result']<0].plot.scatter(x='index', y='close', s=30, c='g', figsize=(21, 7), ax=ax)