import numpy as np

def clip(idxs: np.array, rows, cols):
    res = []
    for r, c in idxs:
        if r < 0 or r >= rows or c < 0 or c >= cols:
            continue
        res.append([r, c])
    return res

def wrap(idxs: np.array, rows, cols):
    res = []
    for r, c in idxs:
        r = (r + rows) % rows
        c = (c + cols) % cols
        res.append([r, c])
    return res