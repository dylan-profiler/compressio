from typing import Union
from pint import UnitRegistry, Quantity


ureg = UnitRegistry()


class StorageSize:
    type_options = {"b": "byte", "kb": "kilobyte", "mb": "megabyte", "gb": "gigabyte"}

    def __init__(self, total: Union[int, float], units="mb") -> None:
        self._unit_str = self.type_options[units.lower()]
        self.total: Quantity = total * self._pint_unit

    @property
    def units(self) -> str:
        return self._unit_str

    @units.setter
    def units(self, val: str) -> None:
        trial_val = val.lower()
        if trial_val in self.type_options:
            self._unit_str = self.type_options[trial_val]
            self.total = self.convert_to_units(self.total)
        else:
            raise ValueError(f"Units must be one of {list(self.type_options.keys())}")

    @property
    def _pint_unit(self) -> Quantity:
        return getattr(ureg, self.units)

    def convert_to_units(self, value) -> float:
        return value.to(self.units)

    def __str__(self) -> str:
        return f"{self.total}"

    def __repr__(self) -> str:
        return self.__str__()
