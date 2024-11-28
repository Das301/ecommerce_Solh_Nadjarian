from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

BASE_URL = "http://127.0.0.1:3001" 

@app.route("/get_all_customers", methods=["GET"])
def get_all_customers():
    """Fetch all customers."""
    response = requests.get(f"{BASE_URL}/get_all_customers")
    return response.content


@app.route("/get_customer_details/<string:username>", methods=["GET"])
def get_customer_details(username):
    """Fetch details of a specific customer."""
    response = requests.get(f"{BASE_URL}/get_customer/{username}")
    return response.content


@app.route("/register_customer", methods=["POST"])
def register_customer():
    """Register a new customer."""
    data = request.get_json()
    response = requests.post(f"{BASE_URL}/register_customer", json=data)
    return response.content


@app.route("/delete_customer/<string:username>", methods=["DELETE"])
def delete_customer(username):
    """Delete a customer."""
    response = requests.delete(f"{BASE_URL}/delete_customer/{username}")
    return response.content


@app.route("/charge_wallet", methods=["POST"])
def charge_wallet():
    """Charge a customer's wallet."""
    info = request.get_json()
    username = info["username"]
    amount = info["amount"]

    response = requests.patch(f"{BASE_URL}/charge_wallet/{username}", json={"amount": amount})
    return response.content


@app.route("/deduct_wallet", methods=["POST"])
def deduct_wallet():
    """Deduct from a customer's wallet."""
    info = request.get_json()
    username = info["username"]
    amount = info["amount"]

    response = requests.patch(f"{BASE_URL}/deduct_wallet/{username}", json={"amount": amount})
    return response.content


@app.route("/update_customer/<string:username>", methods=["POST"])
def update_customer(username):
    """Update a customer's information."""
    data = request.get_json()
    response = requests.patch(f"{BASE_URL}/update_customer/{username}", json=data)
    return response.content


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5003)