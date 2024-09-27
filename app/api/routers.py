from fastapi import APIRouter

from app.api.endpoint import order, product

api_router = APIRouter()
api_router.include_router(order.router)
api_router.include_router(product.router)
