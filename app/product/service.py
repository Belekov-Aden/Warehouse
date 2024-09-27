from fastapi import HTTPException
from sqlalchemy.orm import Session

from . import models, schemas


def get_products(db: Session):
    return db.query(models.Product).all()


def create_product(db: Session, item: schemas.ProductCreate):
    db_item = models.Product(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_product_one(db: Session, product_id: int):
    db_prodcut = db.query(models.Product).filter(models.Product.id == product_id).first()

    if not db_prodcut:
        raise HTTPException(status_code=404, detail="Prodcut not found")

    return db_prodcut


def update_product(db: Session, product_id: int, item: schemas.ProductUpdate):
    # Получаем продукт по ID
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()

    # Если продукт не найден, выбрасываем исключение
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Обновляем только те поля, которые переданы в item (с использованием exclude_unset=True)
    update_data = item.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)

    # Сохраняем изменения в базе данных
    db.commit()
    db.refresh(db_product)

    return db_product


def delete_product(db: Session, product_id: int):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)

    db.commit()

    return {"message": "Product deleted successfully"}
