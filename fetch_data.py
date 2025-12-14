"""
F1 Telemetry Data Fetcher
Fetches Monaco 2024 Grand Prix telemetry data using FastF1
"""

import fastf1
import pandas as pd
from pathlib import Path

# Enable FastF1 cache
cache_dir = Path(__file__).parent / 'cache'
cache_dir.mkdir(exist_ok=True)
fastf1.Cache.enable_cache(str(cache_dir))

def fetch_monaco_2024():
    """Fetch Monaco 2024 Grand Prix session data"""
    print("Loading Monaco 2024 race session...")
    
    # Load Monaco 2024 Race
    session = fastf1.get_session(2024, 'Monaco', 'R')
    session.load()
    
    print(f"Session loaded: {session.event['EventName']} - {session.name}")
    print(f"Drivers in session: {len(session.drivers)}")
    
    # Get all laps
    laps = session.laps
    print(f"Total laps: {len(laps)}")
    
    # Sample data structure
    print("\nSample lap data:")
    print(laps[['Driver', 'LapNumber', 'LapTime', 'Compound', 'TyreLife']].head(10))
    
    return session, laps

def get_driver_telemetry(session, driver_code, lap_number):
    """Get detailed telemetry for specific driver and lap"""
    lap = session.laps.pick_driver(driver_code).pick_lap(lap_number)
    telemetry = lap.get_telemetry()
    
    print(f"\nTelemetry for {driver_code} - Lap {lap_number}:")
    print(f"Data points: {len(telemetry)}")
    print(f"Columns: {telemetry.columns.tolist()}")
    
    return telemetry

if __name__ == "__main__":
    # Test fetch
    session, laps = fetch_monaco_2024()
    
    # Get sample telemetry (Verstappen lap 1)
    telemetry = get_driver_telemetry(session, 'VER', 1)
    
    print("\nData fetch complete! ✅")
