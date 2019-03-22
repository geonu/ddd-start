from abc import ABC, abstractmethod
from typing import List

from domain.customer import Customer
from domain.order import Order, OrderId, OrderLine
from domain.product import Money
from domain.repository.order import OrderRepository


class OrderCancel():
    _order_repository: OrderRepository

    def __init__(self, order_repository: OrderRepository) -> None:
        self._order_repository = order_repository

    def cancel(self, order_id: OrderId) -> None:
        order: Order = self._order_repository.find_by_no(order_id)
        if not order:
            raise ValueError(f'no order {order_id}')

        order.cancel()


class RuleDiscounter(ABC):
    @abstractmethod
    def apply_rules(
            self, customer: Customer, order_lines: List[OrderLine]) -> Money:
        pass


class CustomerRepository(ABC):
    @abstractmethod
    def find_by_id(self, customer_id: str) -> Customer:
        pass


class CalculateDiscount():
    _rule_discounter: RuleDiscounter
    _customer_repository: CustomerRepository

    def __init__(
            self, customer_repository: CustomerRepository,
            rule_discounter: RuleDiscounter) -> None:
        self._customer_repository = customer_repository
        self._rule_discounter = rule_discounter

    def calculate_discount(
            self, order_lines: List[OrderLine], customer_id: str) -> Money:
        customer: Customer = self._find_customer(customer_id)

        return self._rule_discounter.apply_rules(customer, order_lines)

    def _find_customer(self, customer_id: str) -> Customer:
        customer: Customer = self._customer_repository.find_by_id(customer_id)
        if not customer:
            raise ValueError(f'no customer {customer_id}')

        return customer
