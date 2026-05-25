"""
EduTrack — FastAPI Backend
Run: uvicorn main:app --reload --port 8000
Docs: http://localhost:8000/docs
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import date, datetime
import sqlite3
import os
import math

# ── APP SETUP ──────────────────────────────────────────────────────
app = FastAPI(title="EduTrack API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "edutrack.db"

# ── DATABASE ───────────────────────────────────────────────────────
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS students (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id  TEXT NOT NULL UNIQUE,
            name        TEXT NOT NULL,
            email       TEXT NOT NULL,
            grade       TEXT NOT NULL,
            subject     TEXT NOT NULL,
            gpa         REAL NOT NULL DEFAULT 0.0,
            status      TEXT NOT NULL DEFAULT 'Active',
            enrolled_at TEXT NOT NULL,
            created_at  TEXT DEFAULT (datetime('now')),
            updated_at  TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS attendance (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id  INTEGER NOT NULL,
            date        TEXT NOT NULL,
            present     INTEGER NOT NULL DEFAULT 1,
            UNIQUE(student_id, date),
            FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS grade_history (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id  INTEGER NOT NULL,
            period      TEXT NOT NULL,
            gpa         REAL NOT NULL,
            recorded_at TEXT NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
        );
    """)

    # Seed data only if empty
    count = cur.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    if count == 0:
        today = date.today().isoformat()
        yesterday = date.fromordinal(date.today().toordinal() - 1).isoformat()

        students = [
            ("STU-2024-001", "Aarav Sharma",  "aarav.sharma@school.in",  "11", "Science",  3.85, "Active",    "2024-06-01"),
            ("STU-2024-002", "Priya Patel",   "priya.patel@school.in",   "10", "Commerce", 3.62, "Active",    "2024-06-01"),
            ("STU-2024-003", "Rohan Verma",   "rohan.verma@school.in",   "12", "Science",  2.90, "Active",    "2023-06-01"),
            ("STU-2024-004", "Sneha Gupta",   "sneha.gupta@school.in",   "9",  "Arts",     3.45, "Active",    "2024-06-01"),
            ("STU-2024-005", "Kiran Mehta",   "kiran.mehta@school.in",   "11", "Commerce", 3.10, "Inactive",  "2024-06-01"),
            ("STU-2024-006", "Ananya Singh",  "ananya.singh@school.in",  "12", "Arts",     3.78, "Active",    "2023-06-01"),
            ("STU-2024-007", "Vikram Nair",   "vikram.nair@school.in",   "10", "Science",  2.55, "Active",    "2024-06-01"),
            ("STU-2024-008", "Deepa Reddy",   "deepa.reddy@school.in",   "9",  "Commerce", 3.92, "Active",    "2024-06-01"),
            ("STU-2024-009", "Arjun Kumar",   "arjun.kumar@school.in",   "11", "Science",  3.20, "Suspended", "2024-06-01"),
            ("STU-2024-010", "Meera Joshi",   "meera.joshi@school.in",   "12", "Arts",     3.55, "Active",    "2023-06-01"),
        ]
        cur.executemany(
            "INSERT INTO students (student_id,name,email,grade,subject,gpa,status,enrolled_at) VALUES (?,?,?,?,?,?,?,?)",
            students
        )

        # Attendance — today
        att_today = [(1,today,1),(2,today,1),(3,today,0),(4,today,1),
                     (5,today,0),(6,today,1),(7,today,1),(8,today,1),(9,today,0),(10,today,1)]
        att_yesterday = [(1,yesterday,1),(2,yesterday,1),(3,yesterday,1),(4,yesterday,0),
                         (5,yesterday,0),(6,yesterday,1),(7,yesterday,1),(8,yesterday,1),(9,yesterday,1),(10,yesterday,1)]
        cur.executemany("INSERT OR IGNORE INTO attendance (student_id,date,present) VALUES (?,?,?)",
                        att_today + att_yesterday)

        # Grade history for first 3 students
        history = [
            (1,"Term 1",3.20,"2024-09-30"),(1,"Term 2",3.45,"2024-12-31"),(1,"Term 3",3.60,"2025-03-31"),
            (1,"Term 4",3.72,"2025-06-30"),(1,"Term 5",3.80,"2025-09-30"),(1,"Term 6",3.85,"2025-12-31"),
            (2,"Term 1",3.00,"2024-09-30"),(2,"Term 2",3.20,"2024-12-31"),(2,"Term 3",3.35,"2025-03-31"),
            (2,"Term 4",3.45,"2025-06-30"),(2,"Term 5",3.55,"2025-09-30"),(2,"Term 6",3.62,"2025-12-31"),
            (3,"Term 1",2.50,"2024-09-30"),(3,"Term 2",2.60,"2024-12-31"),(3,"Term 3",2.70,"2025-03-31"),
            (3,"Term 4",2.75,"2025-06-30"),(3,"Term 5",2.85,"2025-09-30"),(3,"Term 6",2.90,"2025-12-31"),
        ]
        cur.executemany(
            "INSERT INTO grade_history (student_id,period,gpa,recorded_at) VALUES (?,?,?,?)", history
        )

    conn.commit()
    conn.close()


