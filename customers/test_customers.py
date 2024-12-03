import json
from testing_customers import app


def test_get_all_customers():
    """Test fetching all customers."""
    response = app.test_client().get('/get_all_customers')
    data = json.loads(response.get_data(as_text=True))
    assert "error" not in data and response.status_code == 200


def test_get_customer():
    """Test fetching a single customer by username."""
    username = "DanySolh21"
    response = app.test_client().get(f'/get_customer/{username}')
    data = json.loads(response.get_data(as_text=True))
    if response.status_code == 404:
        assert "error" in data
    else:
        assert "error" not in data and response.status_code == 200


def test_register_customer():
    """Test registering a new customer."""
    new_customer = {
        "username": "TestUser",
        "password": "Password123",
        "first_name": "John",
        "last_name": "Doe",
        "age": 25,
        "address": "123 Test St",
        "gender": "Male",
        "marital_status": "Single"
    }
    response = app.test_client().post('/register_customer', data=json.dumps(new_customer), content_type='application/json')
    data = json.loads(response.get_data(as_text=True))
    assert "error" not in data and response.status_code in [201, 200]


def test_update_customer():
    """Test updating a customer's details."""
    username = "TestUser"
    updates = {"first_name": "Jane"}
    response = app.test_client().patch(f'/update_customer/{username}', data=json.dumps(updates), content_type='application/json')
    data = json.loads(response.get_data(as_text=True))
    assert "error" not in data and response.status_code in [200, 404]


def test_delete_customer():
    """Test deleting a customer."""
    username = "TestUser"
    response = app.test_client().delete(f'/delete_customer/{username}')
    data = json.loads(response.get_data(as_text=True))
    assert "error" not in data and response.status_code in [200, 404]


def test_add_wishlist():
    """Test adding an item to a customer's wishlist."""
    username = "DanySolh21"
    good = {"good": "Lug Nuts"}
    response = app.test_client().post(f'/add_wishlist/{username}', data=json.dumps(good), content_type='application/json')
    data = json.loads(response.get_data(as_text=True))
    assert "error" not in data and response.status_code in [201, 200, 400]


def test_view_wishlist():
    """Test viewing a customer's wishlist."""
    username = "DanySolh21"
    response = app.test_client().get(f'/view_wishlist/{username}')
    data = json.loads(response.get_data(as_text=True))
    assert "error" not in data and response.status_code == 200


def test_remove_wishlist():
    """Test removing an item from a customer's wishlist."""
    username = "DanySolh21"
    good = {"good": "Lug Nuts"}
    response = app.test_client().delete(f'/remove_wishlist/{username}', data=json.dumps(good), content_type='application/json')
    data = json.loads(response.get_data(as_text=True))
    assert "error" not in data and response.status_code in [200, 404]


def test_charge_wallet():
    """Test charging a customer's wallet."""
    username = "DanySolh21"
    amount = {"amount": 50}
    response = app.test_client().patch(f'/charge_wallet/{username}', data=json.dumps(amount), content_type='application/json')
    data = json.loads(response.get_data(as_text=True))
    assert "error" not in data and response.status_code in [200, 404]


def test_deduct_wallet():
    """Test deducting funds from a customer's wallet."""
    username = "DanySolh21"
    amount = {"amount": 50}
    response = app.test_client().patch(f'/deduct_wallet/{username}', data=json.dumps(amount), content_type='application/json')
    data = json.loads(response.get_data(as_text=True))
    assert "error" not in data and response.status_code in [200, 404, 400]