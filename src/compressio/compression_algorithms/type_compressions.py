from typing import Callable, Iterable, Type, Union

import numpy as np
import pandas as pd


def type_tester(
    minv: Union[int, float], maxv: Union[int, float], info_func: Callable
) -> Callable:
    def inner(dtype: Type[np.dtype]) -> bool:
        type_info = info_func(dtype)
        return minv >= type_info.min and maxv <= type_info.max

    return inner


def get_compressed_type(
    type_options: Iterable[Type[np.dtype]], tester: Callable
) -> Type[np.dtype]:
    for test_type in type_options:
        if tester(test_type):
            break

    return test_type


def compress_float(series: pd.Series) -> pd.Series:
    minv, maxv = series.min(), series.max()
    tester = type_tester(minv, maxv, np.finfo)
    test_types = [np.float16, np.float32, np.float64]

    compressed_type = get_compressed_type(test_types, tester)
    return series.astype(compressed_type)


def compress_integer(series: pd.Series) -> pd.Series:
    minv, maxv = series.min(), series.max()
    tester = type_tester(minv, maxv, np.iinfo)

    if minv >= 0:
        test_types = [np.uint8, np.uint16, np.uint32, np.uint64]
    else:
        test_types = [np.int8, np.int16, np.int32, np.int64]

    compressed_type = get_compressed_type(test_types, tester)

    if series.hasnans:
        name = np.dtype(compressed_type).name
        if minv >= 0:
            compressed_type = name[0:2].upper() + name[2:]
        else:
            compressed_type = name.capitalize()

    return series.astype(compressed_type)


def compress_complex(series: pd.Series) -> pd.Series:
    if series.dtype == np.complex64:
        return series

    real_part = series.apply(lambda x: x.real)
    imag_part = series.apply(lambda x: x.imag)

    minv_real, maxv_real = real_part.min(), real_part.max()
    minv_imag, maxv_imag = imag_part.min(), imag_part.max()

    test_real = type_tester(minv_real, maxv_real, np.finfo)
    test_imag = type_tester(minv_imag, maxv_imag, np.finfo)

    if test_real(np.float32) and test_imag(np.float32):
        return series.astype(np.complex64)

    return series


def compress_object(series: pd.Series) -> pd.Series:
    try:
        new_series = series.astype("category")
        if new_series.memory_usage() < series.memory_usage():
            return new_series
    except:
        pass
    return series


def compress_datetime(series: pd.Series) -> pd.Series:
    try:
        new_series = series.astype("category")
        if new_series.memory_usage() < series.memory_usage():
            return new_series
    except:
        pass
    return series


# TODO: Create a period type which checks if dates fall in well defined interval ranges?
# we can get substantial memory savings from compressing these.
