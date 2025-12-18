"""
SQLite Database connection utilities
Handles F1 telemetry data storage
"""

import sqlite3

class F1DatabaseManager:
    def __init__(self, db_path='f1_telemetry.db'):
        """Initialize database connection"""
        self.db_path = db_path
        self.conn =None
        self.cursor = None
    
    def connect(self):
        """Connect to SQLite database"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row  # Return rows as dictionaries
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
