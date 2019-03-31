from datetime import datetime
from typing import List

from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey,
)
from sqlalchemy.orm import relationship, joinedload

from domain.order import (
    Order, OrderId, OrderLines, OrderLine, ShippingInfo, Receiver, Address,
)
from domain.product import Product, Money
from domain.repository.order import OrderRepository

from infra.sqlalchemy import Base, tx


class SAOrderRespository(OrderRepository):
    def find_by_id(self, order_id: OrderId) -> Order:
        with tx() as session:
            dao: OrderDAO = session.query(OrderDAO).options(
                joinedload(OrderDAO.order_lines),
            ).filter(
                OrderDAO.id == order_id.id,
            ).first()

            return dao.to_order()

    def save(self, order: Order) -> None:
        with tx() as session:
            dao: OrderDAO = session.query(OrderDAO).filter(
                OrderDAO.id == order.id.id,
            ).first()

            dao.receiver_name = order.shipping_info._receiver._name
            dao.receiver_phone = order.shipping_info._receiver._phone_number
            dao.shipping_zipcode = order.shipping_info._address._zipcode
            dao.shipping_address1 = order.shipping_info._address._address1
            dao.shipping_address2 = order.shipping_info._address._address2

            dao.state = order.state

            line_daos: List[OrderLineDAO] = []
            for line in order._order_lines._lines:
                line_dao = OrderLineDAO(line.product._id, line.quantity)
                line_daos.append(line_dao)

            dao.order_lines = line_daos


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

    def to_order(self) -> Order:
        order_id = OrderId(self.id)
        receiver = Receiver(self.receiver_name, self.receiver_phone)
        address = Address(
            self.shipping_address1, self.shipping_address2,
            self.shipping_zipcode)
        shipping_info = ShippingInfo(receiver, address)
        order_lines: OrderLines = OrderLines(
            [line.to_order_line() for line in self.order_lines])

        return Order(
            order_id, order_lines, shipping_info, self.state)


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

    def to_order_line(self) -> OrderLine:
        product = Product(Money(100))  # hard coded
        quantity: int = self.quantity

        return OrderLine(product, quantity)
