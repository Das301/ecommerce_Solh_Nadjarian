from flask import Flask, render_template, url_for, request, redirect, session, jsonify
import requests
import json

app = Flask(__name__)

@app.route("/get_available_goods", methods=["GET"])
def get_available_goods():
    response = requests.get("http://127.0.0.1:3000/get_goods")
    return response.content

@app.route("/get_good_details/<int:id>", methods=["GET"])
def get_good_details(id):
    response = requests.get("http://127.0.0.1:3000/get_good/"+str(id))
    return response.content

@app.route("/record_sales", methods=["POST"])
def record_sales():
    info = request.get_json()
    user = info["user"]
    good = info["good"]
    quantity = info["quantity"]

    customer = json.loads(requests.get("http://127.0.0.1:3000/get_customer/"+user).content)
    price = json.loads(requests.get("http://127.0.0.1:3000/get_good_price/"+good).content)
    if customer=="Database Error" or price == "Database Error":
        return jsonify("Database Error")
    
    total_amount = price[0]*quantity
    if total_amount > customer[-1]:
        return jsonify("Not enough funds in wallet")
    if price[1] < quantity:
        return jsonify("Not enough stocks")
    
    data = {"user": user,
            "good": good,
            "quantity": quantity,
            "total": total_amount}
    response = requests.post("http://127.0.0.1:3000/perform_transaction", json=data)

    return response.content

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5001)