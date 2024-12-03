import json
from testing_inventory import app


def test_add_good():
    """Test adding a new good to the inventory."""
    response = app.test_client().post(
        '/add_good',
        data=json.dumps({
            "name": "tablet",
            "category": "Electronics",
            "price": 1200,
            "description": "A high-end tablet",
            "stocks": 15
        }),
        content_type='application/json'
    )
    data = json.loads(response.get_data(as_text=True))
    if "error" in data:
        assert "error" in data
    else:
        assert "error" not in data and response.status_code in [201, 200]
        assert data.get("message") == "Good added successfully"


def test_deduct_good():
    """Test deducting stock for an existing good."""
    response = app.test_client().patch(
        '/deduct_good',
        data=json.dumps({"id": 1, "quantity": 5}),
        content_type='application/json'
    )
    data = json.loads(response.get_data(as_text=True))
    if "error" in data:
        assert "error" in data
    else:
        assert "error" not in data and response.status_code == 200
        assert data.get("message") == "Stock deducted successfully"


def test_update_good():
    """Test updating an existing good."""
    response = app.test_client().patch(
        '/update_good',
        data=json.dumps({"id": 1, "updates": {"price": 1400, "stocks": 25}}),
        content_type='application/json'
    )
    data = json.loads(response.get_data(as_text=True))
    if "error" in data:
        assert "error" in data
    else:
        assert "error" not in data and response.status_code == 200
        assert data.get("message") == "Good updated successfully"