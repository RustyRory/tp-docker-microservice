from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # permet à tous les frontends d’accéder à l’API

@app.route("/api/message")
def message():
    return jsonify({"message": "Hello from backend"})

app.run(host="0.0.0.0", port=5000)