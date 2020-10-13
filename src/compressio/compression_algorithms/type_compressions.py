from typing import Callable, Iterable, Type, Union

import numpy as np
import pandas as pd

nan_value = pd.NA if hasattr(pd, "NA") else np.nan


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
    test_sequence = (dtype for dtype in type_options if tester(dtype))
    return next(test_sequence)


def compress_sparse_missing(series: pd.Series) -> pd.Series:
    """Compresses the data by using the SparseArray data structure for missing values/nans

    :param series: series to compress
    :return: the (compressed) series
    """
    if not series.hasnans:
        return series

    # numpy dtypes
    fill_value = np.nan
    test_dtype = series.dtype

    # pandas dtypes
    if pd.api.types.is_extension_array_dtype(test_dtype):
        if test_dtype != pd.CategoricalDtype():
            if hasattr(test_dtype, "numpy_dtype"):
                test_dtype = test_dtype.numpy_dtype
            elif hasattr(test_dtype, "type"):
                test_dtype = test_dtype.type
            else:
                raise ValueError(f"Couldn't obtain the dtype of {type(test_dtype)}")
            fill_value = nan_value
        else:
            test_dtype = np.object

    new_series = pd.Series(
        pd.arrays.SparseArray(
            series[series.notnull()], dtype=test_dtype, fill_value=fill_value
        )
    )
    if new_series.memory_usage(deep=True) < series.memory_usage(deep=True):
        return new_series

    return series


def compress_float(series: pd.Series) -> pd.Series:
    """
    Compressing to half-precision floating-point format can degrade computational performance
    CPUs often do not have native support for 16-bit floats and simulate the data type.
    https://en.wikipedia.org/wiki/Half-precision_floating-point_format
    https://stackoverflow.com/a/49997863/470433
    https://stackoverflow.com/a/15341193/470433
    :param series:
    :return:
    """
    minv, maxv = series.min(), series.max()
    tester = type_tester(minv, maxv, np.finfo)
    test_types = [np.float16, np.float32, np.float64]

    compressed_type = get_compressed_type(test_types, tester)
    return series.astype(compressed_type)


def compress_integer(series: pd.Series) -> pd.Series:
    minv, maxv = series.min(), series.max()
    tester = type_tester(minv, maxv, np.iinfo)

    test_types = [
        np.int8,
        np.uint8,
        np.int16,
        np.uint16,
        np.int32,
        np.uint32,
        np.int64,
        np.uint64,
    ]

    compressed_type = get_compressed_type(test_types, tester)

    if series.hasnans:
        name = np.dtype(compressed_type).name
        if np.iinfo(compressed_type).min >= 0:
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
        if new_series.memory_usage(deep=True) < series.memory_usage(deep=True):
            return new_series
    except:  # noqa
        pass
    return series


def compress_datetime(series: pd.Series) -> pd.Series:
    try:
        new_series = series.astype("category")
        if new_series.memory_usage(deep=True) < series.memory_usage(deep=True):
            return new_series
    except:  # noqa
        pass
    return series


# TODO: Create a period type which checks if dates fall in well defined interval ranges?
# we can get substantial memory savings from compressing these.
