from flask import Flask, render_template, url_for, request, redirect, session, jsonify
import requests
import json
from memory_profiler import profile  


app = Flask(__name__)

@app.route("/submit_review", methods=["POST", "GET"])
@profile
def submit_review():
    """
    Submits a customer's review of a product. Must pass in the post request the user's username, his password, the reviewed good, the review, and the rating.

    :return: Success message if submission is successful. Error message if submission already exists or other error occured.
    :rtype: flask.Response
    """
    info = request.get_json()
    user = info["user"]
    password = info["password"]

    customer = json.loads(requests.get("http://databaseAPI:3000/get_customer/"+user).content)
    if "error" not in customer and customer[2] == password:
        review = json.loads(requests.get("http://databaseAPI:3000/get_review/"+user+"/"+info["good"]).content)
        if review is not None:
            return jsonify("Review already exists for this product")
        data = {"user": user,
                "good": info["good"],
                "review": info["review"],
                "rating": info["rating"]}
        response = requests.post("http://databaseAPI:3000/submit", json=data)

        return response.content
    else:
        return jsonify("Invalid username or password")

@app.route("/update_review", methods=["PUT", "GET"])
@profile
def update_review():
    """
    Updates a customer's review of a product. Must pass in the put request the user's username, his password, the reviewed good, the review, and the rating.

    :return: Success message if update is successful. Error message if submission doesn't exist or other error occured.
    :rtype: flask.Response
    """
    info = request.get_json()
    user = info["user"]
    password = info["password"]

    customer = json.loads(requests.get("http://databaseAPI:3000/get_customer/"+user).content)
    if "error" not in customer and customer[2] == password:
        review = json.loads(requests.get("http://databaseAPI:3000/get_review/"+user+"/"+info["good"]).content)
        if review is not None:
            data = {"user": user,
                "good": info["good"],
                "review": info["review"],
                "rating": info["rating"]}
            
            response = requests.post("http://databaseAPI:3000/update", json=data)
            return response.content
        else:
            return jsonify("No reviews exists for this product")
    else:
        return jsonify("Invalid username or password")

@app.route("/delete_review", methods=["DELETE", "GET"])
@profile
def delete_review():
    """
    Deletes a customer's review of a product. Must pass in the delete request the user's username, his password, and the reviewed good.

    :return: Success message if delete is successful. Error message if submission doesn't exist or other error occured.
    :rtype: flask.Response
    """
    info = request.get_json()
    user = info["user"]
    password = info["password"]

    customer = json.loads(requests.get("http://databaseAPI:3000/get_customer/"+user).content)
    if "error" not in customer and customer[2] == password:
        review = json.loads(requests.get("http://databaseAPI:3000/get_review/"+user+"/"+info["good"]).content)
        if review is not None:
            data = {"user": user,
                "good": info["good"]}
            
            response = requests.post("http://databaseAPI:3000/delete", json=data)
            return response.content
        else:
            return jsonify("No reviews exists for this product")
    else:
        return jsonify("Invalid username or password")

@app.route("/admin_delete_review", methods=["DELETE", "GET"])
@profile
def admin_delete_review():
    """
    Deletes a customer's review of a product by the admin. Must pass in the post request the user's username, the reviewed good, and the admin's credentials.

    :return: Success message if delete is successful. Error message if submission doesn't exist or other error occured.
    :rtype: flask.Response
    """
    info = request.get_json()
    user = info["user"]
    admin_user = info["admin_user"]
    password = info["password"]

    admin = json.loads(requests.get("http://databaseAPI:3000/get_admin/"+admin_user).content)
    if "error" not in admin and admin[2] == password:
        review = json.loads(requests.get("http://databaseAPI:3000/get_review/"+user+"/"+info["good"]).content)
        if review is not None:
            data = {"user": user,
                "good": info["good"]}
            
            response = requests.post("http://databaseAPI:3000/delete", json=data)
            return response.content
        else:
            return jsonify("No reviews exists for this product")
    else:
        return jsonify("Invalid username or password")

@app.route("/get_review/<string:user>/<string:good>", methods=["GET"])
@profile
def get_review(user, good):
    """
    Get a customer's review of a product.

    :param user: The username of the customer.
    :type user: str
    :param good: The reviewed good
    :type good: str
    :return: If successful, the review submitted by the user about the product. Else, an error message.
    :rtype: flask.Response
    """
    review = requests.get("http://databaseAPI:3000/get_review/"+user+"/"+good).content
    if review is None:
        return jsonify("This user didn't review this product")
    return review

@app.route("/get_product_review/<string:good>", methods=["GET"])
@profile
def get_product_review(good):
    """
    Get all reviews of a product.

    :param good: The reviewed good
    :type good: str
    :return: If successful, the reviews of the product. Else, an error message.
    :rtype: flask.Response
    """
    reviews = requests.get("http://databaseAPI:3000/get_reviews_product/"+good).content
    if len(json.loads(reviews))==0:
        return jsonify("This product doesn't have any reviews")
    return reviews

@app.route("/get_user_review/<string:user>", methods=["GET"])
@profile
def get_user_review(user):
    """
    Get all reviews submitted by a customer.

    :param user: The username of the customer.
    :type user: str
    :return: If successful, all reviews submitted by a customer. Else, an error message.
    :rtype: flask.Response
    """
    reviews = requests.get("http://databaseAPI:3000/get_reviews_user/"+user).content
    if len(json.loads(reviews))==0:
        return jsonify("This user didn't submit any reviews")
    return reviews

@app.route("/flag_review", methods=["PUT", "GET"])
@profile
def flag_review():
    """
    Allows to flag a customer's review by either a user or an admin. Need to pass in the put request the flag's value, the reviewed good, and the corresponding username.

    :return: Success message if flag changed successfully. Error message in case of a problem.
    :rtype: flask.Response
    """
    info = request.get_json()
    response = requests.post("http://databaseAPI:3000/flag", json=info)
    return response.content

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5002)
