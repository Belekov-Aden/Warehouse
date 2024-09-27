from pydantic import BaseModel

from enum import Enum


class StatusEnum(str, Enum):
    IN_PROCESS = "в процессе"
    SENT = "отправлен"
    DELIVERED = "доставлен"


class OrderCreate(BaseModel):
    status: StatusEnum
