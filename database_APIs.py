from flask import Flask, render_template, url_for, request, redirect, session, jsonify
import sqlite3

app = Flask(__name__)

def connect_to_db():
    conn = sqlite3.connect("eCommerce.db")
    return conn

@app.route("/get_all_customers", methods=["GET"])
def get_all_customers():
    """Fetch all customers."""
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM USERS")
        customers = cursor.fetchall()
        conn.close()
    except Exception as e:
        print(e)
        return jsonify({"error": "Database Error"}), 500
    return jsonify(customers)

@app.route("/get_customer/<string:username>", methods=["GET"])
def get_customer(username):
    """Fetch a customer by username."""
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM USERS WHERE username = ?", (username,))
        customer = cursor.fetchone()
        conn.close()
        if customer:
            return jsonify(customer)
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        print(e)
        return jsonify({"error": "Database Error"}), 500

@app.route("/register_customer", methods=["POST"])
def register_customer():
    """Register a new customer."""
    data = request.get_json()
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO USERS (username, password, first_name, last_name, age, address, gender, marital_status, wallet)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
            data["username"], data["password"], data["first_name"], data["last_name"],
            data["age"], data["address"], data["gender"], data["marital_status"], 0))
        conn.commit()
        conn.close()
        return jsonify({"message": "Customer registered successfully"}), 201
    except Exception as e:
        print(e)
        return jsonify({"error": "Database Error"}), 500

@app.route("/delete_customer/<string:username>", methods=["DELETE"])
def delete_customer(username):
    """Delete a customer."""
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM USERS WHERE username = ?", (username,))
        conn.commit()
        conn.close()
        return jsonify({"message": "Customer deleted successfully"}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "Database Error"}), 500

@app.route("/charge_wallet/<string:username>", methods=["PATCH"])
def charge_wallet(username):
    """Add funds to a customer's wallet."""
    data = request.get_json()
    if "amount" not in data:
        return jsonify({"error": "Amount is required"}), 400

    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT wallet FROM USERS WHERE username = ?", (username,))
        user = cursor.fetchone()
        if not user:
            return jsonify({"error": "User not found"}), 404
        cursor.execute("UPDATE USERS SET wallet = wallet + ? WHERE username = ?", (data["amount"], username))
        conn.commit()
        conn.close()
        return jsonify({"message": "Wallet charged successfully"}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "Database Error"}), 500

@app.route("/deduct_wallet/<string:username>", methods=["PATCH"])
def deduct_wallet(username):
    """Deduct funds from a customer's wallet."""
    data = request.get_json()
    if "amount" not in data:
        return jsonify({"error": "Amount is required"}), 400

    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT wallet FROM USERS WHERE username = ?", (username,))
        user = cursor.fetchone()
        if not user:
            return jsonify({"error": "User not found"}), 404
        current_balance = user[0]  # Wallet balance
        if current_balance < data["amount"]:
            return jsonify({"error": "Insufficient funds"}), 400
        cursor.execute("UPDATE USERS SET wallet = wallet - ? WHERE username = ?", (data["amount"], username))
        conn.commit()
        conn.close()
        return jsonify({"message": "Wallet deducted successfully"}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "Database Error"}), 500

@app.route("/update_customer/<string:username>", methods=["PATCH"])
def update_customer(username):
    """Update a customer's information dynamically."""
    data = request.get_json()

    if not data:
        return jsonify({"error": "No fields to update provided"}), 400

    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM USERS WHERE username = ?", (username,))
        existing_user = cursor.fetchone()
        if not existing_user:
            return jsonify({"error": "User not found"}), 404
        
        fields = []
        values = []
        for key, value in data.items():
            fields.append(f"{key} = ?")
            values.append(value)

        if not fields:
            return jsonify({"error": "No valid fields to update"}), 400

        query = f"UPDATE USERS SET {', '.join(fields)} WHERE username = ?"
        values.append(username)
        cursor.execute(query, values)
        conn.commit()
        conn.close()

        return jsonify({"message": "Customer information updated successfully"}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "Database Error"}), 500
    
@app.route("/get_goods", methods=["POST", "GET"])
def get_goods():
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT name, price FROM GOODS WHERE stocks > 0")
        data = cursor.fetchall()
        conn.close()
    except:
        conn.rollback()
        return jsonify({"error": "Database Error"}), 500
    
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
        conn.rollback()
        return jsonify({"error": "Database Error"}), 500
    
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
        conn.rollback()
        return jsonify({"error": "Database Error"}), 500
    
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
        conn.rollback()
        return jsonify({"error": "Database Error"}), 500
    
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
        conn.rollback()
        return jsonify({"error": "Database Error"}), 500
    
    return jsonify(message)

@app.route("/update", methods=["POST"])
def update():
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        data = request.get_json()

        cursor.execute("UPDATE REVIEWS SET review = ?, rating = ? WHERE user=? AND good=?", (data["review"], data["rating"], data["user"], data["good"]))

        conn.commit()
        conn.close()
        message = "Review updated Successfully"
    except Exception as e:
        print(e)
        conn.rollback()
        return jsonify({"error": "Database Error"}), 500
    
    return jsonify(message)

@app.route("/delete", methods=["POST"])
def delete():
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        data = request.get_json()

        cursor.execute("DELETE FROM REVIEWS WHERE user=? AND good=?", (data["user"], data["good"]))

        conn.commit()
        conn.close()
        message = "Review Deleted Successfully"
    except Exception as e:
        print(e)
        conn.rollback()
        return jsonify({"error": "Database Error"}), 500
    
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
        conn.rollback()
        return jsonify({"error": "Database Error"}), 500
    
    return jsonify(data)

@app.route("/get_reviews_product/<string:good>", methods=["GET"])
def get_reviews_product(good):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM REVIEWS WHERE good = ?", (good, ))
        data = cursor.fetchall()
        conn.close()
    except Exception as e:
        print(e)
        conn.rollback()
        return jsonify({"error": "Database Error"}), 500
    
    return jsonify(data)

@app.route("/get_reviews_user/<string:user>", methods=["GET"])
def get_reviews_user(user):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM REVIEWS WHERE user = ?", (user, ))
        data = cursor.fetchall()
        conn.close()
    except Exception as e:
        print(e)
        conn.rollback()
        return jsonify({"error": "Database Error"}), 500
    
    return jsonify(data)

@app.route("/get_admin/<string:username>", methods=["GET"])
def get_admin(username):
    """Fetch an admin by username."""
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ADMINS WHERE username = ?", (username,))
        customer = cursor.fetchone()
        conn.close()
        if customer:
            return jsonify(customer)
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        print(e)
        return jsonify({"error": "Database Error"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=3000)