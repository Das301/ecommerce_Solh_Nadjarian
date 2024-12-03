import cProfile
import pstats
from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

@app.route("/get_all_customers", methods=["GET"])
def get_all_customers():
    """Fetch all customers."""
    response = requests.get("http://localhost:3000/get_all_customers")
    return response.content


@app.route("/get_customer/<string:username>", methods=["GET"])
def get_customer(username):
    """Fetch a customer by username."""
    response = requests.get(f"http://localhost:3000/get_customer/{username}")
    if response.status_code == 404:
        return jsonify("Customer not found"), 404
    return response.content


@app.route("/register_customer", methods=["POST"])
def register_customer():
    """Register a new customer."""
    info = request.get_json()
    response = requests.post("http://localhost:3000/register_customer", json=info)
    return response.content


if __name__ == "__main__":
    profile = cProfile.Profile()
    profile.enable()

    app.run(host='0.0.0.0', port=5003, debug=True)

    profile.disable()
    stats = pstats.Stats(profile)
    stats.sort_stats("cumulative").print_stats(10)  