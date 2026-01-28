from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import csv
app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

@app.route("/")
def home():
    return "Flask is working!"


@app.route("/data", methods=["GET"])
def get_data():
    filename = "users.csv"
    data = []
    with open(filename, mode='r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:
            data.append(row)
    return jsonify({
        "message": "Data from Flask backend",
        "users": data
    })

if __name__ == "__main__":
    app.run(debug=True)
