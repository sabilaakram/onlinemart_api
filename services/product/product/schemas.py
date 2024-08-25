# schemas.py
from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    in_stock: int

class ProductRead(ProductCreate):
    id: int
