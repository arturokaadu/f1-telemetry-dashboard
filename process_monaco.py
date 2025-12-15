"""
Process Monaco 2024 data and insert into PostgreSQL database
Run this after setting up PostgreSQL locally
"""

import fastf1
from pathlib import Path
from db_manager import F1DatabaseManager
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Enable cache
cache_dir = Path(__file__).parent / 'cache'
cache_dir.mkdir(exist_ok=True)
fastf1.Cache.enable_cache(str(cache_dir))

# Database config
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'f1_telemetry'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD')
}

def process_monaco_2024():
    """Fetch Monaco 2024 and insert into database"""
    print("Loading Monaco 2024 session...")
    session = fastf1.get_session(2024, 'Monaco', 'R')
    session.load()
    
    print(f"Session: {session.event['EventName']} - {session.name}")
    
    # Connect to database
    db = F1DatabaseManager(db_config)
    db.connect()
    
    # Insert session
    session_id = db.insert_session(
        year=2024,
        event_name='Monaco',
        session_type='R',
        date=datetime(2024, 5, 26)
    )
    print(f"Session inserted: {session_id}")
    
    # Get unique drivers
    drivers = session.laps['Driver'].unique()
    print(f"Processing {len(drivers)} drivers...")
    
    for driver_code in drivers:
        # Insert driver
        driver_laps = session.laps.pick_driver(driver_code)
        if len(driver_laps) > 0:
            first_lap = driver_laps.iloc[0]
            db.insert_driver(
                driver_code=driver_code,
                full_name=str(driver_code),  # Would need driver info API
                team=first_lap['Team'] if 'Team' in first_lap else 'Unknown',
                number=first_lap['DriverNumber'] if 'DriverNumber' in first_lap else 0
            )
    
    print("Drivers inserted")
    
    # Insert laps
    laps_data = []
    for idx, lap in session.laps.iterrows():
        lap_time = lap['LapTime'].total_seconds() if pd.notna(lap['LapTime']) else None
        
        laps_data.append((
            session_id,
            lap['Driver'],
            int(lap['LapNumber']),
            lap_time,
            lap['Compound'] if 'Compound' in lap else None,
            int(lap['TyreLife']) if 'TyreLife' in lap and pd.notna(lap['TyreLife']) else 0,
            bool(lap['IsPersonalBest']) if 'IsPersonalBest' in lap else False,
            None,  # sector times would need parsing
            None,
            None
        ))
    
    db.insert_laps_batch(laps_data)
    print(f"Inserted {len(laps_data)} laps")
    
    db.close()
    print("✅ Monaco 2024 data processing complete")

if __name__ == "__main__":
    import pandas as pd
    process_monaco_2024()
