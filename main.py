import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def init_db():
    with sqlite3.connect('data.db') as conn:
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS items (name TEXT)')
        conn.commit()

@app.route('/add', methods=['POST'])
def add_item():
    item = request.json.get('name')
    with sqlite3.connect('data.db') as conn:
        c = conn.cursor()
        c.execute('INSERT INTO items (name) VALUES (?)', (item,))
        conn.commit()
    return jsonify({"message": "Item added"}), 201

@app.route('/list', methods=['GET'])
def list_items():
    with sqlite3.connect('data.db') as conn:
        c = conn.cursor()
        c.execute('SELECT name FROM items')
        items = c.fetchall()
    return jsonify({"items": [item[0] for item in items]}), 200

@app.route('/')
def home():
    return "Welcome to the Flask App!"


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0')
