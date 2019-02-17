from __future__ import annotations
import enum
from typing import List

from .product import Product


class Order():
    def __init__(
            self, order_lines: List[OrderLine], shipping_info: ShippingInfo,
            state: OrderState = None,
            ) -> None:
        if not state:
            state = OrderState.PAYMENT_WAITING

        self.validate_order_lines(order_lines)
        self.validate_shipping_info(shipping_info)

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
    def total_amount(self) -> int:
        return sum(line.amount for line in self.order_lines)

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


class OrderState(enum.Enum):
    PAYMENT_WAITING = enum.auto()
    PREPARING = enum.auto()
    SHIPPED = enum.auto()
    DELIVERING = enum.auto()
    DELIVERY_COMPLETE = enum.auto()
    CANCELED = enum.auto()

    def is_before_shipped(self) -> bool:
        if self in (self.PAYMENT_WAITING, self.PREPARING):
            return True

        return False

    def can_cancel_order(self) -> bool:
        if self in (self.PAYMENT_WAITING, self.PREPARING, self.SHIPPED):
            return True

        return False


class OrderLine():
    def __init__(self, product: Product, quantity: int) -> None:
        self.product = product
        self.quantity = quantity

    @property
    def amount(self) -> int:
        return self.product.price * self.quantity


class ShippingInfo():
    def __init__(
            self, receiver: Receiver, address: Address) -> None:
        self.receiver = receiver
        self.address = address


class Receiver():
    def __init__(self, name: str, phone_number: str) -> None:
        self.name = name
        self.phone_number = phone_number


class Address():
    def __init__(self, address1: str, address2: str, zipcode: str) -> None:
        self.address1 = address1
        self.address2 = address2
        self.zipcode = zipcode
