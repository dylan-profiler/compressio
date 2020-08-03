from compressario.compression_algorithms import (
    compress_complex,
    compress_float,
    compress_datetime,
    compress_integer,
    compress_object,
)
from typing import Type

import pandas as pd
from visions import (
    Boolean,
    Categorical,
    Complex,
    DateTime,
    Float,
    Integer,
    Object,
    String,
    VisionsBaseType,
)


class BaseTypeCompressor:
    def __init__(self, compression_map, *args, **kwargs):
        self.compression_map = compression_map

    def compress(self, series: pd.Series, dtype: Type[VisionsBaseType]) -> pd.Series:
        return self.compression_map.get(dtype, lambda x: x)(series)


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
