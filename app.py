from flask import Flask, jsonify, request
from flask_cors import CORS
from db_manager import F1DatabaseManager
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# SQLite database
db = F1DatabaseManager('f1_telemetry.db')

@app.route('/api/health', methods=['GET'])
def health_check():
    """API health check"""
    return jsonify({'status': 'healthy', 'message': 'F1 Telemetry API is running'}), 200

@app.route('/api/sessions', methods=['GET'])
def get_sessions():
    """Get all race sessions"""
    try:
        db.connect()
        
        db.cursor.execute("SELECT * FROM sessions ORDER BY date DESC")
        sessions = [dict(row) for row in db.cursor.fetchall()]
        
        db.close()
        
        return jsonify({'sessions': sessions}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/drivers', methods=['GET'])
def get_drivers():
    """Get all drivers"""
    try:
        db.connect()
        
        db.cursor.execute("SELECT * FROM drivers ORDER BY driver_code")
        drivers = [dict(row) for row in db.cursor.fetchall()]
        
        db.close()
        
        return jsonify({'drivers': drivers}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/compare', methods=['POST'])
def compare_drivers():
    """Compare two drivers' lap times"""
    try:
        data = request.get_json()
        driver1 = data.get('driver1')
        driver2 = data.get('driver2')
        session_id = data.get('session_id')
        
        if not all([driver1, driver2, session_id]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        db.connect()
        
        # Get driver 1 laps
        db.cursor.execute(
            "SELECT lap_number, lap_time FROM laps WHERE session_id = ? AND driver_code = ? ORDER BY lap_number",
            (session_id, driver1)
        )
        driver1_laps = {row['lap_number']: row['lap_time'] for row in db.cursor.fetchall()}
        
        # Get driver 2 laps
        db.cursor.execute(
            "SELECT lap_number, lap_time FROM laps WHERE session_id = ? AND driver_code = ? ORDER BY lap_number",
            (session_id, driver2)
        )
        driver2_laps = {row['lap_number']: row['lap_time'] for row in db.cursor.fetchall()}
        
        db.close()
        
        # Combine data for chart
        comparison = []
        all_laps = sorted(set(driver1_laps.keys()) | set(driver2_laps.keys()))
        
        for lap in all_laps:
            comparison.append({
                'lap': lap,
                'driver1Time': driver1_laps.get(lap),
                'driver2Time': driver2_laps.get(lap)
            })
        
        return jsonify({'comparison': comparison}), 200
        
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


@app.route('/api/tire-analysis/<session_id>/<driver_code>', methods=['GET'])
def analyze_tire(session_id, driver_code):
    """Analyze tire degradation for a driver in a session"""
    try:
        from tire_analysis import analyze_tire_degradation, tire_analysis_to_json
        
        db = F1DatabaseManager(db_config)
        db.connect()
        
        # Get lap times for this driver
        query = """
            SELECT lap_number, lap_time_seconds, compound 
            FROM laps 
            WHERE session_id = %s AND driver_code = %s 
            ORDER BY lap_number
        """
        db.cursor.execute(query, (session_id, driver_code))
        laps = db.cursor.fetchall()
        db.close()
        
        if not laps:
            return jsonify({'error': 'No lap data found'}), 404
        
        # Group by stint (based on compound changes and gaps)
        stints = []
        current_stint = {'compound': None, 'laps': []}
        
        for lap in laps:
            lap_num, lap_time, compound = lap[0], lap[1], lap[2] or 'UNKNOWN'
            
            if lap_time is None or lap_time < 60:  # Skip invalid laps
                continue
                
            if current_stint['compound'] != compound:
                if current_stint['laps']:
                    stints.append(current_stint)
                current_stint = {'compound': compound, 'laps': [lap_time]}
            else:
                current_stint['laps'].append(lap_time)
        
        if current_stint['laps']:
            stints.append(current_stint)
        
        # Analyze each stint
        analyses = []
        for stint in stints:
            analysis = analyze_tire_degradation(stint['laps'], stint['compound'])
            analyses.append(tire_analysis_to_json(analysis))
        
        return jsonify({
            'driver': driver_code,
            'session_id': session_id,
            'stints': analyses,
            'total_stints': len(analyses)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/pit-strategy/<session_id>/<driver_code>', methods=['GET'])
def get_pit_strategy(session_id, driver_code):
    """Calculate optimal pit window for a driver"""
    try:
        from tire_analysis import calculate_optimal_pit_window, analyze_tire_degradation
        
        total_laps = int(request.args.get('total_laps', 57))  # Default Monaco laps
        current_lap = int(request.args.get('current_lap', 1))
        
        db = F1DatabaseManager(db_config)
        db.connect()
        
        query = """
            SELECT lap_number, lap_time_seconds 
            FROM laps 
            WHERE session_id = %s AND driver_code = %s 
            ORDER BY lap_number
        """
        db.cursor.execute(query, (session_id, driver_code))
        laps = db.cursor.fetchall()
        db.close()
        
        if not laps:
            return jsonify({'error': 'No lap data found'}), 404
        
        lap_times = [l[1] for l in laps if l[1] and l[1] > 60]
        current_tire_age = len(lap_times)
        
        analysis = analyze_tire_degradation(lap_times)
        deg_rate = analysis.degradation_rate
        
        earliest, latest, recommendation = calculate_optimal_pit_window(
            current_lap, total_laps, current_tire_age, deg_rate
        )
        
        return jsonify({
            'driver': driver_code,
            'current_lap': current_lap,
            'current_tire_age': current_tire_age,
            'degradation_rate': deg_rate,
            'pit_window': {
                'earliest': earliest,
                'latest': latest
            },
            'recommendation': recommendation
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🏎️  Starting F1 Telemetry API...")
    app.run(debug=True, port=5000)

