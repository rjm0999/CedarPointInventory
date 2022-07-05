from pandas import *


class ValueNotFoundError(Exception):
    def __init__(self):
        super().__init__(self)


def pd_index_of(df, col, val):
    idx = 0
    while idx < df.shape[0]:
        if df[col].iat(idx, 0) == val:
            return idx
        idx += 1
    return ValueNotFoundError