# Run on startup
init_db()

# Serve static frontend
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", include_in_schema=False)
def serve_frontend():
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    return {"message": "EduTrack API running. Place index.html in /static/"}


# ── PYDANTIC MODELS ────────────────────────────────────────────────
class StudentCreate(BaseModel):
    name:        str = Field(..., min_length=2)
    email:       str = Field(..., min_length=5)
    grade:       str = Field(..., pattern="^(9|10|11|12)$")
    subject:     str = Field(..., min_length=2)
    gpa:         float = Field(..., ge=0.0, le=4.0)
    status:      str = Field("Active")
    enrolled_at: str = Field(default_factory=lambda: date.today().isoformat())

class StudentUpdate(BaseModel):
    name:        str
    email:       str
    grade:       str
    subject:     str
    gpa:         float = Field(..., ge=0.0, le=4.0)
    status:      str
    enrolled_at: str

class AttendanceRecord(BaseModel):
    student_id: int
    present:    bool

class AttendanceSave(BaseModel):
    date:    str
    records: List[AttendanceRecord]


# ── HELPERS ────────────────────────────────────────────────────────
def row_to_dict(row):
    return dict(row) if row else None

def rows_to_list(rows):
    return [dict(r) for r in rows]

def next_student_id(cur) -> str:
    count = cur.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    year = date.today().year
    return f"STU-{year}-{str(count + 1).zfill(3)}"


# ── ROUTES: STATS ──────────────────────────────────────────────────
@app.get("/api/stats")
def get_stats():
    conn = get_db()
    cur = conn.cursor()
    today = date.today().isoformat()

    total   = cur.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    avg_gpa = cur.execute("SELECT ROUND(AVG(gpa),2) FROM students WHERE status='Active'").fetchone()[0] or 0.0
    present = cur.execute("SELECT COUNT(*) FROM attendance WHERE date=? AND present=1", (today,)).fetchone()[0]
    att_rate = round((present / total * 100), 1) if total else 0.0

    conn.close()
    return {
        "total_students":  total,
        "average_gpa":     avg_gpa,
        "attendance_rate": att_rate,
        "present_today":   present,
    }


# ── ROUTES: STUDENTS ───────────────────────────────────────────────
@app.get("/api/students")
def list_students(
    search:  Optional[str] = Query(None),
    grade:   Optional[str] = Query(None),
    subject: Optional[str] = Query(None),
    status:  Optional[str] = Query(None),
):
    conn = get_db()
    cur = conn.cursor()
    today = date.today().isoformat()

    sql = """
        SELECT s.*,
               COALESCE(a.present, -1) AS today_present
        FROM students s
        LEFT JOIN attendance a ON a.student_id = s.id AND a.date = ?
        WHERE 1=1
    """
    params: list = [today]

    if search:
        sql += " AND (s.name LIKE ? OR s.student_id LIKE ? OR s.email LIKE ?)"
        like = f"%{search}%"
        params += [like, like, like]
    if grade:
        sql += " AND s.grade = ?"
        params.append(grade)
    if subject:
        sql += " AND s.subject = ?"
        params.append(subject)
    if status:
        sql += " AND s.status = ?"
        params.append(status)

    sql += " ORDER BY s.name ASC"
    rows = cur.execute(sql, params).fetchall()
    conn.close()
    return {"students": rows_to_list(rows)}


