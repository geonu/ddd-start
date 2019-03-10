from abc import ABC, abstractmethod

from domain.order import Order, OrderNo


class OrderRepository(ABC):
    @abstractmethod
    def find_by_no(self, order_no: OrderNo) -> Order:
        pass

    @abstractmethod
    def save(self, order: Order) -> None:
        pass

    @abstractmethod
    def delete(self, order: Order) -> None:
        pass
