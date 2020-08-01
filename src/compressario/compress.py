from compressario.type_compressions import TypeCompressor
from visions import StandardSet, Date, VisionsTypeset
import pandas as pd
import numpy as np
from functools import singledispatch
from typing import Union


class StorageSize(float):
    _conversion = {
        "B": lambda x: x,
        "KB": lambda x: x / 1000,
        "MB": lambda x: x / 1000 ** 2,
        "GB": lambda x: x / 1000 ** 3,
    }

    def __init__(self, total: Union[int, float], units="B"):
        self.units = units
        self.total = total
        float.__init__(total)

    @property
    def _in_units(self) -> float:
        return self._conversion[self.units](self.total)

    def __str__(self) -> str:
        return f"{self._in_units} {self.units}"

    def __repr__(self) -> str:
        return self.__str__()


@singledispatch
def compress_func(
    data, typeset: VisionsTypeset, compressor: TypeCompressor
) -> pd.DataFrame:
    raise f"Can't compress objects of type {type(data)}"


@compress_func.register
def _(
    data: pd.Series, typeset: VisionsTypeset, compressor: TypeCompressor
) -> pd.Series:
    dtype = typeset.detect_series_type(data)
    return compressor.compress(series, dtype)


@compress_func.register
def _(
    data: pd.DataFrame, typeset: VisionsTypeset, compressor: TypeCompressor
) -> pd.DataFrame:
    dtypes = typeset.detect_frame_type(data)
    return pd.DataFrame(
        {col: compressor.compress(data[col], dtypes[col]) for col in data.columns}
    )


@singledispatch
def savings(data) -> int:
    raise f"Can't compute memory size of objects with type {type(data)}"


@savings.register
def _(data: pd.Series) -> int:
    return data.memory_usage()


@savings.register
def _(data: pd.DataFrame) -> int:
    return data.memory_usage().sum()


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
        return compress_func(data, self.typeset, self.type_compressor)

    @staticmethod
    def savings(
        self,
        original_data: Union[pd.Series, pd.DataFrame],
        new_data: Union[pd.Series, pd.DataFrame],
        units="MB",
    ) -> Union[pd.Series, pd.DataFrame]:
        original_size = savings(original_data)
        new_size = savings(new_data)
        return StorageSize(original_size - new_size, units=units)
