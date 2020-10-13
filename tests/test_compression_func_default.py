import numpy as np
import pandas as pd
import pytest
from pandas.testing import assert_series_equal
from visions import StandardSet

from compressio.compress import compress_func
from compressio.type_compressor import DefaultCompressor

bool_dtype = "boolean" if int(pd.__version__.split(".")[0]) >= 1 else "Bool"


@pytest.mark.parametrize(
    "series,before,expected",
    [
        (
            pd.Series([10.0, 100.0, np.iinfo(np.int16).max * 1.0], dtype=np.float64),
            np.float64,
            "int16",
        ),
        (pd.Series([np.nan, 1], dtype=np.float64), np.float64, "Int8"),
        (
            pd.Series([True, False, None, None, None, None, True, False] * 1000),
            np.object,
            bool_dtype,
        ),
    ],
)
def test_compress_series(series, before, expected):
    assert series.dtype == before
    compressed_series = compress_func(
        series,
        typeset=StandardSet(),
        compressor=DefaultCompressor(),
        with_inference=True,
    )

    assert str(compressed_series.dtype) == expected

    assert_series_equal(series, compressed_series, check_dtype=False)
