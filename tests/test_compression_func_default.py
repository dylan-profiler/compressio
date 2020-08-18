import numpy as np
import pandas as pd
import pytest
import visions
from pandas._testing import assert_series_equal
from visions import StandardSet

from compressio.type_compressor import DefaultCompressor
from compressio.compress import compress_func


if hasattr(visions, "BoolDtype"):
    from visions import BoolDtype
    bool_type = BoolDtype
elif hasattr(pd, "BooleanDtype"):
    bool_type = pd.BooleanDtype
else:
    raise RuntimeError("No boolean Dtype found. Please update visions/pandas")


@pytest.mark.parametrize(
    "series,before,expected",
    [
        (pd.Series([10.0, 100.0, 1000.0], dtype=np.float64), np.float64, np.uint16),
        (pd.Series([np.nan, 1], dtype=np.float64), np.float64, pd.UInt8Dtype),
        (
            pd.Series([True, False, None, None, None, None, True, False] * 1000),
            np.object,
            bool_type
        ),
    ],
)
def test_compress_series(series, before, expected):
    assert series.dtype == before
    compressed_series = compress_func(
        series, typeset=StandardSet(), compressor=DefaultCompressor()
    )
    assert compressed_series.dtype == expected or isinstance(
        compressed_series.dtype, expected
    )

    assert_series_equal(series, compressed_series, check_dtype=False)