@app.get("/api/students/{student_id}")
def get_student(student_id: int):
    conn = get_db()
    row = conn.execute("SELECT * FROM students WHERE id=?", (student_id,)).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"student": row_to_dict(row)}


@app.post("/api/students", status_code=201)
def create_student(data: StudentCreate):
    conn = get_db()
    cur = conn.cursor()
    sid = next_student_id(cur)
    try:
        cur.execute(
            "INSERT INTO students (student_id,name,email,grade,subject,gpa,status,enrolled_at) VALUES (?,?,?,?,?,?,?,?)",
            (sid, data.name, data.email, data.grade, data.subject, data.gpa, data.status, data.enrolled_at)
        )
        conn.commit()
        new_id = cur.lastrowid
    except sqlite3.IntegrityError as e:
        conn.close()
        raise HTTPException(status_code=400, detail=str(e))
    conn.close()
    return {"success": True, "id": new_id, "student_id": sid}


@app.put("/api/students/{student_id}")
def update_student(student_id: int, data: StudentUpdate):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """UPDATE students SET name=?,email=?,grade=?,subject=?,gpa=?,status=?,
           enrolled_at=?,updated_at=datetime('now') WHERE id=?""",
        (data.name, data.email, data.grade, data.subject, data.gpa,
         data.status, data.enrolled_at, student_id)
    )
    if cur.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Student not found")
    conn.commit()
    conn.close()
    return {"success": True}


@app.delete("/api/students/{student_id}")
def delete_student(student_id: int):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id=?", (student_id,))
    if cur.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Student not found")
    conn.commit()
    conn.close()
    return {"success": True}


# ── ROUTES: ATTENDANCE ─────────────────────────────────────────────
@app.get("/api/attendance")
def get_attendance(date_str: str = Query(default=None, alias="date")):
    if not date_str:
        date_str = date.today().isoformat()
    conn = get_db()
    rows = conn.execute("""
        SELECT s.id, s.name, s.student_id AS sid,
               COALESCE(a.present, 0) AS present
        FROM students s
        LEFT JOIN attendance a ON a.student_id=s.id AND a.date=?
        ORDER BY s.name
    """, (date_str,)).fetchall()
    conn.close()
    return {"date": date_str, "records": rows_to_list(rows)}


@app.post("/api/attendance")
def save_attendance(data: AttendanceSave):
    conn = get_db()
    cur = conn.cursor()
    for rec in data.records:
        cur.execute(
            "INSERT INTO attendance (student_id,date,present) VALUES (?,?,?) ON CONFLICT(student_id,date) DO UPDATE SET present=excluded.present",
            (rec.student_id, data.date, 1 if rec.present else 0)
        )
    conn.commit()
    conn.close()
    return {"success": True}


# ── ROUTES: GRADE HISTORY ──────────────────────────────────────────
@app.get("/api/grade-history")
def get_grade_history(student_id: Optional[int] = Query(None)):
    conn = get_db()
    if student_id:
        rows = conn.execute(
            "SELECT period,gpa,recorded_at FROM grade_history WHERE student_id=? ORDER BY recorded_at",
            (student_id,)
        ).fetchall()
    else:
        rows = conn.execute("""
            SELECT period, ROUND(AVG(gpa),2) AS gpa, MIN(recorded_at) AS recorded_at
            FROM grade_history GROUP BY period ORDER BY recorded_at
        """).fetchall()
    conn.close()
    return {"history": rows_to_list(rows)}
