from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
from typing import List

from .product import Product, Money


class Order():
    order_no: OrderNo
    order_lines: List[OrderLine]
    shipping_info: ShippingInfo
    state: OrderState

    def __init__(
            self, order_lines: List[OrderLine], shipping_info: ShippingInfo,
            state: OrderState = None,
            ) -> None:
        if not state:
            state = OrderState.PAYMENT_WAITING

        self.validate_order_lines(order_lines)
        self.validate_shipping_info(shipping_info)

        self.order_no = OrderNo()
        self.order_lines = order_lines
        self.shipping_info = shipping_info
        self.state = state

    def validate_order_lines(self, order_lines: List[OrderLine]) -> None:
        if len(order_lines) == 0:
            raise ValueError('Order must have more than one OrderLine')

    def validate_shipping_info(self, shipping_info: ShippingInfo) -> None:
        if shipping_info is None:
            raise ValueError('Order must have not None ShippingInfo')

    @property
    def total_amount(self) -> Money:
        _total_amount = Money(0)
        for line in self.order_lines:
            _total_amount += line.amount

        return _total_amount

    def change_shipping_info(self, shipping_info: ShippingInfo) -> None:
        if not self.state.is_before_shipped():
            raise ValueError(
                    f'cannot change shipping info because the state\
                    {self.state} is not before shipped')

        self.validate_shipping_info(shipping_info)
        self.shipping_info = shipping_info

    def change_shipped(self) -> None:
        self.state = OrderState.SHIPPED

    def payment(self) -> None:
        pass

    def cancel(self) -> None:
        if not self.state.is_before_shipped():
            raise ValueError(
                    f'cannot cancel order because the state {self.state}\
                    is not before shipped')

        self.state = OrderState.CANCELED


@dataclass
def OrderNo():
    no: str


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

    def can_cancel_order(self) -> bool:
        if self in (self.PAYMENT_WAITING, self.PREPARING, self.SHIPPED):
            return True

        return False


class OrderLine():
    product: Product
    quantity: int

    def __init__(self, product: Product, quantity: int) -> None:
        self.product = product
        self.quantity = quantity

    @property
    def amount(self) -> Money:
        price: Money = self.product.price

        return price * self.quantity


@dataclass
class ShippingInfo():
    receiver: Receiver
    address: Address


@dataclass
class Receiver():
    name: str
    phone_number: str


@dataclass
class Address():
    address1: str
    address2: str
    zipcode: str
