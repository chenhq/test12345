<<<<<<< HEAD
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
=======
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
>>>>>>> 582efb50f5f21cc471dc67eaa9be4671d961bbc5
    return vt