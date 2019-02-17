from domain.order import Order, OrderState, ShippingInfo


class TestOrderChangeShippingInfo():
    def test_change_shipping_info(self):
        order = Order()
        new_shipping_info = ShippingInfo()

        order.change_shipping_info(new_shipping_info)

        assert order.shipping_info is new_shipping_info


class TestOrderChangeShipped():
    def test_change_shipped(self):
        order = Order()

        order.change_shipped()

        assert order.state is OrderState.SHIPPED


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
