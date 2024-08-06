from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
import bcrypt
from dotenv import load_dotenv
import os
from bson import ObjectId

load_dotenv()

app = Flask(__name__)
CORS(app)

# Connecting to MongoDB
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)

## API endpoint to allow user signup
@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    # Hashing the password before storing it
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Check if user already exists
    user = mongo.db.users.find_one({"username": username})
    if user:
        return jsonify({"message": "User already exists"}), 400

    # Create a new user in the database
    mongo.db.users.insert_one({
        "username": username,
        "password": hashed_password
    })
    return jsonify({"message": "User created successfully"}), 201

## API endpoint to allow user signup
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    # If user does not supply username or password
    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    user = mongo.db.users.find_one({"username": username})

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid username/password"}), 401

## API to retrieve conversations for a user
@app.route('/api/conversations', methods=['GET'])
def get_conversations():
    username = request.args.get('username')
    if not username:
        return jsonify({"message": "Username is required"}), 400

    conversations = list(mongo.db.conversations.find({"username": username}, {"messages": 0}))
    for conversation in conversations:
        conversation["_id"] = str(conversation["_id"])
    return jsonify(conversations)

## API To create a new conversation for a user
@app.route('/api/conversation', methods=['POST'])
def create_conversation():
    data = request.json
    username = data.get('username')
    if not username:
        return jsonify({"message": "Username is required"}), 400

    conversation_id = mongo.db.conversations.insert_one({
        "username": username,
        "messages": []
    }).inserted_id
    return jsonify({"conversation_id": str(conversation_id)})


## API to delete the conversation thread
@app.route('/api/conversation/<conversation_id>', methods=['DELETE'])
def delete_conversation(conversation_id):
    result = mongo.db.conversations.delete_one({"_id": ObjectId(conversation_id)})
    if result.deleted_count == 0:
        return jsonify({"message": "Conversation not found"}), 404
    return jsonify({"message": "Conversation deleted"}), 200


### API to retrieve messages for a specific conversation
@app.route('/api/messages', methods=['GET'])
def get_messages():
    conversation_id = request.args.get('conversation_id')
    if not conversation_id:
        return jsonify({"message": "Conversation ID is required"}), 400

    conversation = mongo.db.conversations.find_one({"_id": ObjectId(conversation_id)})
    if not conversation:
        return jsonify({"message": "Conversation not found"}), 404

    return jsonify(conversation['messages'])

## API to add messages to specific conversations
@app.route('/api/messages', methods=['POST'])
def add_message():
    data = request.json
    conversation_id = data.get('conversation_id')
    user_message = data.get('message', '')

    if not conversation_id or not user_message:
        return jsonify({"message": "Conversation ID and message are required"}), 400

    # Simulate a bot response
    bot_response = f"Bot response to: {user_message}"

    mongo.db.conversations.update_one(
        {"_id": ObjectId(conversation_id)},
        {"$push": {"messages": {"text": user_message, "user": "user"}}}
    )
    mongo.db.conversations.update_one(
        {"_id": ObjectId(conversation_id)},
        {"$push": {"messages": {"text": bot_response, "user": "bot"}}}
    )

    return jsonify({'text': bot_response, 'user': 'bot'})

if __name__ == '__main__':
    app.run(debug=True)
