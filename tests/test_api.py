from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

@pytest.fixture
def setup_database():
    # Setup database before tests and teardown after tests
    # Use SQLAlchemy to create tables and add initial data
    yield
    # Drop tables or truncate data after tests

def test_read_items(setup_database):
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == []

def test_create_item(setup_database):
    response = client.post("/items/", json={"name": "Test item"})
    assert response.status_code == 200
    assert response.json() == {"name": "Test item"}