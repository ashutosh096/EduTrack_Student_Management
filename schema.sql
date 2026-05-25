-- EduTrack — SQLite Schema
-- This file is for reference only. Python will auto-create the DB on first run.

CREATE TABLE IF NOT EXISTS students (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id  TEXT NOT NULL UNIQUE,
    name        TEXT NOT NULL,
    email       TEXT NOT NULL,
    grade       TEXT NOT NULL CHECK(grade IN ('9','10','11','12')),
    subject     TEXT NOT NULL,
    gpa         REAL NOT NULL DEFAULT 0.0,
    status      TEXT NOT NULL DEFAULT 'Active' CHECK(status IN ('Active','Inactive','Suspended')),
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
