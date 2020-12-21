import os

import psycopg2
from flask import Flask, jsonify, send_from_directory

app = Flask(__name__, static_folder='../../frontend/build')

dbname = 'vibe-check'
user = 'postgres'
conn = psycopg2.connect(f"dbname={dbname} user={user}")
cursor = conn.cursor()

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.route('/')
def index():
    cursor.execute("SELECT * FROM song;")
    return jsonify(cursor.fetchall())

if __name__ == '__main__':
    app.run(debug=True)
