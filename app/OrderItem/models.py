from sqlalchemy import String, Integer, ForeignKey, Boolean, Column, Date, DateTime, Enum, Text, Float

from ..order.models import Order
from ..product.models import Product


class Product:
    '''Model Order Item'''
    __tablename = 'OrderItem'

    id = Column(Integer, primary_key=True, index=True)
    id_order = Column(Integer, ForeignKey('orders.id'))
    id_product = Column(Integer, ForeignKey('products.id'))
    count_in_order = Column(Integer, nullable=False)
