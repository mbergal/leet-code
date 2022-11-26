"""
>>> class TestEnum(OrderedEnum): 
...     ONE = "1"
...     TWO = "2" 
...     THREE = "3" 
>>> TestEnum.ONE
<TestEnum.ONE: '1'>
>>> "1" in TestEnum
True
>>> "4" in TestEnum
False
"""
from enum import Enum, EnumMeta
from typing import Any, TypeVar


T = TypeVar("T", bound="OrderedEnum")


def prev_value(t: T) -> T:
    return list(t.__class__)[list(t.__class__).index(t) - 1]


class MyEnumMeta(EnumMeta):
    def __contains__(cls, item: Any) -> bool:
        try:
            cls(item)  # type: ignore
        except ValueError:
            return False
        else:
            return True


class OrderedEnum(Enum, metaclass=MyEnumMeta):
    """ """

    def __ge__(self, other: "OrderedEnum"):
        if self.__class__ is other.__class__:
            values = [e.value for e in self.__class__]
            return values.index(self.value) >= values.index(other.value)
        return NotImplemented

    def __gt__(self, other: "OrderedEnum"):
        if self.__class__ is other.__class__:
            values = [e.value for e in self.__class__]
            return values.index(self.value) > values.index(other.value)
        return NotImplemented

    def __le__(self, other: "OrderedEnum"):
        if self.__class__ is other.__class__:
            values = [e.value for e in self.__class__]
            return values.index(self.value) <= values.index(other.value)
        return NotImplemented

    def __lt__(self, other: "OrderedEnum"):
        if self.__class__ is other.__class__:
            values = [e.value for e in self.__class__]
            return values.index(self.value) < values.index(other.value)
        return NotImplemented


if __name__ == "__main__":
    import doctest

    doctest.testmod()
