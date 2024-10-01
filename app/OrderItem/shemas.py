from pydantic import BaseModel

from app.product.schemas import ProductInOrder


class OrderItemCreate(BaseModel):
    id_product: int
    count_in_order: int

    class Config:
        from_orm = True


class OrderItemInOrder(BaseModel):
    id: int
    product: ProductInOrder  # Связанный товар
    count_in_order: int
