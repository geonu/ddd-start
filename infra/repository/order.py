from datetime import datetime

from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey,
)
from sqlalchemy.orm import relationship, joinedload

from domain.order import Order, OrderId, Receiver, Address
from domain.repository.order import OrderRepository

from infra.sqlalchemy import Base, tx


class SAOrderRespository(OrderRepository):
    def find_by_id(self, order_id: OrderId) -> Order:
        with tx() as session:
            order: OrderDAO = session.query(OrderDAO).options(
                joinedload(OrderDAO.order_lines),
            ).filter(
                OrderDAO.id == order_id.id,
            ).first()

            order_id = OrderId(order.id)
            receiver = Receiver(order.receiver_name, order.receiver_phone)
            address = Address(
                order.shipping_address1, order.shipping_address2,
                order.shipping_zipcode)

            return Order(order.order_lines, receiver, address)

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

    order_lines = relationship('OrderLineDAO')


class OrderLineDAO(Base):
    __tablename__ = 'order_line'

    order_id = Column(
        String, ForeignKey('order.id'), primary_key=True, nullable=False)
    product_id = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)

    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(
        DateTime, nullable=False, default=datetime.now,
        onupdate=datetime.now)
