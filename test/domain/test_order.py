import pytest

from domain.order import Order, OrderState, OrderLine, ShippingInfo
from domain.product import Product


class TestOrderValidateOrderLines():
    def test_validate_order_lines(self):
        order_lines = []

        with pytest.raises(ValueError):
            Order(order_lines)


class TestOrderTotalAmount():
    def test_total_amount(self):
        price = 5000
        product = Product(price)
        quantity = 3
        order_lines = [OrderLine(product, quantity),
                       OrderLine(product, quantity)]
        order = Order(order_lines)

        total_amount: int = order.total_amount

        assert total_amount == sum(line.amount for line in order_lines)


class TestOrderChangeShippingInfo():
    def test_change_shipping_info(self):
        price = 5000
        product = Product(price)
        quantity = 3
        order_lines = [OrderLine(product, quantity)]
        order = Order(order_lines)
        new_shipping_info = ShippingInfo()

        order.change_shipping_info(new_shipping_info)

        assert order.shipping_info is new_shipping_info


class TestOrderChangeShipped():
    def test_change_shipped(self):
        price = 5000
        product = Product(price)
        quantity = 3
        order_lines = [OrderLine(product, quantity)]
        order = Order(order_lines)

        order.change_shipped()

        assert order.state is OrderState.SHIPPED


class TestOrderPayment():
    pass


class TestOrderCancel():
    pass


class TestOrderStateCanChangeShippingInfo():
    def test_can_change_shipping_info(self):
        state = OrderState.PAYMENT_WAITING
        assert state.can_change_shipping_info() is True

        state = OrderState.PREPARING
        assert state.can_change_shipping_info() is True

    def test_cannot_change_shipping_info(self):
        state = OrderState.SHIPPED
        assert state.can_change_shipping_info() is False

        state = OrderState.DELIVERING
        assert state.can_change_shipping_info() is False

        state = OrderState.DELIVERY_COMPLETE
        assert state.can_change_shipping_info() is False


class TestOrderLineAmount():
    def test_amount(self):
        price = 5000
        product = Product(price)
        quantity = 5
        order_line = OrderLine(product, quantity)

        amount: int = order_line.amount

        assert amount == price * quantity
