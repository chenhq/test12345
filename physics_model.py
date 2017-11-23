import numpy as np


def angle_degree(x, y):
    return np.arctan2(x, y)


def acceleration(g, alpha, drag_ratio):
    a = g * np.sin(alpha) - g * np.cos(alpha) * drag_ratio
    return a


def velocity(v0, a, s):
    vt_square = np.square(v0) + 2 * a * s
    vt = np.sqrt(vt_square)
    if vt_square < 0:
        vt = -vt
    return vt