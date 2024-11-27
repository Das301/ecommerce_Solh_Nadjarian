from flask import Flask, render_template, url_for, request, redirect, session, jsonify
import requests
import json

app = Flask(__name__)



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5002)
