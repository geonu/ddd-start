from domain.order import Order


class OrderCancelService():
    def order_cancel(self, order_id: str) -> None:
        order: Order = self.find_by_order_id(order_id)
        if not order:
            raise ValueError(f'no order {order_id}')

        order.cancel()
