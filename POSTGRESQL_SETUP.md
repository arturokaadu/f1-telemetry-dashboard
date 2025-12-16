# PostgreSQL Setup - Quick Guide
# For F1 Dashboard Database

## Install PostgreSQL

**Download:** https://www.postgresql.org/download/windows/

**During install:**
- Set password (remember it!)
- Port: 5432 (default)
- Locale: Spanish (Argentina) or default

## Setup Database

```powershell
# Open psql (PostgreSQL CLI)
# Start → pgAdmin 4 → Tools → Query Tool

# Or command line:
psql -U postgres

# Create database
CREATE DATABASE f1_telemetry;

# Connect to database
\c f1_telemetry

# Run schema
\i C:/Users/artur/OneDrive/Escritorio/f1-telemetry-dashboard/schema.sql

# Verify tables created
\dt
```

## Configure Environment

```powershell
cd C:\Users\artur\OneDrive\Escritorio\f1-telemetry-dashboard

# Copy env template
copy .env.example .env

# Edit .env (notepad .env)
# Set your PostgreSQL password:
DB_PASSWORD=your_password_here
```

## Load Monaco Data

```powershell
# Install Python dependencies (if not done)
pip install -r requirements.txt

# Run data processor
python process_monaco.py
```

**Expected output:** "✅ Monaco 2024 data processing complete"

## Test API

```powershell
# Start Flask
python app.py

# Visit: http://localhost:5000/api/health
# Should see: {"status":"healthy"}
```

## Test Frontend

```powershell
cd frontend
npm install
npm start

# Opens: http://localhost:3000
# Select drivers, see lap comparison chart
```

---

**Total time:** ~20 minutes

**Next:** Deploy to Vercel cuando funcione local

💙
