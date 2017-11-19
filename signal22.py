import matplotlib.pylab as plt
from trade_signal import *
from stratege.ma import *
from stratege.dummy import *
from stratege.close_stratege import *

market = pd.read_csv("~/cs_market.csv", parse_dates=["date"], dtype={"code": str})

ohlcv = market.drop(["Unnamed: 0", "total_turnover", "limit_up", "limit_down"], axis=1)

ohlcv = ohlcv.set_index('date')

zz500 = ohlcv[ohlcv["code"] == "000001.XSHE"].drop("code", axis=1).tail(250)

zz500['close'].plot(figsize=(21, 7))


# dummy_returns = signal2return(zz500, dummy_stratege(zz500))
#
# double_ma_returns = signal2return(zz500, double_ma_stratege(zz500, 3, 20))

# c_dummy_returns = cumulate_return(dummy_returns)
# c_double_ma_returns = cumulate_return(double_ma_returns)

# pd.concat([c_dummy_returns, c_double_ma_returns], axis=1).plot(figsize=(21, 7))

f_double_ma_signal = double_ma_stratege(zz500, 3, 20)

i_double_ma_signal = signal_full2increment(f_double_ma_signal)

pd.concat([f_double_ma_signal, i_double_ma_signal], axis=1).tail(10)

open_signal_copy = i_double_ma_signal.copy()

ohlcv = zz500

colse_signal = close_signal_generate(ohlcv, open_signal_copy, close_MaxLoss_ATR, loss_pct=0.02, atr_times=0.5)

results = pd.DataFrame()

for int_lost_pct in range(1, 6):
    lost_pct = int_lost_pct / 100.0
    for int_atr_times in range(1, 20):
        atr_times = 0.1 * int_atr_times
        print("lost_pct: {:.2}, atr_times: {:.2}".format(lost_pct, atr_times))

        close_signal = close_signal_generate(ohlcv, open_signal_copy, close_MaxLoss_ATR, loss_pct=lost_pct, atr_times=atr_times)

        returns = signal2return(ohlcv, open_signal_copy, close_signal)

        returns.name = "lost{:.2}_atr{:.2}".format(lost_pct, atr_times)
        results = pd.concat([results, returns], axis=1)

results.to_csv("results.csv")

(results.fillna(0) + 1).cumprod().plot()
plt.show()


"""

df = pd.concat([ohlcv, open_signal_copy], axis=1)
df['close_signal'] = 0
open_status = False
open_singal = 0

returns = signal_to_return(zz500, signal)


cum_returns = (returns.fillna(0) + 1).cumprod()


pct_chg = zz500['close'] / zz500['close'].shift(1) - 1



(pct_chg.fillna(0) + 1).cumprod().plot(figsize=(21, 7))
cum_returns.plot(figsize=(21, 7))
new_cum_returns.plot(figsize=(21, 7))



cum_returns.name = 'cum_returns'
pd_cum_returns = cum_returns.reset_index().set_index("date")



bolling = BBANDS(pd_cum_returns, 20, 2, 2, price="cum_returns")


df = pd.concat([pd_cum_returns, bolling], axis=1)


df.plot(figsize=(21, 7))



new_cum_returns.plot(figsize=(21, 7))



df['signal'] = np.nan
df.loc[df["cum_returns"] > df["middleband"], 'signal'] = 1


df['signal_up'] = np.nan
df.loc[df["cum_returns"] > df["upperband"], 'signal_up'] = 1



upup = False
for idx, row in df.iterrows():
    if row['signal_up'] > 0:
        upup = True
        continue
    if np.isnan(row["signal"]):
        upup = False
        continue
    if upup and (row['signal'] > 0):
        df.loc[idx, 'signal'] = 0



new_returns = df['signal'].shift(1) * returns



new_cum_returns = (new_returns.fillna(0) + 1).cumprod()


new_cum_returns.plot(figsize=(21, 7))


close_signal = dummy_close_signal(open_signal)

from empyrical import *


sharpe_ratio(returns)

# In[ ]:


sharpe_ratio(new_returns)


# ## 信号

# 信号定义
#
# * 1 多
# * -1 空
# * 0 同前值(增量)
# * N/A 无

# In[26]:


increment_signal = signal_full2increment(open_signal)

# In[ ]:


full_signal = signal_increment2full(increment_signal)

# In[ ]:


allx = pd.concat([open_signal, full_signal, increment_signal], axis=1)

# In[ ]:


allx.to_csv("allx.csv")


# In[ ]:
"""