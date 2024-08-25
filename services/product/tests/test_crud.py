# test_crud.py
import pytest
from sqlmodel import Session, SQLModel, create_engine
from product.models import Product
from product.crud import create_product, get_product, get_products, update_product, delete_product

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, echo=True)

@pytest.fixture
def session():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

@pytest.fixture
def product_data():
    return Product(
        name="Test Product",
        description="Test Description",
        price=10.0,
        in_stock=100
    )

def test_create_product(session, product_data):
    product = create_product(session, product_data)
    assert product.id is not None
    assert product.name == product_data.name
    assert product.description == product_data.description
    assert product.price == product_data.price
    assert product.in_stock == product_data.in_stock

def test_get_product(session, product_data):
    product = create_product(session, product_data)
    fetched_product = get_product(session, product.id)
    assert fetched_product == product

def test_get_products(session, product_data):
    create_product(session, product_data)
    products = get_products(session)
    assert len(products) == 1

def test_update_product(session, product_data):
    product = create_product(session, product_data)
    updated_data = {
        "name": "Updated Product",
        "description": "Updated Description",
        "price": 15.0,
        "in_stock": 150
    }
    updated_product = update_product(session, product.id, updated_data)
    assert updated_product.name == updated_data["name"]
    assert updated_product.description == updated_data["description"]
    assert updated_product.price == updated_data["price"]
    assert updated_product.in_stock == updated_data["in_stock"]

def test_delete_product(session, product_data):
    product = create_product(session, product_data)
    delete_product(session, product.id)
    fetched_product = get_product(session, product.id)
    assert fetched_product is None
