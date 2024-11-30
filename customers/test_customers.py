import pytest
from customers import app
from flask import json

@pytest.fixture
def client():
    """Fixture to initialize Flask test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_all_customers(client):
    """Test fetching all customers."""
    response = client.get("/get_all_customers")
    assert response.status_code == 200
    assert isinstance(json.loads(response.get_data(as_text=True)), list)

def test_get_customer(client):
    """Test fetching a customer by username."""
    response = client.get("/get_customer/john_doe")
    if response.status_code == 404:
        assert json.loads(response.get_data(as_text=True)) == "Customer not found"
    else:
        assert response.status_code == 200
        assert "username" in json.loads(response.get_data(as_text=True))

def test_register_customer(client):
    """Test registering a new customer."""
    new_customer = {
        "username": "jane_doe",
        "password": "securepass",
        "first_name": "Jane",
        "last_name": "Doe",
        "age": 25,
        "address": "456 Elm St",
        "gender": "Female",
        "marital_status": "Single"
    }
    response = client.post("/register_customer", data=json.dumps(new_customer), content_type="application/json")
    assert response.status_code == 201
    assert json.loads(response.get_data(as_text=True))["message"] == "Customer registered successfully"

def test_update_customer(client):
    """Test updating a customer's details."""
    updates = {"age": 26, "address": "789 Pine St"}
    response = client.patch("/update_customer/jane_doe", data=json.dumps(updates), content_type="application/json")
    assert response.status_code == 200
    assert json.loads(response.get_data(as_text=True))["message"] == "Customer information updated successfully"

def test_delete_customer(client):
    """Test deleting a customer."""
    response = client.delete("/delete_customer/jane_doe")
    if response.status_code == 404:
        assert json.loads(response.get_data(as_text=True)) == "Customer not found"
    else:
        assert response.status_code == 200
        assert json.loads(response.get_data(as_text=True))["message"] == "Customer deleted successfully"

def test_charge_wallet(client):
    """Test charging a customer's wallet."""
    charge_data = {"amount": 100}
    response = client.patch("/charge_wallet/jane_doe", data=json.dumps(charge_data), content_type="application/json")
    assert response.status_code == 200
    assert json.loads(response.get_data(as_text=True))["message"] == "Wallet charged successfully"

def test_deduct_wallet(client):
    """Test deducting from a customer's wallet."""
    deduct_data = {"amount": 50}
    response = client.patch("/deduct_wallet/jane_doe", data=json.dumps(deduct_data), content_type="application/json")
    assert response.status_code == 200
    assert json.loads(response.get_data(as_text=True))["message"] == "Wallet deducted successfully"