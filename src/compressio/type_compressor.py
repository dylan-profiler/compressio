from typing import Type

import pandas as pd
from visions import Complex, DateTime, Float, Integer, Object, String, VisionsBaseType

from compressio.compression_algorithms import (
    compress_complex,
    compress_datetime,
    compress_float,
    compress_integer,
    compress_object,
    compress_sparse,
)
from compressio.utils import compose


class BaseTypeCompressor:
    def __init__(self, compression_map, *args, **kwargs):
        self.compression_map = compression_map

    def compress(self, series: pd.Series, dtype: Type[VisionsBaseType]) -> pd.Series:
        compression_func = self.compression_map.get(dtype, lambda x: x)
        if isinstance(compression_func, (list, tuple, set)):
            compression_func = compose(compression_func)

        return compression_func(series)


class DefaultCompressor(BaseTypeCompressor):
    def __init__(self, *args, **kwargs):
        compression_map = {
            Integer: compress_integer,
            Float: compress_float,
            Complex: compress_complex,
            Object: compress_object,
            DateTime: compress_datetime,
            String: compress_object,
        }
        super().__init__(compression_map, *args, **kwargs)


class SparseCompressor(BaseTypeCompressor):
    def __init__(self, *args, **kwargs):
        compression_map = {
            Integer: [compress_sparse, compress_integer],
            Float: [compress_sparse, compress_float],
            Complex: [compress_sparse, compress_complex],
            Object: compress_object,
            # Pending https://github.com/pandas-dev/pandas/issues/35762
            DateTime: compress_datetime,
            String: [compress_sparse, compress_object],
        }
        super().__init__(compression_map, *args, **kwargs)
