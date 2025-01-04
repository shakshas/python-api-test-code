from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory "database" for demonstration
items = [
    {"id": 1, "name": "Item 1", "description": "Description for Item 1"},
    {"id": 2, "name": "Item 2", "description": "Description for Item 2"},
]

# GET all items
@app.route("/items", methods=["GET"])
def get_items():
    return jsonify(items), 200

# GET a single item by ID
@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = next((item for item in items if item["id"] == item_id), None)
    if item:
        return jsonify(item), 200
    return jsonify({"error": "Item not found"}), 404

# POST: Create a new item
@app.route("/items", methods=["POST"])
def create_item():
    data = request.get_json()
    if not data or not data.get("name"):
        return jsonify({"error": "Name is required"}), 400

    new_item = {
        "id": items[-1]["id"] + 1 if items else 1,
        "name": data["name"],
        "description": data.get("description", ""),
    }
    items.append(new_item)
    return jsonify(new_item), 201

# PUT: Update an existing item
@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    item = next((item for item in items if item["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    data = request.get_json()
    item["name"] = data.get("name", item["name"])
    item["description"] = data.get("description", item["description"])
    return jsonify(item), 200

# DELETE: Remove an item
@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    global items
    item = next((item for item in items if item["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    items = [item for item in items if item["id"] != item_id]
    return jsonify({"message": "Item deleted"}), 200

# Health Check
@app.route("/", methods=["GET"])
def hello_world():
    return jsonify({"message": "Hello, World!"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
