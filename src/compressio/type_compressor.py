from functools import singledispatch
from typing import Type, Union

import pandas as pd
from visions import (
    Boolean,
    Complex,
    DateTime,
    Float,
    Integer,
    Object,
    String,
    VisionsBaseType,
)

from compressio.compression_algorithms import (
    compress_complex,
    compress_datetime,
    compress_float,
    compress_integer,
    compress_object,
    compress_sparse_missing,
)
from compressio.utils import compose


@singledispatch
def parse_func(f):
    raise NotImplementedError


@parse_func.register(object)
def _(f: object):
    return f


@parse_func.register(list)
@parse_func.register(tuple)
def _(f: Union[list, tuple]):
    return compose(f)


class BaseTypeCompressor:
    def __init__(self, compression_map, *args, **kwargs):
        self.compression_map = compression_map

    def compress(self, series: pd.Series, dtype: Type[VisionsBaseType]) -> pd.Series:
        compression_func = parse_func(self.compression_map.get(dtype, lambda x: x))
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
            Integer: [compress_sparse_missing, compress_integer],
            Float: [compress_sparse_missing, compress_float],
            Complex: [compress_sparse_missing, compress_complex],
            Object: compress_object,
            Boolean: compress_sparse_missing,
            # Pending https://github.com/pandas-dev/pandas/issues/35762
            DateTime: compress_datetime,
            String: [compress_sparse_missing, compress_object],
        }
        super().__init__(compression_map, *args, **kwargs)
