from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/create', methods=['POST'])
def create_entry():
    data = request.json
    # Add your logic to handle the data
    return jsonify({"message": "Entry created successfully!"}), 201

@app.route('/get/<int:id>', methods=['GET'])
def get_entry(id):
    # Add your logic to retrieve and return data
    return jsonify({"data": f"Entry data for ID {id}"})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
