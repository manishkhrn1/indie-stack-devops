from flask import request
from flask import Flask, jsonify
import psycopg2
import os
import time


app = Flask(__name__)

def get_db_connection():
    # This pulls the URL we defined in our docker-compose.yml
    db_url = os.environ.get('DATABASE_URL')
    conn = None
    # Retry logic: Databases take a few seconds to start up!
    for i in range(5):
        try:
            conn = psycopg2.connect(db_url)
            return conn
        except Exception as e:
            print(f"Database not ready yet... (Attempt {i+1}/5)")
            time.sleep(2)
    return None

@app.route('/health', methods=['GET'])
def health_check():
    conn = get_db_connection()
    db_status = "Connected" if conn else "Disconnected"
    if conn: conn.close()
    
    return jsonify({
        "status": "online",
        "service": "IndieStack-Backend",
        "database_connected": db_status
    }), 200

@app.route('/update_stats', methods=['POST'])
def update_stats():
    data = request.json
    name = data.get('player_name')
    score = data.get('score')
    level = data.get('level')

    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO player_stats (player_name, score, level) VALUES (%s, %s, %s)",
            (name, score, level)
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Stats updated!"}), 201
    return jsonify({"error": "Database connection failed"}), 500

def init_db():
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        # Create a simple table for player scores
        cur.execute('''
            CREATE TABLE IF NOT EXISTS player_stats (
                id SERIAL PRIMARY KEY,
                player_name VARCHAR(50) NOT NULL,
                score INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        conn.commit()
        cur.close()
        conn.close()
        print("Database initialized!")

# Call it before starting the app
if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)