import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

dbname = 'vibe-check'
user = 'postgres'
conn = psycopg2.connect(f"dbname={dbname} user={user}")
cursor = conn.cursor()

@app.route('/')
def index():
    cursor.execute("SELECT * FROM song;")
    return jsonify(cursor.fetchall())

if __name__ == '__main__':
    app.run(debug=True)
