from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

@app.route("/get_all_customers", methods=["GET"])
def get_all_customers():
    """Fetch all customers."""
    response = requests.get("http://databaseAPI:3000/get_all_customers")
    return response.content


@app.route("/get_customer/<string:username>", methods=["GET"])
def get_customer(username):
    """
    Fetch a customer by username.

    :param username: The username of the customer to fetch.
    :type username: str
    :return: Customer details if found, otherwise a 'not found' message.
    :rtype: flask.Response
    """
    response = requests.get(f"http://databaseAPI:3000/get_customer/{username}")
    if response.status_code == 404:
        return jsonify("Customer not found"), 404
    return response.content


@app.route("/register_customer", methods=["POST"])
def register_customer():
    """
    Register a new customer.

    :return: Success message if registration is successful.
    :rtype: flask.Response
    """
    info = request.get_json()
    response = requests.post("http://databaseAPI:3000/register_customer", json=info)
    return response.content


@app.route("/update_customer/<string:username>", methods=["PATCH"])
def update_customer(username):
    """
    Update a customer's details.

    :param username: The username of the customer whose details are to be updated.
    :type username: str
    :return: Success message if update is successful.
    :rtype: flask.Response
    """
    updates = request.get_json()
    response = requests.patch(f"http://databaseAPI:3000/update_customer/{username}", json=updates)
    return response.content


@app.route("/delete_customer/<string:username>", methods=["DELETE"])
def delete_customer(username):
    """
    Delete a customer.

    :param username: The username of the customer to delete.
    :type username: str
    :return: Success message if deletion is successful, or an error message if the customer is not found.
    :rtype: flask.Response
    """
    response = requests.delete(f"http://databaseAPI:3000/delete_customer/{username}")
    if response.status_code == 404:
        return jsonify("Customer not found"), 404
    return response.content


@app.route("/charge_wallet/<string:username>", methods=["PATCH"])
def charge_wallet(username):
    """
    Add funds to a customer's wallet.

    :param username: The username of the customer whose wallet is to be charged.
    :type username: str
    :return: Success message if wallet charging is successful.
    :rtype: flask.Response
    """
    info = request.get_json()
    response = requests.patch(f"http://databaseAPI:3000/charge_wallet/{username}", json={"amount": info["amount"]})
    return response.content


@app.route("/deduct_wallet/<string:username>", methods=["PATCH"])
def deduct_wallet(username):
    """
    Deduct funds from a customer's wallet.

    :param username: The username of the customer whose wallet is to be deducted.
    :type username: str
    :return: Success message if deduction is successful.
    :rtype: flask.Response
    """
    info = request.get_json()
    response = requests.patch(f"http://databaseAPI:3000/deduct_wallet/{username}", json={"amount": info["amount"]})
    return response.content


@app.route("/add_wishlist/<string:username>", methods=["POST"])
def add_wishlist(username):
    """
    Add a product to the user's wishlist.

    :param username: The username of the user.
    :type username: str
    :return: Success message if added successfully, error otherwise.
    :rtype: flask.Response
    """
    info = request.get_json()
    response = requests.post(f"http://localhost:3000/add_wishlist/{username}", json=info)
    return response.content


@app.route("/view_wishlist/<string:username>", methods=["GET"])
def view_wishlist(username):
    """
    View all products in a user's wishlist.

    :param username: The username of the user.
    :type username: str
    :return: Wishlist items as JSON or error message.
    :rtype: flask.Response
    """
    response = requests.get(f"http://databaseAPI:3000/view_wishlist/{username}")
    return response.content


@app.route("/remove_wishlist/<string:username>", methods=["DELETE"])
def remove_wishlist(username):
    """
    Remove a product from the user's wishlist.

    :param username: The username of the user.
    :type username: str
    :return: Success message if removed successfully, error otherwise.
    :rtype: flask.Response
    """
    info = request.get_json()
    response = requests.delete(f"http://databaseAPI:3000/remove_wishlist/{username}", json=info)
    return response.content


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5003)