from datetime import datetime

from sqlalchemy import Column, String, DateTime

from domain.order import Order, OrderId
from domain.repository.order import OrderRepository

from infra.sqlalchemy import Base


class SAOrderRespository(OrderRepository):
    def find_by_id(self, order_id: OrderId) -> Order:
        pass

    def save(self, order: Order) -> None:
        pass


class OrderDAO(Base):
    __tablename__ = 'order'

    id = Column(String, primary_key=True)
    state = Column(String, nullable=False)
    orderer_id = Column(String, nullable=False)

    shipping_zipcode = Column(String)
    shipping_address1 = Column(String)
    shipping_address2 = Column(String)
    receiver_name = Column(String)
    receiver_phone = Column(String)

    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(
        DateTime, nullable=False, default=datetime.now,
        onupdate=datetime.now)
