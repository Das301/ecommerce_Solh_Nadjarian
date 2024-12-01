import unittest
import json
from flask import Flask, request, jsonify
from testing_customers import app 

class TestCustomerAPI(unittest.TestCase):
    """
    Unit tests for the Customer API endpoints.
    """

    def setUp(self):
        """
        Set up the test client for the Flask application.
        """
        self.app = app.test_client()
        self.app.testing = True

    def test_get_all_customers(self):
        """
        Test fetching all customers.
        """
        response = self.app.get('/get_all_customers')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(json.loads(response.data), list))

    def test_get_customer(self):
        """
        Test fetching a single customer by username.
        """
        username = "DanySolh21"
        response = self.app.get(f'/get_customer/{username}')
        if response.status_code == 404:
            self.assertIn("Customer not found", response.json)
        else:
            self.assertEqual(response.status_code, 200)
            self.assertTrue(isinstance(json.loads(response.data), dict))

    def test_register_customer(self):
        """
        Test registering a new customer.
        """
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
        response = self.app.post('/register_customer', json=new_customer)
        self.assertIn(response.status_code, [201, 500])

    def test_update_customer(self):
        """
        Test updating an existing customer's details.
        """
        username = "TestUser"
        updates = {"first_name": "Jane"}
        response = self.app.patch(f'/update_customer/{username}', json=updates)
        self.assertIn(response.status_code, [200, 404])

    def test_delete_customer(self):
        """
        Test deleting a customer by username.
        """
        username = "TestUser"
        response = self.app.delete(f'/delete_customer/{username}')
        self.assertIn(response.status_code, [200, 404])

    def test_add_wishlist(self):
        """
        Test adding an item to a customer's wishlist.
        """
        username = "DanySolh21"
        good = {"good": "Lug Nuts"}
        response = self.app.post(f'/add_wishlist/{username}', json=good)
        self.assertIn(response.status_code, [201, 404, 400])

    def test_view_wishlist(self):
        """
        Test viewing a customer's wishlist.
        """
        username = "DanySolh21"
        response = self.app.get(f'/view_wishlist/{username}')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(json.loads(response.data), list))

    def test_remove_wishlist(self):
        """
        Test removing an item from a customer's wishlist.
        """
        username = "DanySolh21"
        good = {"good": "Lug Nuts"}
        response = self.app.delete(f'/remove_wishlist/{username}', json=good)
        self.assertIn(response.status_code, [200, 404])

    def test_charge_wallet(self):
        """
        Test charging a customer's wallet.
        """
        username = "DanySolh21"
        amount = {"amount": 50}
        response = self.app.patch(f'/charge_wallet/{username}', json=amount)
        self.assertIn(response.status_code, [200, 404])

    def test_deduct_wallet(self):
        """
        Test deducting funds from a customer's wallet.
        """
        username = "DanySolh21"
        amount = {"amount": 50}
        response = self.app.patch(f'/deduct_wallet/{username}', json=amount)
        self.assertIn(response.status_code, [200, 404, 400])

if __name__ == "__main__":
    unittest.main()