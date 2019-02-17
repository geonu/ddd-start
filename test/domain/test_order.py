import pytest

from domain.order import (
        Order, OrderState, OrderLine, ShippingInfo, Receiver, Address,
)
from domain.product import Product


class TestOrderValidateOrderLines():
    def test_validate_order_lines(self):
        order_lines = []
        shipping_info: ShippingInfo = create_shipping_info_helper()

        with pytest.raises(ValueError):
            Order(order_lines, shipping_info)


class TestOrderValidateShippingInfo():
    def test_validate_shipping_info(self):
        order_line: OrderLine = create_order_line_helper()

        with pytest.raises(ValueError):
            Order([order_line], None)


class TestOrderTotalAmount():
    def test_total_amount(self):
        order_line_1: OrderLine = create_order_line_helper()
        order_line_2: OrderLine = create_order_line_helper()
        order_lines = [order_line_1, order_line_2]
        shipping_info: ShippingInfo = create_shipping_info_helper()
        order = Order(order_lines, shipping_info)

        total_amount: int = order.total_amount

        assert total_amount == sum(line.amount for line in order_lines)


class TestOrderChangeShippingInfo():
    def test_change_shipping_info(self):
        order_line: OrderLine = create_order_line_helper()
        shipping_info: ShippingInfo = create_shipping_info_helper()
        order = Order([order_line], shipping_info)

        name = 'new my name'
        phone_number = 'new 01012341234'
        address1 = 'new my address 1'
        address2 = 'new my address 1'
        zipcode = 'new my address 1'
        new_shipping_info = create_shipping_info_helper(
                name, phone_number, address1, address2, zipcode)

        order.change_shipping_info(new_shipping_info)

        assert order.shipping_info is new_shipping_info


class TestOrderChangeShipped():
    def test_change_shipped(self):
        order_line: OrderLine = create_order_line_helper()
        shipping_info: ShippingInfo = create_shipping_info_helper()
        order = Order([order_line], shipping_info)

        order.change_shipped()

        assert order.state is OrderState.SHIPPED


class TestOrderPayment():
    pass


class TestOrderCancel():
    def test_cancel(self):
        order_line: OrderLine = create_order_line_helper()
        shipping_info: ShippingInfo = create_shipping_info_helper()
        order = Order([order_line], shipping_info)

        order.cancel()

        assert order.state is OrderState.CANCELED


class TestOrderStateCanChangeShippingInfo():
    def test_is_before_shipped(self):
        state = OrderState.PAYMENT_WAITING

        assert state.is_before_shipped() is True

        state = OrderState.PREPARING
        assert state.is_before_shipped() is True

    def test_is_not_before_shipped(self):
        state = OrderState.SHIPPED

        assert state.is_before_shipped() is False

        state = OrderState.DELIVERING
        assert state.is_before_shipped() is False

        state = OrderState.DELIVERY_COMPLETE
        assert state.is_before_shipped() is False


class TestOrderLineAmount():
    def test_amount(self):
        price = 5000
        quantity = 3
        order_line: OrderLine = create_order_line_helper(
                price=price, quantity=quantity)

        amount: int = order_line.amount

        assert amount == price * quantity


def create_order_line_helper(
        price: int = 5000, quantity: int = 3,
        ) -> OrderLine:
    product = Product(price)
    order_line = OrderLine(product, quantity)

    return order_line


def create_shipping_info_helper(
        name: str = 'my name',
        phone_number: str = '01012341234',
        address1: str = 'my address 1',
        address2: str = 'my address 2',
        zipcode: str = 'my zipcode',
        ) -> ShippingInfo:

    receiver = Receiver(name, phone_number)
    address = Address(address1, address2, zipcode)
    return ShippingInfo(receiver, address)
