from flask import Flask, jsonify, request
from flask_cors import CORS
from db_manager import F1DatabaseManager
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Database configuration
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
    try:
        db = F1DatabaseManager(db_config)
        db.connect()
        
        db.cursor.execute("SELECT * FROM sessions ORDER BY date DESC")
        sessions = db.cursor.fetchall()
        
        db.close()
        
        return jsonify({'sessions': [dict(s) for s in sessions]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/drivers', methods=['GET'])
def get_drivers():
    """Get all drivers"""
    try:
        db = F1DatabaseManager(db_config)
        db.connect()
        
        db.cursor.execute("SELECT * FROM drivers ORDER BY driver_code")
        drivers = db.cursor.fetchall()
        
        db.close()
        
        return jsonify({'drivers': [dict(d) for d in drivers]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/laps/<session_id>', methods=['GET'])
def get_laps(session_id):
    """Get laps for a session"""
    driver_code = request.args.get('driver')
    
    try:
        db = F1DatabaseManager(db_config)
        db.connect()
        
        if driver_code:
            query = "SELECT * FROM laps WHERE session_id = %s AND driver_code = %s ORDER BY lap_number"
            db.cursor.execute(query, (session_id, driver_code))
        else:
            query = "SELECT * FROM laps WHERE session_id = %s ORDER BY lap_number"
            db.cursor.execute(query, (session_id,))
        
        laps = db.cursor.fetchall()
        db.close()
        
        return jsonify({'laps': [dict(l) for l in laps]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/telemetry/<lap_id>', methods=['GET'])
def get_telemetry(lap_id):
    """Get telemetry for a specific lap"""
    try:
        db = F1DatabaseManager(db_config)
        db.connect()
        
        query = "SELECT * FROM telemetry WHERE lap_id = %s ORDER BY distance"
        db.cursor.execute(query, (lap_id,))
        telemetry = db.cursor.fetchall()
        
        db.close()
        
        return jsonify({'telemetry': [dict(t) for t in telemetry]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/compare', methods=['POST'])
def compare_drivers():
    """Compare two drivers' lap times"""
    data = request.json
    driver1 = data.get('driver1')
    driver2 = data.get('driver2')
    session_id = data.get('session_id')
    
    try:
        db = F1DatabaseManager(db_config)
        db.connect()
        
        # Get driver1 laps
        query1 = "SELECT lap_number, lap_time_seconds FROM laps WHERE session_id = %s AND driver_code = %s ORDER BY lap_number"
        db.cursor.execute(query1, (session_id, driver1))
        driver1_laps = {row[0]: row[1] for row in db.cursor.fetchall()}
        
        # Get driver2 laps
        db.cursor.execute(query1, (session_id, driver2))
        driver2_laps = {row[0]: row[1] for row in db.cursor.fetchall()}
        
        db.close()
        
        # Combine for chart
        comparison = []
        all_laps = set(driver1_laps.keys()) | set(driver2_laps.keys())
        for lap in sorted(all_laps):
            comparison.append({
                'lap': lap,
                'driver1Time': driver1_laps.get(lap),
                'driver2Time': driver2_laps.get(lap)
            })
        
        return jsonify({
            'driver1': driver1,
            'driver2': driver2,
            'comparison': comparison
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🏎️  Starting F1 Telemetry API...")
    app.run(debug=True, port=5000)

