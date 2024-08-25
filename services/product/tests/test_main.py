# test_main.py
import pytest
from fastapi.testclient import TestClient
from product.main import app

client = TestClient(app)

@pytest.fixture
def product_data():
    return {
        "name": "Test Product",
        "description": "Test Description",
        "price": 10.0,
        "in_stock": 100
    }

def test_create_product(product_data):
    response = client.post("/products/", json=product_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["description"] == product_data["description"]
    assert data["price"] == product_data["price"]
    assert data["in_stock"] == product_data["in_stock"]

def test_read_product(product_data):
    # First create a product
    response = client.post("/products/", json=product_data)
    product_id = response.json()["id"]

    # Now read the product
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["description"] == product_data["description"]
    assert data["price"] == product_data["price"]
    assert data["in_stock"] == product_data["in_stock"]

def test_update_product(product_data):
    # First create a product
    response = client.post("/products/", json=product_data)
    product_id = response.json()["id"]

    updated_data = {
        "name": "Updated Product",
        "description": "Updated Description",
        "price": 15.0,
        "in_stock": 150
    }

    # Now update the product
    response = client.put(f"/products/{product_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == updated_data["name"]
    assert data["description"] == updated_data["description"]
    assert data["price"] == updated_data["price"]
    assert data["in_stock"] == updated_data["in_stock"]

def test_delete_product(product_data):
    # First create a product
    response = client.post("/products/", json=product_data)
    product_id = response.json()["id"]

    # Now delete the product
    response = client.delete(f"/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data == {"ok": True}

    # Verify the product is deleted
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 404
