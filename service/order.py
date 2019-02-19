from abc import ABC, abstractmethod
from typing import List

from domain.order import Order, OrderLine
from domain.product import Money


class OrderCancelService():
    def order_cancel(self, order_id: str) -> None:
        order: Order = self.find_by_order_id(order_id)
        if not order:
            raise ValueError(f'no order {order_id}')

        order.cancel()


class RuleDiscounter(ABC):
    @abstractmethod
    def apply_rules(self, customer, order_lines: List[OrderLine]) -> Money:
        pass


class RuleDiscounterImpl(RuleDiscounter):
    """ 실제로 룰 엔진을 구현하지는 않을 예정 """

    def apply_rules(self, customer, order_lines: List[OrderLine]) -> Money:
        pass


class CalculateDiscountService():
    _rule_discounter: RuleDiscounter

    def __init__(self, rule_discounter: RuleDiscounter) -> None:
        self._rule_discounter = rule_discounter

    def calculate_discount(
            self, order_lines: List[OrderLine], customer_id) -> Money:
        customer = self.find_customer_by_id(customer_id)

        return self._rule_discounter.apply_rules(customer, order_lines)
