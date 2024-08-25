# test_schemas.py
from pydantic import ValidationError
from product.schemas import ProductCreate, ProductRead

def test_product_create_schema():
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 10.0,
        "in_stock": 100
    }
    product = ProductCreate(**product_data)
    assert product.name == product_data["name"]
    assert product.description == product_data["description"]
    assert product.price == product_data["price"]
    assert product.in_stock == product_data["in_stock"]

def test_product_create_schema_invalid():
    invalid_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": "invalid_price",
        "in_stock": 100
    }
    try:
        ProductCreate(**invalid_data)
    except ValidationError as e:
        assert "value is not a valid float" in str(e)

def test_product_read_schema():
    product_data = {
        "id": 1,
        "name": "Test Product",
        "description": "Test Description",
        "price": 10.0,
        "in_stock": 100
    }
    product = ProductRead(**product_data)
    assert product.id == product_data["id"]
    assert product.name == product_data["name"]
    assert product.description == product_data["description"]
    assert product.price == product_data["price"]
    assert product.in_stock == product_data["in_stock"]
