from __future__ import annotations

import enum


class Order():
    def __init__(
            self, state: OrderState=None, shipping_info: ShippingInfo=None,
            ) -> None:
        if not state:
            state = OrderState.PAYMENT_WAITING

        self.state = state
        self.shipping_info = shipping_info

    def change_shipping_info(self, shipping_info: ShippingInfo):
        if not self.state.can_change_shipping_info():
            raise ValueError(
                    f'cannot change shipping info in {self.state} order state')

        self.shipping_info = shipping_info

    def change_shipped(self):
        self.state = OrderState.SHIPPED


class OrderState(enum.Enum):
    PAYMENT_WAITING = enum.auto()
    PREPARING = enum.auto()
    SHIPPED = enum.auto()
    DELIVERING = enum.auto()
    DELIVERY_COMPLETE = enum.auto()

    def can_change_shipping_info(self):
        if self in (self.PAYMENT_WAITING, self.PREPARING):
            return True

        return False

    def can_cancel_order(self):
        if self in (self.PAYMENT_WAITING, self.PREPARING, self.SHIPPED):
            return True

        return False


class ShippingInfo():
    pass
