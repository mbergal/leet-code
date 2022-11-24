from enum import Enum
from typing import TypeVar


T = TypeVar("T", bound="OrderedEnum")

def prev_value(t: T) -> T:
    return list(t.__class__)[list(t.__class__).index(t) - 1]


class OrderedEnum(Enum):
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
