from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.utils.db import get_db
from app.product import service, schemas

router = APIRouter()