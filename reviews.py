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
    if "error" not in customer and customer[2] == password:
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
    if "error" not in customer and customer[2] == password:
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

@app.route("/delete_review", methods=["DELETE"])
def delete_review():
    info = request.get_json()
    user = info["user"]
    password = info["password"]

    customer = json.loads(requests.get("http://127.0.0.1:3000/get_customer/"+user).content)
    if "error" not in customer and customer[2] == password:
        review = json.loads(requests.get("http://127.0.0.1:3000/get_review/"+user+"/"+info["good"]).content)
        if review is not None:
            data = {"user": user,
                "good": info["good"]}
            
            response = requests.post("http://127.0.0.1:3000/delete", json=data)
            return response.content
        else:
            return jsonify("No reviews exists for this product")
    else:
        return jsonify("Invalid username or password")

@app.route("/admin_delete_review", methods=["DELETE"])
def admin_delete_review():
    info = request.get_json()
    user = info["user"]
    admin_user = info["admin_user"]
    password = info["password"]

    admin = json.loads(requests.get("http://127.0.0.1:3000/get_admin/"+admin_user).content)
    print(admin)
    if "error" not in admin and admin[2] == password:
        review = json.loads(requests.get("http://127.0.0.1:3000/get_review/"+user+"/"+info["good"]).content)
        if review is not None:
            data = {"user": user,
                "good": info["good"]}
            
            response = requests.post("http://127.0.0.1:3000/delete", json=data)
            return response.content
        else:
            return jsonify("No reviews exists for this product")
    else:
        return jsonify("Invalid username or password")

@app.route("/get_review/<string:user>/<string:good>", methods=["GET"])
def get_review(user, good):
    review = requests.get("http://127.0.0.1:3000/get_review/"+user+"/"+good).content
    if review is None:
        return jsonify("This user didn't review this product")
    return review

@app.route("/get_product_review/<string:good>", methods=["GET"])
def get_product_review(good):
    reviews = requests.get("http://127.0.0.1:3000/get_reviews_product/"+good).content
    if len(json.loads(reviews))==0:
        return jsonify("This product doesn't have any reviews")
    return reviews

@app.route("/get_user_review/<string:user>", methods=["GET"])
def get_user_review(user):
    reviews = requests.get("http://127.0.0.1:3000/get_reviews_user/"+user).content
    if len(json.loads(reviews))==0:
        return jsonify("This user didn't submit any reviews")
    return reviews

@app.route("/flag_review", methods=["PUT"])
def flag_review():
    info = request.get_json()
    response = requests.post("http://127.0.0.1:3000/flag", json=info)
    return response.content

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5002)
