import numpy as np
import pandas as pd
import pytest
from pandas.testing import assert_series_equal

from compressio.compression_algorithms import (
    compress_complex,
    compress_float,
    compress_integer,
)


@pytest.mark.parametrize(
    "series,func,before,expected",
    [
        (
            pd.Series([complex(10, 10)], dtype=np.complex128),
            compress_complex,
            np.complex128,
            np.complex64,
        ),
        (
            pd.Series([complex(10, 10)], dtype=np.complex64),
            compress_complex,
            np.complex64,
            np.complex64,
        ),
        (
            pd.Series([complex(10e100, 10)], dtype=np.complex128),
            compress_complex,
            np.complex128,
            np.complex128,
        ),
        (
            pd.Series([10.0, 100.0, 1000.0], dtype=np.float64),
            compress_float,
            np.float64,
            np.float16,
        ),
        (pd.Series([0, 1, 2, 3], dtype=np.int64), compress_integer, np.int64, np.int8),
        (
            pd.Series([np.iinfo(np.int8).max + 1], dtype=np.int64),
            compress_integer,
            np.int64,
            np.uint8,
        ),
        (
            pd.Series([np.iinfo(np.uint8).max + 1], dtype=np.int64),
            compress_integer,
            np.int64,
            np.int16,
        ),
        (
            pd.Series([np.iinfo(np.int16).max + 1], dtype=np.int64),
            compress_integer,
            np.int64,
            np.uint16,
        ),
        (
            pd.Series([np.iinfo(np.uint16).max + 1], dtype=np.int64),
            compress_integer,
            np.int64,
            np.int32,
        ),
        (
            pd.Series([np.iinfo(np.int32).max + 1], dtype=np.int64),
            compress_integer,
            np.int64,
            np.uint32,
        ),
        (
            pd.Series([np.iinfo(np.uint32).max + 1], dtype=np.int64),
            compress_integer,
            np.int64,
            np.int64,
        ),
        (
            pd.Series([0, 1, 2, 3, 300], dtype=np.int64),
            compress_integer,
            np.int64,
            np.int16,
        ),
        (
            pd.Series([-1, 0, 1, 2, 3, 300], dtype=np.int64),
            compress_integer,
            np.int64,
            np.int16,
        ),
        (
            pd.Series([np.nan, 1], dtype=np.float64),
            compress_float,
            np.float64,
            np.float16,
        ),
    ],
)
def test_compress_series(series, func, before, expected):
    assert series.dtype == before
    compressed_series = func(series)
    assert compressed_series.dtype == expected or isinstance(
        compressed_series.dtype, expected
    )

    assert_series_equal(series, compressed_series, check_dtype=False)
