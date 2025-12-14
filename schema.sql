-- F1 Telemetry Database Schema
-- PostgreSQL 14+

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
