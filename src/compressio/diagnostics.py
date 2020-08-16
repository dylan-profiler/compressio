"""Work in progress"""
from functools import singledispatch

import pandas as pd
from visions.typesets import VisionsTypeset
from compressio.type_compressor import BaseTypeCompressor

from compressio.compress import compress_func
from compressio.typing import pdT

from pint import Quantity


@singledispatch
def storage_size(data: pdT, deep=True) -> Quantity:
    raise TypeError(f"Can't compute memory size of objects with type {type(data)}")


@storage_size.register(pd.Series)  # type: ignore
def _(data: pd.Series, deep) -> Quantity:
    return Quantity(value=data.memory_usage(deep=deep), units="byte")


@storage_size.register(pd.DataFrame)  # type: ignore
def _(data: pd.DataFrame, deep=False) -> Quantity:
    return Quantity(value=data.memory_usage(deep=deep).sum(), units="byte")


@singledispatch
def compress_report(
    data: pdT, typeset: VisionsTypeset, compressor: BaseTypeCompressor
) -> None:
    raise TypeError(f"Can't create a compression report of data type {type(data)}")


@compress_report.register(pd.Series)  # type: ignore
def _(data: pd.Series, typeset: VisionsTypeset, compressor: BaseTypeCompressor) -> None:
    before = data.dtype
    compressed = compress_func(data, typeset, compressor)
    after = compressed.dtype
    print(
        f"{data.name}: was {before} compressed {after} savings {compressor.savings(data, compressed)}"
    )


@compress_report.register(pd.DataFrame)  # type: ignore
def _(
    data: pd.DataFrame, typeset: VisionsTypeset, compressor: BaseTypeCompressor
) -> None:
    before = data.dtypes
    compressed = compress_func(data, typeset, compressor)
    after = compressed.dtypes

    # for in zip(before, after):
    # print(f"{data[col].name}: was {before} compressed {after} savings {compressor.savings(data[col], compressed[col])}")


def savings(
    original_data: pdT, new_data: pdT, units="megabyte", deep=False,
) -> Quantity:
    original_size = storage_size(original_data, deep)
    new_size = storage_size(new_data, deep)
    return (original_size - new_size).to(units)


def savings_report(
    original_data: pdT, new_data: pdT, units="megabyte", deep=False,
) -> None:
    original_size = storage_size(original_data, deep).to(units)
    new_size = storage_size(new_data, deep).to(units)
    reduction = original_size - new_size
    print(f"Original size: {original_size}")
    print(f"Compressed size: {new_size}")
    print(f"Savings: {reduction}")
    print(f"Reduction percentage: {reduction / original_size:.2%}")
