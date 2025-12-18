import sqlite3

# Create F1 Telemetry database
conn = sqlite3.connect('f1_telemetry.db')
cursor = conn.cursor()

# Create sessions table
cursor.execute('''
CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    circuit TEXT NOT NULL,
    date TEXT NOT NULL,
    session_type TEXT NOT NULL
)
''')

# Create drivers table
cursor.execute('''
CREATE TABLE IF NOT EXISTS drivers (
    driver_code TEXT PRIMARY KEY,
    full_name TEXT NOT NULL,
    team TEXT NOT NULL,
    team_color TEXT NOT NULL
)
''')

# Create laps table
cursor.execute('''
CREATE TABLE IF NOT EXISTS laps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    driver_code TEXT,
    lap_number INTEGER NOT NULL,
    lap_time REAL NOT NULL,
    sector1_time REAL,
    sector2_time REAL,
    sector3_time REAL,
    tire_compound TEXT,
    tire_age INTEGER,
    FOREIGN KEY (session_id) REFERENCES sessions(id),
    FOREIGN KEY (driver_code) REFERENCES drivers(driver_code)
)
''')

# Insert Monaco 2024 session
cursor.execute('''
INSERT OR REPLACE INTO sessions (id, name, circuit, date, session_type) 
VALUES ('monaco_2024', 'Monaco Grand Prix 2024', 'Circuit de Monaco', '2024-05-26', 'Race')
''')

# Insert drivers
drivers_data = [
    ('VER', 'Max Verstappen', 'Red Bull Racing', '#0600EF'),
    ('HAM', 'Lewis Hamilton', 'Mercedes', '#00D2BE'),
    ('LEC', 'Charles Leclerc', 'Ferrari', '#DC0000'),
    ('PER', 'Sergio Perez', 'Red Bull Racing', '#0600EF')
]

cursor.executemany('INSERT OR REPLACE INTO drivers (driver_code, full_name, team, team_color) VALUES (?, ?, ?, ?)', drivers_data)

# Insert sample lap data - Verstappen
ver_laps = [
    ('monaco_2024', 'VER', 1, 78.234, None, None, None, 'SOFT', 1),
    ('monaco_2024', 'VER', 2, 74.567, None, None, None, 'SOFT', 2),
    ('monaco_2024', 'VER', 3, 74.123, None, None, None, 'SOFT', 3),
    ('monaco_2024', 'VER', 4, 73.987, None, None, None, 'SOFT', 4),
    ('monaco_2024', 'VER', 5, 73.654, None, None, None, 'SOFT', 5),
    ('monaco_2024', 'VER', 6, 73.892, None, None, None, 'SOFT', 6),
    ('monaco_2024', 'VER', 7, 74.234, None, None, None, 'SOFT', 7),
    ('monaco_2024', 'VER', 8, 74.567, None, None, None, 'SOFT', 8),
    ('monaco_2024', 'VER', 9, 74.891, None, None, None, 'SOFT', 9),
    ('monaco_2024', 'VER', 10, 75.123, None, None, None, 'SOFT', 10),
]

# Insert sample lap data - Hamilton
ham_laps = [
    ('monaco_2024', 'HAM', 1, 78.987, None, None, None, 'SOFT', 1),
    ('monaco_2024', 'HAM', 2, 75.234, None, None, None, 'SOFT', 2),
    ('monaco_2024', 'HAM', 3, 74.876, None, None, None, 'SOFT', 3),
    ('monaco_2024', 'HAM', 4, 74.654, None, None, None, 'SOFT', 4),
    ('monaco_2024', 'HAM', 5, 74.432, None, None, None, 'SOFT', 5),
    ('monaco_2024', 'HAM', 6, 74.678, None, None, None, 'SOFT', 6),
    ('monaco_2024', 'HAM', 7, 74.923, None, None, None, 'SOFT', 7),
    ('monaco_2024', 'HAM', 8, 75.156, None, None, None, 'SOFT', 8),
    ('monaco_2024', 'HAM', 9, 75.489, None, None, None, 'SOFT', 9),
    ('monaco_2024', 'HAM', 10, 75.823, None, None, None, 'SOFT', 10),
]

all_laps = ver_laps + ham_laps
cursor.executemany('''
INSERT INTO laps (session_id, driver_code, lap_number, lap_time, sector1_time, sector2_time, sector3_time, tire_compound, tire_age) 
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', all_laps)

conn.commit()
conn.close()

print("✅ SQLite database created successfully!")
print("✅ Tables created: sessions, drivers, laps")
print("✅ Monaco 2024 data populated")
print("✅ Database file: f1_telemetry.db")
