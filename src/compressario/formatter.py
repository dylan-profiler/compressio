from typing import Union
from pint import UnitRegistry, Quantity


ureg = UnitRegistry()


class StorageSize:
    type_options = {"b": "byte", "kb": "kilobyte", "mb": "megabyte", "gb": "gigabyte"}

    def __init__(self, total: Union[int, float], units="mb") -> None:
        self.total: Quantity = total * ureg.byte
        self.units: str = units

    @property
    def desired_unit(self):
        return getattr(ureg, self.type_options[self.units.lower()])

    @property
    def _in_units(self) -> float:
        return self.total.to(self.desired_unit)

    def __str__(self) -> str:
        return f"{self._in_units}"

    def __repr__(self) -> str:
        return self.__str__()
