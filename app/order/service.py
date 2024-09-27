from fastapi import HTTPException
from sqlalchemy.orm import Session

from . import models, schemas


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


def create_order(db: Session, item: schemas.OrderCreate):
    db_item = models.Order(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_orders(db: Session):
    return db.query(models.Order).all()


def get_order_single(db: Session, order_id: int):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    return db_order
