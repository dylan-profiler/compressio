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
