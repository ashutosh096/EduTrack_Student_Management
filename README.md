<<<<<<< HEAD
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
=======
System Description: EduTrack Student Management

EduTrack is a high-performance, full-stack student management system designed for educational institutions to track academic progress and daily operations. It features a modern, responsive dashboard built with FastAPI on the backend and a dynamic Chart.js frontend. 


Academic Monitoring: Automatically tracks student GPA trends over multiple terms and visualizes class-wide performance. 


Daily Operations: Includes a dedicated Attendance module that allows teachers to log daily presence and visualize real-time attendance rates. 


Data Integrity: Built on a robust SQLite database with automated schema creation, ensuring that student IDs are unique and records are protected via foreign key constraints. 

User Experience: The interface is optimized for "Premium" professional use, featuring smooth CSS animations, a sidebar-driven navigation, and a "search-as-you-type" filtering system.

README.md
2. Launch the Application
Run the FastAPI server using Uvicorn:

3. Access the Dashboard
Open your browser and visit:
👉 http://localhost:8000

🛠 Key Features

Interactive Dashboard: Real-time stats for total students, average GPA, and today's attendance rate. 


Student CRUD: Full capability to add, edit, search, and delete student profiles. 


Attendance Tracking: A dedicated interface to log and save daily attendance with instant "Present/Absent" counts. 

Visual Analytics: * Grade Trends: Line charts showing GPA progress.

Demographics: Bar charts for student distribution by grade and subject.


Automated Database: Uses SQLite; the database (edutrack.db) and sample data are auto-generated on the first run.
![image alt](https://github.com/ashutosh096/EduTrack_Student_Management/blob/2fcf2c897c4d89002f7f10483cc1b6849786c119/Screenshot%202026-03-30%20223521.png)
![image alt](https://github.com/ashutosh096/EduTrack_Student_Management/blob/12727ddc2634b4067d89970e493c32d8a29d7c46/Screenshot%202026-03-30%20223559.png)
>>>>>>> 776cf44f3368713541a2bbf0036eda2a865392f9
