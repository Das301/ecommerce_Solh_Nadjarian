from flask import Flask, render_template, url_for, request, redirect, session, jsonify
import requests

app = Flask(__name__)

@app.route("/get_available_goods", methods=["POST", "GET"])
def get_available_goods():
    response = requests.get("http://127.0.0.1:3000/get_goods")
    return response.content


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5001)