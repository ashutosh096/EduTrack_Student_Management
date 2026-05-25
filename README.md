# EduTrack — Student Dashboard
### FastAPI + SQLite + Chart.js

## Setup (3 steps)

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the server
```bash
uvicorn main:app --reload --port 8000
```

### 3. Open the dashboard
Visit → http://localhost:8000

---

## Project Structure
```
edutrack/
├── main.py            ← FastAPI backend (all routes)
├── requirements.txt   ← Python deps
├── schema.sql         ← Reference schema (auto-created by Python)
├── edutrack.db        ← SQLite database (auto-created on first run)
└── static/
    └── index.html     ← Full frontend dashboard
```

## API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| GET | /api/stats | Dashboard summary stats |
| GET | /api/students | List students (search, filter) |
| GET | /api/students/{id} | Get single student |
| POST | /api/students | Create student |
| PUT | /api/students/{id} | Update student |
| DELETE | /api/students/{id} | Delete student |
| GET | /api/attendance?date=YYYY-MM-DD | Get attendance for a date |
| POST | /api/attendance | Save attendance records |
| GET | /api/grade-history | Class-wide GPA trend |
| GET | /api/grade-history?student_id={id} | Per-student GPA trend |

## API Docs
Visit → http://localhost:8000/docs (FastAPI auto-generated Swagger UI)

## Notes
- Database is SQLite — no MySQL setup needed
- Sample data (10 students) is auto-seeded on first run
- Frontend talks to API on localhost:8000
- CORS is open for development — restrict in production
