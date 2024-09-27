from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.utils.db import get_db
from app.product import service, schemas

router = APIRouter()


@router.post("/products/", response_model=schemas.ProductCreate)
async def create_product(item: schemas.ProductCreate, db: Session = Depends(get_db)):
    return service.create_product(db=db, item=item)


@router.get("/products/", response_model=List[schemas.ProductList])
async def products(db: Session = Depends(get_db)):
    return service.get_products(db=db)


@router.get("/products/{product_id}/", response_model=schemas.ProductOne)
async def product(product_id: int, db: Session = Depends(get_db)):
    return service.get_product_one(db=db, product_id=product_id)


@router.put("/products/{product_id}/", response_model=schemas.ProductOne)
async def update_product(product_id: int, item: schemas.ProductUpdate, db: Session = Depends(get_db)):
    return service.update_product(db=db, product_id=product_id, item=item)


@router.delete("/products/{product_id}/")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    return service.delete_product(db=db, product_id=product_id)
