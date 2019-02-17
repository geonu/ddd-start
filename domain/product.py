from __future__ import annotations


class Product():
    def __init__(self, price: Money) -> None:
        self.price = price


class Money():
    def __init__(self, value: int) -> None:
        self.value = value
