"""Work in progress"""
from functools import singledispatch
from typing import Union

import pandas as pd

from compressario import StorageSize
from compressario.compress import compress_func, storage_size


@singledispatch
def compress_report(data, typeset, compressor):
    raise TypeError(f"Can't create a compression report of data type {type(data)}")


@compress_report.register
def _(data: pd.Series, typeset, compressor):
    before = data.dtype
    compressed = compress_func(data, typeset, compressor)
    after = compressed.dtype
    print(
        f"{data.name}: was {before} compressed {after} savings {compressor.savings(data, compressed)}"
    )


#
@compress_report.register
def _(data: pd.DataFrame, typeset, compressor):
    before = data.dtypes
    compressed = compress_func(data, typeset, compressor)
    after = compressed.dtypes

    # for in zip(before, after):
    # print(f"{data[col].name}: was {before} compressed {after} savings {compressor.savings(data[col], compressed[col])}")


def savings(
    original_data: Union[pd.Series, pd.DataFrame],
    new_data: Union[pd.Series, pd.DataFrame],
    units="MB",
    deep=False,
) -> StorageSize:
    original_size = storage_size(original_data, deep)
    new_size = storage_size(new_data, deep)
    return StorageSize(original_size - new_size, units=units)


def savings_report(
    original_data: Union[pd.Series, pd.DataFrame],
    new_data: Union[pd.Series, pd.DataFrame],
    units="MB",
    deep=False,
):
    original_size = storage_size(original_data, deep)
    new_size = storage_size(new_data, deep)
    reduction = original_size - new_size
    print(f"Original size: {StorageSize(original_size, units=units)}")
    print(f"Compressed size: {StorageSize(new_size, units=units)}")
    print(f"Savings: {StorageSize(reduction, units=units)}")
    print(f"Reduction percentage: {reduction / original_size:.2%}")
