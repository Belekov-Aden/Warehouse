from sqlalchemy import String, Integer, Column, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.base_class import Base

from .schemas import StatusEnum


class Order(Base):
    '''Model Order'''
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(Enum(StatusEnum), default=StatusEnum.IN_PROCESS)

    order_items = relationship("OrderItem", back_populates="order")
