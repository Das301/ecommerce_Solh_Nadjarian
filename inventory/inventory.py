from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

@app.route("/add_good", methods=["POST"])
def add_good():
    """
    Add a new good to the inventory.

    :return: Response from the inventory service after adding the good.
    :rtype: flask.Response
    """
    info = request.get_json()
    response = requests.post("http://databaseAPI:3000/add_good", json=info)
    return response.content


@app.route("/deduct_good", methods=["PATCH"])
def deduct_good():
    """
    Deduct stock for a specific good.

    :return: Response from the inventory service after deducting stock.
    :rtype: flask.Response
    """
    info = request.get_json()
    response = requests.patch(f"http://databaseAPI:3000/deduct_good/{info['id']}", json={"quantity": info["quantity"]})
    return response.content


@app.route("/update_good", methods=["PATCH"])
def update_good():
    """
    Update details of a good.

    :return: Response from the inventory service after updating the good details.
    :rtype: flask.Response
    """
    info = request.get_json()
    response = requests.patch(f"http://databaseAPI:3000/update_good/{info['id']}", json=info["updates"])
    return response.content


@app.route("/health/inventory", methods=["GET"])
def health_check_inventory():
    """
    Health check for the inventory service.

    :return: JSON response indicating the health status of the inventory service.
    :rtype: flask.Response
    """
    status = {"service": "inventory", "status": "ok"}
    try:
        response = requests.get("http://databaseAPI:3000/health")
        if response.status_code == 200:
            status["databaseAPI"] = "reachable"
        else:
            status["status"] = "degraded"
            status["databaseAPI"] = "unreachable"
    except requests.exceptions.RequestException as e:
        print(e)
        status["status"] = "degraded"
        status["databaseAPI"] = "unreachable"
    return jsonify(status), 200 if status["status"] == "ok" else 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004, debug=True)