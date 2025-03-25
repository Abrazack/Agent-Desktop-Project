
from flask import Flask, jsonify, request
import json
import hashlib
import os

app = Flask(__name__)

# File paths
USER_FILE = "users.json"
LOG_FILE = "log.txt"
INVENTORY_FILE = "inventory.json"

def load_users():
    if not os.path.exists(USER_FILE):
        return {"admin": {"password": hash_password("admin123"), "role": "admin"}}
    with open(USER_FILE, "r") as f:
        return json.load(f)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')
    
    users = load_users()
    user = users.get(username)
    
    if user and user['password'] == hash_password(password) and user['role'] == role:
        return jsonify({"success": True, "user": {"username": username, "role": role}})
    return jsonify({"success": False, "message": "Invalid credentials"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
