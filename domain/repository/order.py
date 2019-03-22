from abc import ABC, abstractmethod

from domain.order import Order, OrderId


class OrderRepository(ABC):
    @abstractmethod
    def find_by_id(self, order_id: OrderId) -> Order:
        pass

    @abstractmethod
    def save(self, order: Order) -> None:
        pass

    @abstractmethod
    def delete(self, order: Order) -> None:
        pass
