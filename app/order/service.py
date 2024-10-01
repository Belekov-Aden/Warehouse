from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from . import models, schemas
from .models import Order
from ..OrderItem.models import OrderItem
from ..product.models import Product


def patch_order(db: Session, order_id: int, update_data: schemas.OrderUpdate):
    # Получаем заказ по ID
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()

    # Если заказ не найден, выбрасываем исключение
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    update_data_dict = update_data.dict(exclude_unset=True)
    for key, value in update_data_dict.items():
        setattr(db_order, key, value)

    db.commit()
    db.refresh(db_order)

    return db_order


def create_order(db: Session, order: schemas.OrderCreate):
    try:
        order_items = []
        product_ids = [item.id_product for item in order.items]
        products = db.query(Product).filter(Product.id.in_(product_ids)).all()

        product_map = {product.id: product for product in products}

        for item in order.items:
            product = product_map.get(item.id_product)

            if not product:
                raise HTTPException(status_code=404, detail=f"Product {item.id_product} not found")

            if product.count_in_storage < item.count_in_order:
                raise HTTPException(
                    status_code=400,
                    detail=f"Not enough stock for product '{product.name}'. "
                           f"Requested: {item.count_in_order}, Available: {product.count_in_storage}"
                )

            product.count_in_storage -= item.count_in_order

            order_item = OrderItem(id_product=item.id_product, count_in_order=item.count_in_order)
            order_items.append(order_item)

        new_order = Order(order_items=order_items)

        db.add(new_order)
        db.commit()
        db.refresh(new_order)

        return new_order
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")


def get_orders(db: Session):
    return db.query(models.Order).all()


def get_order_single(db: Session, order_id: int):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    return db_order
