from flask import Flask, render_template, url_for, request, redirect, session, jsonify
import sqlite3

app = Flask(__name__)

def connect_to_db():
    conn = sqlite3.connect("eCommerce.db")
    return conn


@app.route("/get_goods", methods=["POST", "GET"])
def get_goods():
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT name, price FROM GOODS WHERE stocks > 0")
        data = cursor.fetchall()
        conn.close()
    except:
        data = "Database Error"
    
    return jsonify(data)


@app.route("/get_good/<int:id>", methods=["POST", "GET"])
def get_good(id):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT name, description, category, price FROM GOODS WHERE id = ?", (id,))
        data = cursor.fetchone()
        conn.close()
    except Exception as e:
        print(e)
        data = "Database Error"
    
    return jsonify(data)


@app.route("/get_customer/<string:user>", methods=["GET"])
def get_customer(user):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM USERS WHERE username = ?", (user,))
        data = cursor.fetchone()
        conn.close()
    except Exception as e:
        print(e)
        data = "Database Error"
    
    return jsonify(data)

@app.route("/get_good_price/<string:name>", methods=["GET"])
def get_good_price(name):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT price, stocks FROM GOODS WHERE name = ?", (name,))
        data = cursor.fetchone()
        conn.close()
    except Exception as e:
        print(e)
        data = "Database Error"
    
    return jsonify(data)

@app.route("/perform_transaction", methods=["POST"])
def perform_transaction():
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        data = request.get_json()

        cursor.execute("UPDATE USERS SET wallet = wallet - ? WHERE username = ?", (data["total"], data["user"]))
        cursor.execute("UPDATE GOODS SET stocks = stocks - ? WHERE name = ?", (data["quantity"], data["good"]))
        cursor.execute("INSERT INTO PURCHASES (user, good, quantity, total_price) VALUES(?, ?, ?, ?)", (data["user"], data["good"], data["quantity"], data["total"]))

        conn.commit()
        conn.close()
        message = "Purchase Successful"
    except Exception as e:
        print(e)
        message = "Database Error"
    
    return jsonify(message)

@app.route("/submit", methods=["POST"])
def submit():
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        data = request.get_json()

        cursor.execute("INSERT INTO REVIEWS (user, good, review, rating) VALUES(?, ?, ?, ?)", (data["user"], data["good"], data["review"], data["rating"]))

        conn.commit()
        conn.close()
        message = "Review Submitted Successfully"
    except Exception as e:
        print(e)
        message = "Database Error"
    
    return jsonify(message)

@app.route("/get_review/<string:user>/<string:good>", methods=["GET"])
def get_review(user, good):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM REVIEWS WHERE user = ? AND good = ?", (user, good))
        data = cursor.fetchone()
        conn.close()
    except Exception as e:
        print(e)
        data = "Database Error"
    
    return jsonify(data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=3000)