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
        print(data)
        conn.close()
    except:
        data = "Database Error"
    
    return jsonify(data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=3000)