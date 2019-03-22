from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
from typing import List

from domain.member import MemberId
from domain.product import Product, Money


class Order():
    _order_id: OrderId
    _order_lines: OrderLines
    _shipping_info: ShippingInfo
    _state: OrderState

    def __init__(
            self, order_lines: List[OrderLine], shipping_info: ShippingInfo,
            state: OrderState = None) -> None:
        if not state:
            state = OrderState.PAYMENT_WAITING

        self._order_id = OrderId()
        self._state = state
        self._order_lines = OrderLines(order_lines)
        self.change_shipping_info(shipping_info)

    @property
    def state(self) -> OrderState:
        return self._state

    def change_shipped(self) -> None:
        self._state = OrderState.SHIPPED

    def payment(self) -> None:
        pass

    def cancel(self) -> None:
        if not self._state.is_before_shipped():
            raise ValueError(
                f'cannot cancel order because the state {self.state}\
                is not before shipped')

        self._state = OrderState.CANCELED

    @property
    def shipping_info(self) -> ShippingInfo:
        return self._shipping_info

    def _validate_shipping_info(self, shipping_info: ShippingInfo) -> None:
        if shipping_info is None:
            raise ValueError('Order must have not None ShippingInfo')

        if not self._state.is_before_shipped():
            raise ValueError(
                f'cannot change shipping info because the state\
                {self.state} is not before shipped')

    def change_shipping_info(self, shipping_info: ShippingInfo) -> None:
        self._validate_shipping_info(shipping_info)
        self._shipping_info = shipping_info

    def total_amount(self) -> Money:
        return self._order_lines.total_amount()

    def change_order_lines(self, order_lines: List[OrderLine]) -> None:
        self._order_lines.change_order_lines(order_lines)


@dataclass
class OrderId():
    _id: str

    def __init__(self, _id: str = None) -> None:
        if _id is None:
            _id = 'uuid'

        self._id = _id


class OrderState(Enum):
    PAYMENT_WAITING = auto()
    PREPARING = auto()
    SHIPPED = auto()
    DELIVERING = auto()
    DELIVERY_COMPLETE = auto()
    CANCELED = auto()

    def is_before_shipped(self) -> bool:
        if self in (self.PAYMENT_WAITING, self.PREPARING):
            return True

        return False


class OrderLines:
    _lines: List[OrderLine]

    def __init__(self, lines: List[OrderLine] = None) -> None:
        if lines is None:
            lines = []

        self.change_order_lines(lines)

    def total_amount(self) -> Money:
        total = Money(0)
        for line in self._lines:
            total += line.amount

        return total

    def change_order_lines(self, order_lines: List[OrderLine]) -> None:
        if not order_lines:
            raise ValueError('Order must have more than one OrderLine')

        self._lines = order_lines


class OrderLine:
    _product: Product
    _quantity: int

    def __init__(self, product: Product, quantity: int) -> None:
        self._product = product
        self._quantity = quantity

    @property
    def amount(self) -> Money:
        price: Money = self._product.price

        return price * self._quantity


class Orderer:
    _member_id: MemberId


@dataclass
class ShippingInfo():
    _receiver: Receiver
    _address: Address


@dataclass
class Receiver():
    _name: str
    _phone_number: str


@dataclass
class Address():
    _address1: str
    _address2: str
    _zipcode: str
