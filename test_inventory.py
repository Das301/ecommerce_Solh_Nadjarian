import pytest
from inventory import app
from flask import json

@pytest.fixture
def client():
    """Fixture to initialize Flask test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_add_good(client):
    """Test adding a new good to the inventory."""
    good_data = {
        "name": "Laptop",
        "category": "Electronics",
        "price": 1500,
        "description": "High-end gaming laptop",
        "stocks": 20
    }
    response = client.post("/add_good", data=json.dumps(good_data), content_type="application/json")
    assert response.status_code == 201
    assert json.loads(response.get_data(as_text=True))["message"] == "Good added successfully"

def test_deduct_good(client):
    """Test deducting stock for an existing good."""
    deduct_data = {"id": 1, "quantity": 5}
    response = client.patch("/deduct_good", data=json.dumps(deduct_data), content_type="application/json")
    assert response.status_code == 200
    assert json.loads(response.get_data(as_text=True))["message"] == "Stock deducted successfully"

def test_deduct_good_insufficient_stock(client):
    """Test deducting stock with insufficient quantity."""
    deduct_data = {"id": 1, "quantity": 50}  # Assume 50 exceeds available stock
    response = client.patch("/deduct_good", data=json.dumps(deduct_data), content_type="application/json")
    assert response.status_code == 400
    assert json.loads(response.get_data(as_text=True))["error"] == "Not enough stock available"

def test_update_good(client):
    """Test updating an existing good."""
    update_data = {
        "id": 1,
        "updates": {"price": 1400, "stocks": 25}
    }
    response = client.patch("/update_good", data=json.dumps(update_data), content_type="application/json")
    assert response.status_code == 200
    assert json.loads(response.get_data(as_text=True))["message"] == "Good updated successfully"