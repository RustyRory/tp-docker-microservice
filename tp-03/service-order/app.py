import requests
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/orders", methods=["GET"])

def get_orders():
    users = requests.get("http://service-user:5001/users").json()
    return jsonify({"orders": ["Order 1 for " + users[0]["name"], "Order 2 for " + users[1]["name"]]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)