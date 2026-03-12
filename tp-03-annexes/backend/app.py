from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, PyMongoError
import os
import time

app = Flask(__name__)
CORS(app)

# --- MongoDB connection avec auth ---
mongo_user = os.getenv("MONGO_USER", "admin")
mongo_password = os.getenv("MONGO_PASSWORD", "password123")
mongo_host = os.getenv("MONGO_HOST", "mongodb")
mongo_port = os.getenv("MONGO_PORT", "27017")
mongo_dbname = os.getenv("MONGO_DB", "tpdb")

mongo_uri = os.getenv("MONGO_URI")  # depuis ConfigMap
if not mongo_uri:
    mongo_uri = f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}/{mongo_dbname}?authSource=admin"
print("Connecting to MongoDB with URI:", mongo_uri)  # utile pour debug

def get_mongo_client(uri, retries=5):
    for i in range(retries):
        try:
            client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            client.server_info()  # test de connexion
            print("✅ MongoDB reachable!")
            return client
        except ServerSelectionTimeoutError as e:
            print(f"MongoDB not reachable yet ({i+1}/{retries}): {e}")
            time.sleep(2)
    raise Exception("❌ Could not connect to MongoDB after retries")

client = get_mongo_client(mongo_uri)
db = client[mongo_dbname]
collection = db["messages"]

# --- Routes CRUD ---

@app.route("/api/messages", methods=["GET"])
def get_messages():
    messages = list(collection.find({}, {"_id": 0}))
    return jsonify(messages)

@app.route("/api/message/<string:msg>", methods=["GET"])
def get_message(msg):
    data = collection.find_one({"message": msg}, {"_id": 0})
    if not data:
        return jsonify({"error": "Message not found"}), 404
    return jsonify(data)

@app.route("/api/message", methods=["POST"])
def add_message():
    content = request.json
    print("Incoming JSON:", content)    
    message = content.get("message")
    if not message:
        return jsonify({"error": "Missing 'message' field"}), 400
    try:
        collection.insert_one({"message": message})
        return jsonify({"status": "message added"}), 201
    except Exception as e:
        print("❌ Failed to insert message:", e)  # <-- affichera l'erreur dans les logs
        return jsonify({"error": str(e)}), 500

@app.route("/api/message/<string:old_msg>", methods=["PUT"])
def update_message(old_msg):
    try:
        content = request.json
        new_msg = content.get("message")
        if not new_msg:
            return jsonify({"error": "Missing 'message' field"}), 400
        result = collection.update_one({"message": old_msg}, {"$set": {"message": new_msg}})
        if result.matched_count == 0:
            return jsonify({"error": "Message not found"}), 404
        return jsonify({"status": "message updated"})
    except PyMongoError as e:
        print("MongoDB error:", e)
        return jsonify({"error": "Database error"}), 500

@app.route("/api/message/<string:msg>", methods=["DELETE"])
def delete_message(msg):
    try:
        result = collection.delete_one({"message": msg})
        if result.deleted_count == 0:
            return jsonify({"error": "Message not found"}), 404
        return jsonify({"status": "message deleted"})
    except PyMongoError as e:
        print("MongoDB error:", e)
        return jsonify({"error": "Database error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)