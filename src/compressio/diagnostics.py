"""Work in progress"""
from functools import singledispatch

import pandas as pd
from pint import Quantity
from visions.typesets import VisionsTypeset

from compressio.compress import compress_func
from compressio.type_compressor import BaseTypeCompressor
from compressio.typing import pdT


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
    data: pdT,
    typeset: VisionsTypeset,
    compressor: BaseTypeCompressor,
    with_inference: bool,
    units: str = "megabytes",
) -> None:
    raise TypeError(f"Can't create a compression report of data type {type(data)}")


@compress_report.register(pd.Series)  # type: ignore
def _(
    data: pd.Series,
    typeset: VisionsTypeset,
    compressor: BaseTypeCompressor,
    with_inference: bool,
    units: str = "megabytes",
) -> None:
    before = data.dtype
    compressed = compress_func(data, typeset, compressor, with_inference)
    after = compressed.dtype
    if str(before) != str(after):
        print(
            f'{data.name}: converting from {before} to {after} saves {savings(data, compressed, units)} (use `data[{data.name}].astype("{after}")`)'
        )


@compress_report.register(pd.DataFrame)  # type: ignore
def _(
    data: pd.DataFrame,
    typeset: VisionsTypeset,
    compressor: BaseTypeCompressor,
    with_inference: bool,
    units: str = "megabytes",
) -> None:
    for column in data.columns:
        compress_report(data[column], typeset, compressor, with_inference, units)


def savings(
    original_data: pdT, new_data: pdT, units="megabyte", deep=False
) -> Quantity:
    original_size = storage_size(original_data, deep)
    new_size = storage_size(new_data, deep)
    return (original_size - new_size).to(units)


def savings_report(
    original_data: pdT, new_data: pdT, units="megabyte", deep=False
) -> None:
    original_size = storage_size(original_data, deep).to(units)
    new_size = storage_size(new_data, deep).to(units)
    reduction = original_size - new_size
    print(f"Original size: {original_size}")
    print(f"Compressed size: {new_size}")
    print(f"Savings: {reduction}")
    print(f"Reduction percentage: {reduction / original_size:.2%}")
