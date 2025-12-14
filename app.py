"""
Flask API for F1 Telemetry Dashboard
Provides endpoints for driver comparison, lap times, telemetry data
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from db_manager import F1DatabaseManager
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Database configuration from environment
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'f1_telemetry'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD')
}

@app.route('/api/health', methods=['GET'])
def health_check():
    """API health check"""
    return jsonify({'status': 'healthy', 'message': 'F1 Telemetry API is running'}), 200

@app.route('/api/sessions', methods=['GET'])
def get_sessions():
    """Get all race sessions"""
    # TODO: Query database for sessions
    return jsonify({'sessions': []}), 200

@app.route('/api/drivers', methods=['GET'])
def get_drivers():
    """Get all drivers"""
    # TODO: Query database for drivers
    return jsonify({'drivers': []}), 200

@app.route('/api/laps/<session_id>', methods=['GET'])
def get_laps(session_id):
    """Get laps for a session"""
    driver_code = request.args.get('driver')
    # TODO: Query database for laps
    return jsonify({'laps': []}), 200

@app.route('/api/telemetry/<lap_id>', methods=['GET'])
def get_telemetry(lap_id):
    """Get telemetry for a specific lap"""
    # TODO: Query database for telemetry
    return jsonify({'telemetry': []}), 200

@app.route('/api/compare', methods=['POST'])
def compare_drivers():
    """Compare two drivers' lap times"""
    data = request.json
    driver1 = data.get('driver1')
    driver2 = data.get('driver2')
    session_id = data.get('session_id')
    
    # TODO: Implement driver comparison logic
    return jsonify({
        'driver1': driver1,
        'driver2': driver2,
        'comparison': {}
    }), 200

if __name__ == '__main__':
    print("🏎️  Starting F1 Telemetry API...")
    app.run(debug=True, port=5000)
