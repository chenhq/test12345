import numpy as np
import pandas as pd

def signal_by_wave(ohlcv, timeperiod, threshold, price='close'):
    signals = pd.Series(index=ohlcv.index)
    for idx in range(len(ohlcv)):
        cur_price = ohlcv.iloc[idx][price]
        next_prices = ohlcv.iloc[idx+1:idx+timeperiod][price].values
        if len(next_prices) < 1:
            break
        min_value = next_prices.min()
        max_value = next_prices.max()
        argmax = next_prices.argmax()
        argmin = next_prices.argmin()
        print("min_value: {}, max_value: {}, argmax: {}, argmin: {}, cur_price: {}".format(min_value, max_value, argmax, argmin, cur_price))

        signal = np.nan
        if cur_price <= min_value:
            max_returns = (max_value / cur_price) - 1
            if max_returns > threshold:
                signal = 1
        elif cur_price >= max_value:
            max_returns = 1 - (min_value / cur_price)
            if max_returns > threshold:
                signal = -1
        else:
            short_returns = 1 - (min_value / cur_price)
            long_returns = (max_value / cur_price) - 1
            if argmin < argmax:
                if short_returns > threshold:
                    signal = -1
                elif long_returns > threshold:
                        signal = 1
            else:
                if long_returns > threshold:
                    signal = 1
                elif short_returns > threshold:
                    signal = -1

            signals.iloc[idx] = signal
    return signals
