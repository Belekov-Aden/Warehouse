from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.utils.db import get_db
from app.order import service, schemas

router = APIRouter()


@router.post("/orders/", response_model=schemas.OrderCreate)
async def create_order(item: schemas.OrderCreate, db: Session = Depends(get_db)):
    return service.create_order(db=db, item=item)
