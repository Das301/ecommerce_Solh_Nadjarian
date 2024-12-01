import unittest
from testing_reviews import app

class TestReviewsAPI(unittest.TestCase):
    def setUp(self):
        """Set up the Flask test client."""
        self.client = app.test_client()

    def test_submit_review(self):
        """Test the /submit_review endpoint."""
        payload = {
            "user": "testuser",
            "password": "password123",
            "good": "Test Product",
            "review": "Great product!",
            "rating": 5
        }
        response = self.client.post("/submit_review", json=payload)
        self.assertIn(response.status_code, [200, 400])

    def test_update_review(self):
        """Test the /update_review endpoint."""
        payload = {
            "user": "testuser",
            "password": "password123",
            "good": "Test Product",
            "review": "Updated review content",
            "rating": 4
        }
        response = self.client.put("/update_review", json=payload)
        self.assertIn(response.status_code, [200, 400])

    def test_delete_review(self):
        """Test the /delete_review endpoint."""
        payload = {
            "user": "testuser",
            "password": "password123",
            "good": "Test Product"
        }
        response = self.client.delete("/delete_review", json=payload)
        self.assertIn(response.status_code, [200, 400])

    def test_admin_delete_review(self):
        """Test the /admin_delete_review endpoint."""
        payload = {
            "user": "testuser",
            "admin_user": "admin",
            "password": "adminpass123",
            "good": "Test Product"
        }
        response = self.client.delete("/admin_delete_review", json=payload)
        self.assertIn(response.status_code, [200, 400])

    def test_get_review(self):
        """Test the /get_review/<user>/<good> endpoint."""
        response = self.client.get("/get_review/testuser/Test Product")
        self.assertIn(response.status_code, [200, 404])

    def test_get_product_review(self):
        """Test the /get_product_review/<good> endpoint."""
        response = self.client.get("/get_product_review/Test Product")
        self.assertIn(response.status_code, [200, 404])

    def test_get_user_review(self):
        """Test the /get_user_review/<user> endpoint."""
        response = self.client.get("/get_user_review/testuser")
        self.assertIn(response.status_code, [200, 404])

    def test_flag_review(self):
        """Test the /flag_review endpoint."""
        payload = {
            "user": "testuser",
            "good": "Test Product",
            "flag": True
        }
        response = self.client.put("/flag_review", json=payload)
        self.assertIn(response.status_code, [200, 400])

if __name__ == "__main__":
    unittest.main()