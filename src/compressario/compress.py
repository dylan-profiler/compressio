from functools import singledispatch
from typing import Union

import pandas as pd
from visions import StandardSet, VisionsTypeset

from compressario.type_compressions import TypeCompressor


@singledispatch
def compress_func(
    data, typeset: VisionsTypeset, compressor: TypeCompressor
) -> pd.DataFrame:
    raise TypeError(f"Can't compress objects of type {type(data)}")


@compress_func.register
def _(
    data: pd.Series, typeset: VisionsTypeset, compressor: TypeCompressor
) -> pd.Series:
    dtype = typeset.detect_series_type(data)
    return compressor.compress(data, dtype)


@compress_func.register
def _(
    data: pd.DataFrame, typeset: VisionsTypeset, compressor: TypeCompressor
) -> pd.DataFrame:
    dtypes = typeset.detect_frame_type(data)
    return pd.DataFrame(
        {col: compressor.compress(data[col], dtypes[col]) for col in data.columns}
    )


@singledispatch
def storage_size(data, deep=False) -> int:
    raise TypeError(f"Can't compute memory size of objects with type {type(data)}")


@storage_size.register
def _(data: pd.Series, deep=False) -> int:
    return data.memory_usage(deep=deep)


@storage_size.register
def _(data: pd.DataFrame, deep=False) -> int:
    return data.memory_usage(deep=deep).sum()


class Compress:
    def __init__(
        self, typeset: VisionsTypeset = None, type_compression: TypeCompressor = None
    ):
        self.typeset = typeset if typeset is not None else StandardSet()
        self.type_compressor = (
            type_compression if type_compression is not None else TypeCompressor()
        )

    def it(
        self, data: Union[pd.Series, pd.DataFrame]
    ) -> Union[pd.Series, pd.DataFrame]:
        data = compress_func(data, self.typeset, self.type_compressor)
        return data
