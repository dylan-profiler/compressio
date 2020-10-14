from functools import singledispatch

import pandas as pd
from visions import VisionsTypeset
from visions.typesets.typeset import get_type_from_path, traverse_graph

from compressio.typesets import DefaultCompressioTypeset
from compressio.type_compressor import BaseTypeCompressor, DefaultCompressor
from compressio.typing import pdT
from tqdm import tqdm


def get_data_and_dtype(data: pdT, typeset: VisionsTypeset, with_inference: bool):
    graph = typeset.relation_graph if with_inference else typeset.base_graph
    data, dtype_path, state = traverse_graph(data, typeset.root_node, graph)
    dtype = get_type_from_path(dtype_path)
    return data, dtype


@singledispatch
def compress_func(
    data: pdT,
    typeset: VisionsTypeset,
    compressor: BaseTypeCompressor,
    with_inference: bool,
    inplace: bool = False,
) -> pdT:
    raise Exception(f"Unsupported datatype {type(data)}")


@compress_func.register(pd.Series)  # type: ignore
def _(
    data: pd.Series,
    typeset: VisionsTypeset,
    compressor: BaseTypeCompressor,
    with_inference: bool,
    inplace: bool = False,
) -> pd.Series:
    data, dtype = get_data_and_dtype(data, typeset, with_inference)
    return compressor.compress(data, dtype)


@compress_func.register(pd.DataFrame)  # type: ignore
def _(
    data: pd.DataFrame,
    typeset: VisionsTypeset,
    compressor: BaseTypeCompressor,
    with_inference: bool,
    inplace: bool = False,
) -> pd.DataFrame:
    result = data if inplace else pd.DataFrame()
    for col in tqdm(data.columns):
        result[col] = compress_func(
            data[col], typeset, compressor, with_inference, inplace
        )
    return result


class Compress:
    def __init__(
        self,
        typeset: VisionsTypeset = None,
        compressor: BaseTypeCompressor = None,
        with_type_inference: bool = False,
    ) -> None:
        self.typeset = typeset if typeset is not None else DefaultCompressioTypeset()
        self.compressor = compressor if compressor is not None else DefaultCompressor()
        self.with_type_inference = with_type_inference

    def it(self, data: pdT, inplace: bool = False) -> pdT:
        data = compress_func(
            data, self.typeset, self.compressor, self.with_type_inference, inplace
        )
        return data
