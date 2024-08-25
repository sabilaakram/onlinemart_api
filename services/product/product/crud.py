# crud.py
from sqlmodel import Session, select
from product.models import Product

def create_product(session: Session, product: Product) -> Product:
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

def get_product(session: Session, product_id: int) -> Product:
    return session.get(Product, product_id)

def get_products(session: Session, skip: int = 0, limit: int = 10):
    return session.exec(select(Product).offset(skip).limit(limit)).all()

def update_product(session: Session, product_id: int, product_data: dict):
    product = session.get(Product, product_id)
    for key, value in product_data.items():
        setattr(product, key, value)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

def delete_product(session: Session, product_id: int):
    product = session.get(Product, product_id)
    session.delete(product)
    session.commit()
