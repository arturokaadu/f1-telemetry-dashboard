"""
Database connection and data insertion utilities
Handles PostgreSQL connection and F1 data storage
"""

import psycopg2
from psycopg2.extras import execute_values
import uuid
from datetime import datetime

class F1DatabaseManager:
    def __init__(self, db_config):
        """Initialize database connection"""
        self.db_config = db_config
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """Connect to PostgreSQL database"""
        try:
            self.conn = psycopg2.connect(**self.db_config)
            self.cursor = self.conn.cursor()
            print("✅ Database connected successfully")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            raise
    
    def close(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("Database connection closed")
    
    def insert_session(self, year, event_name, session_type, date):
        """Insert race session"""
        session_id = str(uuid.uuid4())
        query = """
            INSERT INTO sessions (session_id, year, event_name, session_type, date)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING session_id
        """
        self.cursor.execute(query, (session_id, year, event_name, session_type, date))
        self.conn.commit()
        return session_id
    
    def insert_driver(self, driver_code, full_name, team, number):
        """Insert driver if not exists"""
        query = """
            INSERT INTO drivers (driver_code, full_name, team, number)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (driver_code) DO NOTHING
        """
        self.cursor.execute(query, (driver_code, full_name, team, number))
        self.conn.commit()
    
    def insert_laps_batch(self, laps_data):
        """Batch insert laps"""
        query = """
            INSERT INTO laps (session_id, driver_code, lap_number, lap_time_seconds,
                            tire_compound, tire_life, is_personal_best,
                            sector1_time, sector2_time, sector3_time)
            VALUES %s
        """
        execute_values(self.cursor, query, laps_data)
        self.conn.commit()
        print(f"✅ Inserted {len(laps_data)} laps")
    
    def insert_telemetry_batch(self, telemetry_data):
        """Batch insert telemetry"""
        query = """
            INSERT INTO telemetry (lap_id, distance, speed, throttle, brake,
                                 drs, gear, rpm, position_x, position_y)
            VALUES %s
        """
        execute_values(self.cursor, query, telemetry_data)
        self.conn.commit()
        print(f"✅ Inserted {len(telemetry_data)} telemetry points")

# Example usage (will be called from main script)
if __name__ == "__main__":
    # Database config (will use environment variables in production)
    db_config = {
        'host': 'localhost',
        'database': 'f1_telemetry',
        'user': 'postgres',
        'password': 'your_password'
    }
    
    db = F1DatabaseManager(db_config)
    db.connect()
    
    # Test session insert
    session_id = db.insert_session(2024, 'Monaco', 'R', datetime(2024, 5, 26))
    print(f"Session ID: {session_id}")
    
    db.close()
