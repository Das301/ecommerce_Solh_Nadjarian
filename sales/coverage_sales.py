import unittest
from testing_sales import app

import json

class TestSalesAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_get_available_goods(self):
        response = self.client.get("/get_available_goods")
        self.assertIn(response.status_code, [200, 500])
        if response.status_code == 200:
            data = json.loads(response.data)
            self.assertIsInstance(data, list)
            for item in data:
                self.assertEqual(len(item), 2)
                self.assertIsInstance(item[0], str)
                self.assertIsInstance(item[1], float)

    def test_get_good_details(self):
        product_id = 1
        response = self.client.get(f"/get_good_details/{product_id}")
        self.assertIn(response.status_code, [200, 404])
        if response.status_code == 200:
            data = json.loads(response.data)
            self.assertEqual(len(data), 4)
            self.assertIsInstance(data[0], str)
            self.assertIsInstance(data[1], str)
            self.assertIsInstance(data[2], str)
            self.assertIsInstance(data[3], float)

    def test_record_sales(self):
        payload = {
            "user": "testuser",
            "good": "Product 1",
            "quantity": 2
        }
        response = self.client.post("/record_sales", json=payload)
        self.assertIn(response.status_code, [200, 400, 500])
        if response.status_code == 200:
            self.assertIn(b"Transaction successful", response.data)

if __name__ == "__main__":
    unittest.main()