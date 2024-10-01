from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.utils.db import get_db
from app.order import service, schemas

router = APIRouter()


@router.post("/orders/", response_model=schemas.OrderCreate)
async def create_order(item: schemas.OrderCreate, db: Session = Depends(get_db)):
    return service.create_order(db=db, order=item)


@router.get("/orders/", response_model=List[schemas.OrderList])
async def get_orders(db: Session = Depends(get_db)):
    return service.get_orders(db=db)


@router.get("/orders/{order_id}/", response_model=schemas.OrderList)
async def get_orders(order_id: int, db: Session = Depends(get_db)):
    return service.get_order_single(db=db, order_id=order_id)


@router.patch("/orders/{order_id}/status/", response_model=schemas.OrderCreate)
async def patch_order(order_id: int, update_data: schemas.OrderUpdate, db: Session = Depends(get_db)):
    return service.patch_order(db=db, order_id=order_id, update_data=update_data)
