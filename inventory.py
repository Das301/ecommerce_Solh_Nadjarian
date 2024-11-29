from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

BASE_URL = "http://127.0.0.1:3002"  # Backend API for Inventory Service

@app.route("/add_good", methods=["POST"])
def add_good():
    """Add a new good to the inventory."""
    data = request.get_json()
    response = requests.post(f"{BASE_URL}/add_good", json=data)
    return response.content

@app.route("/deduct_good/<int:id>", methods=["PATCH"])
def deduct_good(id):
    """Deduct a quantity of a good from the inventory."""
    data = request.get_json()
    response = requests.patch(f"{BASE_URL}/deduct_good/{id}", json=data)
    return response.content

@app.route("/update_good/<int:id>", methods=["PATCH"])
def update_good(id):
    """Update one or more fields of a good."""
    data = request.get_json()
    response = requests.patch(f"{BASE_URL}/update_good/{id}", json=data)
    return response.content

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004, debug=True)