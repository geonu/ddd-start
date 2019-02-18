from __future__ import annotations
from dataclasses import dataclass


class Product():
    _price: Money

    def __init__(self, price: Money) -> None:
        self._price = price

    @property
    def price(self) -> Money:
        return self._price


@dataclass
class Money():
    _value: int

    @property
    def value(self) -> int:
        return self._value

    def __add__(self, other: Money) -> Money:
        return Money(self._value + other.value)

    __radd__ = __add__

    def __mul__(self, quantity: int) -> Money:
        return Money(self._value * quantity)

    __rmul__ = __mul__
