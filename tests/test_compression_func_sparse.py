import random

import numpy as np
import pandas as pd
import pytest
from visions import StandardSet

from compressio.type_compressor import SparseCompressor
from compressio.compress import compress_func


@pytest.mark.parametrize(
    "series,before,expected,inference",
    [
        (pd.Series([np.NaN] * 100 + [0] * 9000 + [1] * 500 + [2] * 400 + [3] * 10, dtype=np.float), np.float64, pd.Int8Dtype(), True),
        (pd.Series([np.NaN] * 100 + [0] * 9000 + [1] * 500 + [2] * 400 + [3] * 10, dtype=np.float).astype("Int64"), pd.Int64Dtype(), pd.Int8Dtype(), False),
        (pd.Series([pd.NA] * 100 + [0] * 9000 + [1] * 500 + [2] * 400 + [3] * 10, dtype="Int64"), pd.Int64Dtype(), pd.Int8Dtype(), False),
        (pd.Series([None] * 10000 + random.choices(['gold', 'black', 'silver'], k=10), dtype=str), np.object, pd.SparseDtype("object", np.nan), False),
        (pd.Series([np.nan] * 10000 + random.choices(['gold', 'black', 'silver'], k=10), dtype=str), np.object, pd.SparseDtype("object", np.nan), False),
        (pd.Series([pd.NA] * 10000 + random.choices(['gold', 'black', 'silver'], k=10), dtype=str), np.object, pd.SparseDtype("object", np.nan), False),
        (pd.Series([pd.NA] * 10000 + [True, False], dtype="boolean"), pd.BooleanDtype(), pd.SparseDtype(bool, pd.NA), False),
    ]
)
def test_compress_series(series, before, expected, inference):
    assert series.dtype == before
    compressed_series = compress_func(
        series, typeset=StandardSet(), compressor=SparseCompressor(), with_inference=inference
    )
    assert compressed_series.dtype == expected

    assert np.array_equal(series[series.notna()].values, compressed_series[compressed_series.notna()].values)
