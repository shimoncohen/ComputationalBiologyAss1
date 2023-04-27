import numpy as np

def clip(idxs: np.array, rows, cols):
    """
    Remove indexes that exceed the given dimentions.

    Args:
        idxs (np.array): given indexes
        rows (_type_): wanted num of rows
        cols (_type_): wanted num of columns

    Returns:
        _type_: clipped indexes to fit given dimensions
    """
    res = []
    for r, c in idxs:
        if r < 0 or r >= rows or c < 0 or c >= cols:
            continue
        res.append([r, c])
    return res

def wrap(idxs: np.array, rows, cols):
    """
    Fix given indexes in a cyclic calculation to fit the given dimentions.

    Args:
        idxs (np.array): given indexes
        rows (_type_): wanted num of rows
        cols (_type_): wanted num of columns

    Returns:
        _type_: wrapped indexes to fit given dimensions
    """
    res = []
    for r, c in idxs:
        r = (r + rows) % rows
        c = (c + cols) % cols
        res.append([r, c])
    return res