import unittest
from testing_customers import app 


class TestCustomersAPI(unittest.TestCase):
    def setUp(self):
        """Set up the test client."""
        self.client = app.test_client()

    def test_get_all_customers(self):
        """Test the endpoint to fetch all customers."""
        response = self.client.get("/get_all_customers")
        self.assertEqual(response.status_code, 200)

    def test_get_customer(self):
        """Test fetching a customer by username."""
        response = self.client.get("/get_customer/testuser")
        self.assertIn(response.status_code, [200, 404])

    def test_register_customer(self):
        """Test customer registration."""
        payload = {
            "username": "testuser",
            "full_name": "Test User",
            "password": "password123",
            "age": 25,
            "address": "123 Main St",
            "gender": "Male",
            "marital_status": "Single"
        }
        response = self.client.post("/register_customer", json=payload)
        self.assertIn(response.status_code, [200, 201, 400])

    def test_update_customer(self):
        """Test updating customer details."""
        payload = {"address": "456 New St"}
        response = self.client.patch("/update_customer/testuser", json=payload)
        self.assertIn(response.status_code, [200, 404])

    def test_delete_customer(self):
        """Test deleting a customer."""
        response = self.client.delete("/delete_customer/testuser")
        self.assertIn(response.status_code, [200, 404])

    def test_charge_wallet(self):
        """Test charging a customer's wallet."""
        payload = {"amount": 50}
        response = self.client.patch("/charge_wallet/testuser", json=payload)
        self.assertIn(response.status_code, [200, 404])

    def test_deduct_wallet(self):
        """Test deducting from a customer's wallet."""
        payload = {"amount": 30}
        response = self.client.patch("/deduct_wallet/testuser", json=payload)
        self.assertIn(response.status_code, [200, 404])


if __name__ == "__main__":
    unittest.main()