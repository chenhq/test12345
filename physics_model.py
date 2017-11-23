import numpy as np


def angle_size(x, y):
    return np.arctan2(x, y)


def acceleration(alpha, drag_ratio):
    a = np.sin(alpha) - np.cos(alpha) * drag_ratio
    return a


def velocity(v0, a, s):
    vt_square = np.square(v0) + 2 * a * s
    if vt_square < 0:
        vt = 0
    else:
        vt = np.sqrt(vt_square)
    return vt