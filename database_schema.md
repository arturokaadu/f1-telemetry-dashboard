"""
Database schema for F1 Telemetry data
PostgreSQL tables for laps, telemetry, and race sessions
"""

# Database Schema Design

## Tables:

### 1. sessions
- session_id (PRIMARY KEY, UUID)
- year (INTEGER)
- event_name (VARCHAR) - e.g., "Monaco"
- session_type (VARCHAR) - "R" (Race), "Q" (Qualifying), "FP1/2/3"
- date (DATE)
- created_at (TIMESTAMP)

### 2. laps
- lap_id (PRIMARY KEY, UUID)
- session_id (FOREIGN KEY → sessions)
- driver_code (VARCHAR) - e.g., "VER", "HAM"
- lap_number (INTEGER)
- lap_time_seconds (FLOAT)
- tire_compound (VARCHAR) - "SOFT", "MEDIUM", "HARD"
- tire_life (INTEGER) - laps on this tire
- is_personal_best (BOOLEAN)
- sector1_time (FLOAT)
- sector2_time (FLOAT)
- sector3_time (FLOAT)
- created_at (TIMESTAMP)

### 3. telemetry
- telemetry_id (PRIMARY KEY, UUID)
- lap_id (FOREIGN KEY → laps)
- distance (FLOAT) - meters along track
- speed (INTEGER) - km/h
- throttle (INTEGER) - 0-100%
- brake (BOOLEAN)
- drs (INTEGER) - 0 (off), 1-14 (on)
- gear (INTEGER) - 1-8
- rpm (INTEGER)
- position_x (FLOAT)
- position_y (FLOAT)
- created_at (TIMESTAMP)

### 4. drivers
- driver_id (PRIMARY KEY, UUID)
- driver_code (VARCHAR UNIQUE) - "VER"
- full_name (VARCHAR) - "Max Verstappen"
- team (VARCHAR) - "Red Bull Racing"
- number (INTEGER) - 1

## Indexes:
- sessions: (year, event_name, session_type)
- laps: (session_id, driver_code, lap_number)
- telemetry: (lap_id, distance)

## SQL Creation Script:

```sql
CREATE TABLE sessions (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    year INTEGER NOT NULL,
    event_name VARCHAR(100) NOT NULL,
    session_type VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE drivers (
    driver_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    driver_code VARCHAR(3) UNIQUE NOT NULL,
    full_name VARCHAR(100),
    team VARCHAR(100),
    number INTEGER
);

CREATE TABLE laps (
    lap_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES sessions(session_id),
    driver_code VARCHAR(3) REFERENCES drivers(driver_code),
    lap_number INTEGER NOT NULL,
    lap_time_seconds FLOAT,
    tire_compound VARCHAR(10),
    tire_life INTEGER,
    is_personal_best BOOLEAN DEFAULT FALSE,
    sector1_time FLOAT,
    sector2_time FLOAT,
    sector3_time FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE telemetry (
    telemetry_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lap_id UUID REFERENCES laps(lap_id),
    distance FLOAT NOT NULL,
    speed INTEGER,
    throttle INTEGER,
    brake BOOLEAN,
    drs INTEGER,
    gear INTEGER,
    rpm INTEGER,
    position_x FLOAT,
    position_y FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sessions_lookup ON sessions(year, event_name, session_type);
CREATE INDEX idx_laps_lookup ON laps(session_id, driver_code, lap_number);
CREATE INDEX idx_telemetry_lookup ON telemetry(lap_id, distance);
```

## Data Flow:
1. FastF1 fetches race data
2. Python script processes and structures data
3. Insert into PostgreSQL via psycopg2
4. Flask API queries for dashboard
5. React frontend displays visualizations
