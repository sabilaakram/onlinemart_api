# main.py
from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from product.database import create_db_and_tables, get_session
from product.models import Product
from product.schemas import ProductCreate, ProductRead
from product.crud import create_product, get_product, get_products, update_product, delete_product

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/products/", response_model=List[ProductRead])
def create_product_view(*, session: Session = Depends(get_session), product: ProductCreate):
    return create_product(session, Product.from_orm(product))

@app.get("/products/{product_id}", response_model=ProductRead)
def read_product_view(*, session: Session = Depends(get_session), product_id: int):
    product = get_product(session, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.get("/products/", response_model=List[ProductRead])
def read_products_view(*, session: Session = Depends(get_session), skip: int = 0, limit: int = 10):
    return get_products(session, skip=skip, limit=limit)

@app.put("/products/{product_id}", response_model=ProductRead)
def update_product_view(*, session: Session = Depends(get_session), product_id: int, product: ProductCreate):
    return update_product(session, product_id, product.dict())

@app.delete("/products/{product_id}")
def delete_product_view(*, session: Session = Depends(get_session), product_id: int):
    delete_product(session, product_id)
    return {"ok": True}
