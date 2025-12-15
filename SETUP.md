# F1 Telemetry Dashboard - Setup Instructions

## What You Need

1. PostgreSQL installed locally
2. Python 3.9+
3. Node.js 16+

## Setup Steps

### 1. Database Setup

```bash
# Install PostgreSQL (if not installed)
# Windows: Download from postgresql.org

# Create database
psql -U postgres
CREATE DATABASE f1_telemetry;
\q

# Run schema
psql -U postgres -d f1_telemetry -f schema.sql
```

### 2. Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your PostgreSQL password

# Process Monaco data into database
python process_monaco.py

# Start Flask API
python app.py
```

API will run on http://localhost:5000

### 3. Frontend Setup

```bash
cd frontend
npm install
npm start
```

Dashboard will open on http://localhost:3000

## Test the App

1. Backend running: Visit http://localhost:5000/api/health
2. Frontend running: Open http://localhost:3000
3. Select two drivers (VER vs HAM)
4. View lap time comparison chart

## What Works

- Monaco 2024 data (18,879 telemetry points)
- Flask API with all endpoints
- React dashboard with driver comparison
- Database schema designed

## What's Left

- Connect frontend to backend (API call integration)
- Test with real data
- Deploy to Vercel

---

Built autonomously by Luna
