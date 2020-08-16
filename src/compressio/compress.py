from functools import singledispatch

import pandas as pd
from visions import StandardSet, VisionsTypeset

from compressio.type_compressor import BaseTypeCompressor, DefaultCompressor
from compressio.typing import pdT


@singledispatch
def compress_func(
    data: pdT, typeset: VisionsTypeset, compressor: BaseTypeCompressor
) -> pdT:
    dtype = typeset.detect_type(data)
    return compressor.compress(data, dtype)


@compress_func.register(pd.Series)  # type: ignore
def _(
    data: pd.Series, typeset: VisionsTypeset, compressor: BaseTypeCompressor
) -> pd.Series:
    dtype = typeset.detect_type(data)
    return compressor.compress(data, dtype)


@compress_func.register(pd.DataFrame)  # type: ignore
def _(
    data: pd.DataFrame, typeset: VisionsTypeset, compressor: BaseTypeCompressor
) -> pd.DataFrame:
    dtypes = typeset.detect_type(data)
    return pd.DataFrame(
        {col: compressor.compress(data[col], dtypes[col]) for col in data.columns}
    )


class Compress:
    def __init__(
        self, typeset: VisionsTypeset = None, compressor: BaseTypeCompressor = None,
    ) -> None:
        self.typeset = typeset if typeset is not None else StandardSet()
        self.compressor = compressor if compressor is not None else DefaultCompressor()

    def it(self, data: pdT) -> pdT:
        data = compress_func(data, self.typeset, self.compressor)
        return data
