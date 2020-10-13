import pandas as pd
from compressio import storage_size, savings


def test_size_formatting():
    series1 = pd.Series([True, False] * 10000, dtype=bool)
    series2 = pd.Series([True, False] * 5000, dtype=bool)
    assert series1.memory_usage(deep=True) == 20128
    assert str(storage_size(series1)) == "20128 byte"
    assert str(savings(series1, series2)) == "0.01 megabyte"
