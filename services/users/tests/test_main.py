from fastapi.testclient import TestClient
from users.main import app
import pytest

client = TestClient(app)

@pytest.fixture(autouse=True)
def run_around_tests():
    # Setup before test
    yield
    # Teardown after test

def test_register_user():
    response = client.post("/register/", json={"username": "testuser", "email": "test@example.com", "password": "password"})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"

def test_login_user():
    response = client.post("/token", data={"username": "testuser", "password": "password"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
