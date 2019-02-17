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
        self.validate_shipping_info(shipping_info)

        if not self.state.can_change_shipping_info():
            raise ValueError(
                    f'cannot change shipping info in {self.state} order state')

        self.shipping_info = shipping_info

    def change_shipped(self) -> None:
        self.state = OrderState.SHIPPED

    def payment(self) -> None:
        pass

    def cancel(self) -> None:
        pass


class OrderState(enum.Enum):
    PAYMENT_WAITING = enum.auto()
    PREPARING = enum.auto()
    SHIPPED = enum.auto()
    DELIVERING = enum.auto()
    DELIVERY_COMPLETE = enum.auto()

    def can_change_shipping_info(self) -> bool:
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
            self, receiver_name: str, receiver_phone_number: str,
            receiver_address: str,
            ) -> None:
        self.receiver_name = receiver_name
        self.receiver_phone_number = receiver_phone_number
        self.receiver_address = receiver_address
