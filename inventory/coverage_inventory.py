import unittest
from testing_inventory import app

class TestInventoryAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_add_good(self):
        payload = {
            "name": "Test Good",
            "category": "Test Category",
            "price": 100.0,
            "count": 10
        }
        response = self.client.post("/add_good", json=payload)
        self.assertIn(response.status_code, [200, 201, 400])

    def test_deduct_good(self):
        payload = {"id": 1, "quantity": 5}
        response = self.client.patch("/deduct_good", json=payload)
        self.assertIn(response.status_code, [200, 400])

    def test_update_good(self):
        payload = {"id": 1, "updates": {"price": 120}}
        response = self.client.patch("/update_good", json=payload)
        self.assertIn(response.status_code, [200, 400])

if __name__ == "__main__":
    unittest.main()