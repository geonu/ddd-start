from __future__ import annotations
from dataclasses import dataclass


class Product():
    def __init__(self, price: Money) -> None:
        self.price = price


@dataclass
class Money():
    value: int

    def __add__(self, other: Money) -> Money:
        return Money(self.value + other.value)

    __radd__ = __add__

    def __mul__(self, quantity: int) -> Money:
        return Money(self.value * quantity)

    __rmul__ = __mul__
