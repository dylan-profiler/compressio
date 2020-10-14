import pandas as pd
from compressio import DefaultCompressor
from compressio.compress import compress_func
from visions import StandardSet


def test_copy_frame():
    df = pd.DataFrame({"column": pd.Series([1], dtype="int64")})

    compressed_df = compress_func(
        df,
        typeset=StandardSet(),
        compressor=DefaultCompressor(),
        with_inference=True,
        inplace=False,
    )

    assert id(df) != id(compressed_df)


def test_inplace_frame():
    df = pd.DataFrame({"column": pd.Series([1], dtype="int64")})

    compressed_df = compress_func(
        df,
        typeset=StandardSet(),
        compressor=DefaultCompressor(),
        with_inference=True,
        inplace=True,
    )

    assert id(df) == id(compressed_df)
