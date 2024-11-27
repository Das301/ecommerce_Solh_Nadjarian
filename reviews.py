from flask import Flask, render_template, url_for, request, redirect, session, jsonify
import requests
import json

app = Flask(__name__)

@app.route("/submit_review", methods=["POST"])
def submit_review():
    info = request.get_json()
    user = info["user"]
    password = info["password"]

    customer = json.loads(requests.get("http://127.0.0.1:3000/get_customer/"+user).content)
    if customer is not None and customer[2] == password:
        review = json.loads(requests.get("http://127.0.0.1:3000/get_review/"+user+"/"+info["good"]).content)
        if review is not None:
            return jsonify("Review already exists for this product")
        data = {"user": user,
                "good": info["good"],
                "review": info["review"],
                "rating": info["rating"]}
        response = requests.post("http://127.0.0.1:3000/submit", json=data)

        return response.content
    else:
        return jsonify("Invalid username or password")

@app.route("/update_review", methods=["PUT"])
def update_review():
    info = request.get_json()
    user = info["user"]
    password = info["password"]

    customer = json.loads(requests.get("http://127.0.0.1:3000/get_customer/"+user).content)
    if customer is not None and customer[2] == password:
        review = json.loads(requests.get("http://127.0.0.1:3000/get_review/"+user+"/"+info["good"]).content)
        if review is not None:
            data = {"user": user,
                "good": info["good"],
                "review": info["review"],
                "rating": info["rating"]}
            
            response = requests.post("http://127.0.0.1:3000/update", json=data)
            return response.content
        else:
            return jsonify("No reviews exists for this product")
    else:
        return jsonify("Invalid username or password")

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5002)
