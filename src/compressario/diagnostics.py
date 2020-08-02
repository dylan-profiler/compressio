"""Work in progress"""
from functools import singledispatch
from typing import Union

import pandas as pd
from visions.typesets import VisionsTypeset
from compressario.type_compressor import BaseTypeCompressor
from compressario.formatter import StorageSize
from compressario.compress import compress_func
from compressario.typing import pdT


@singledispatch
def storage_size(data: pdT, deep=False) -> int:
    raise TypeError(f"Can't compute memory size of objects with type {type(data)}")


@storage_size.register(pd.Series)
def _(data: pd.Series, deep=False) -> int:
    return data.memory_usage(deep=deep)


@storage_size.register(pd.DataFrame)
def _(data: pd.DataFrame, deep=False) -> int:
    return data.memory_usage(deep=deep).sum()


@singledispatch
def compress_report(
    data: pdT, typeset: VisionsTypeset, compressor: BaseTypeCompressor
) -> None:
    raise TypeError(f"Can't create a compression report of data type {type(data)}")


@compress_report.register(pd.Series)
def _(data: pd.Series, typeset: VisionsTypeset, compressor: BaseTypeCompressor) -> None:
    before = data.dtype
    compressed = compress_func(data, typeset, compressor)
    after = compressed.dtype
    print(
        f"{data.name}: was {before} compressed {after} savings {compressor.savings(data, compressed)}"
    )


@compress_report.register(pd.DataFrame)
def _(
    data: pd.DataFrame, typeset: VisionsTypeset, compressor: BaseTypeCompressor
) -> None:
    before = data.dtypes
    compressed = compress_func(data, typeset, compressor)
    after = compressed.dtypes

    # for in zip(before, after):
    # print(f"{data[col].name}: was {before} compressed {after} savings {compressor.savings(data[col], compressed[col])}")


def savings(original_data: pdT, new_data: pdT, units="MB", deep=False,) -> StorageSize:
    original_size = storage_size(original_data, deep)
    new_size = storage_size(new_data, deep)
    return StorageSize(original_size - new_size, units=units)


def savings_report(original_data: pdT, new_data: pdT, units="MB", deep=False,) -> None:
    original_size = storage_size(original_data, deep)
    new_size = storage_size(new_data, deep)
    reduction = original_size - new_size
    print(f"Original size: {StorageSize(original_size, units=units)}")
    print(f"Compressed size: {StorageSize(new_size, units=units)}")
    print(f"Savings: {StorageSize(reduction, units=units)}")
    print(f"Reduction percentage: {reduction / original_size:.2%}")
