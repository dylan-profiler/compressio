import pytest
from compressario.formatter import StorageSize


def test_valid_StorageSize():
    n = 1000.0
    size = StorageSize(n, "b")

    valid_units = {"KB": n / 1000, "mb": n / 1000 ** 2, "b": n, "Gb": n / 1000 ** 3}
    for unit, equivalent in valid_units.items():
        size.units = unit
        assert size.total.magnitude == pytest.approx(equivalent, rel=0.00000001)

    size = StorageSize(n, "mb")

    valid_units = {"KB": n * 1000, "mb": n, "b": n * 1000 ** 2, "Gb": n / 1000}
    for unit, equivalent in valid_units.items():
        size.units = unit
        assert size.total.magnitude == pytest.approx(equivalent, rel=0.00000001)


@pytest.mark.xfail(raises=ValueError)
def test_invalid_StorageSize():
    n = 1000.0
    size = StorageSize(n, "b")

    valid_units = {"geckos": n}
    for unit, equivalent in valid_units.items():
        size.units = unit
