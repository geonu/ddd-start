from typing import List

from service.order import RuleDiscounter
from domain.customer import Customer
from domain.order import OrderLine
from domain.product import Money


class RuleDiscounterImpl(RuleDiscounter):
    """ 실제로 룰 엔진을 구현하지는 않을 예정 """

    def apply_rules(
            self, customer: Customer, order_lines: List[OrderLine]) -> Money:
        pass
