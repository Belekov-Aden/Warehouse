from sqlalchemy import String, Integer, ForeignKey, Boolean, Column, Date, DateTime, Enum, Text, Float
from sqlalchemy.orm import relationship
from db.base_class import Base


class Product:
    '''Model Product'''
    __tablename = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    count_in_storage = Column(Integer, nullable=False)


