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
