import random

import numpy as np
import pandas as pd
import pytest
from pandas._testing import assert_series_equal
from visions import StandardSet

from compressio.type_compressor import SparseCompressor
from compressio.compress import compress_func


@pytest.mark.parametrize(
    "series,before,expected",
    [
        (pd.Series([np.NaN] * 100 + [0] * 9000 + [1] * 500 + [2] * 400 + [3] * 10, dtype=np.float), np.float64, pd.UInt8Dtype),
        (pd.Series([np.NaN] * 100 + [0] * 9000 + [1] * 500 + [2] * 400 + [3] * 10, dtype=np.float).astype("Int64"), pd.Int64Dtype(), pd.UInt8Dtype),
        (pd.Series([pd.NA] * 100 + [0] * 9000 + [1] * 500 + [2] * 400 + [3] * 10, dtype="Int64"), pd.Int64Dtype(), pd.UInt8Dtype),
        (pd.Series([None] * 10000 + random.choices(['gold', 'black', 'silver'], k=10), dtype=str), np.object, pd.SparseDtype(np.object, None)),
        (pd.Series([np.nan] * 10000 + random.choices(['gold', 'black', 'silver'], k=10), dtype=str), np.object, pd.SparseDtype(np.object, np.nan)),
        (pd.Series([pd.NA] * 10000 + random.choices(['gold', 'black', 'silver'], k=10), dtype=str), np.object, pd.SparseDtype(np.object, pd.NA)),
        (pd.Series([None] * 10000 + [True, False], dtype="boolean"), pd.BooleanDtype(), pd.SparseDtype(bool, None)),
    ]
)
def test_compress_series(series, before, expected):
    assert series.dtype == before
    compressed_series = compress_func(
        series, typeset=StandardSet(), compressor=SparseCompressor()
    )
    assert compressed_series.dtype == expected or isinstance(
        compressed_series.dtype, expected
    )

    assert_series_equal(series, compressed_series, check_dtype=False)
