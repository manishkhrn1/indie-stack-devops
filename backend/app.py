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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)