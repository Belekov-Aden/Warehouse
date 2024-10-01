from datetime import datetime
from typing import List

from pydantic import BaseModel

from enum import Enum

from app.OrderItem.shemas import OrderItemCreate, OrderItemInOrder


class StatusEnum(str, Enum):
    IN_PROCESS = "в процессе"
    SENT = "отправлен"
    DELIVERED = "доставлен"


class OrderCreate(BaseModel):
    items: list[OrderItemCreate]

    class Config:
        from_orm = True


class OrderList(BaseModel):
    id: int
    time_created: datetime
    status: str
    order_items: List[OrderItemInOrder]


class OrderUpdate(BaseModel):
    status: StatusEnum
