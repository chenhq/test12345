# coding: utf-8
import numpy as np
import pandas as pd


def dummy_stratege(ohlcv):
    signal = pd.Series(index=ohlcv.index, data=np.full((len(ohlcv),), 1.0))
    return signal
