from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Sample data to mimic a database
data = []

# Route to serve index.html
@app.route('/')
def index():
    return render_template('index.html')

# Route to get all items
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(data)

# Route to create a new item
@app.route('/items', methods=['POST'])
def create_item():
    new_item = request.json
    data.append(new_item)
    return jsonify(new_item), 201

# Route to get a specific item by its ID
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    for item in data:
        if item['id'] == item_id:
            return jsonify(item)
    return jsonify({'error': 'Item not found'}), 404

# Route to update a specific item by its ID
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    for item in data:
        if item['id'] == item_id:
            item.update(request.json)
            return jsonify(item)
    return jsonify({'error': 'Item not found'}), 404

# Route to delete a specific item by its ID
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    for item in data:
        if item['id'] == item_id:
            data.remove(item)
            return jsonify({'message': 'Item deleted successfully'})
    return jsonify({'error': 'Item not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
