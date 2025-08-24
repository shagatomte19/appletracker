import sqlite3
import pandas as pd
from datetime import datetime
from typing import List, Optional
from models import JobApplication
from config import DATABASE_PATH

class DatabaseManager:
    def __init__(self):
        self.db_path = DATABASE_PATH
        self.init_database()
    
    def init_database(self):
        """Initialize the database and create tables if they don't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS job_applications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_title TEXT NOT NULL,
                    company_name TEXT NOT NULL,
                    location TEXT NOT NULL,
                    application_date DATE NOT NULL,
                    status TEXT NOT NULL,
                    salary_range TEXT,
                    job_description TEXT,
                    notes TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
    
    def add_application(self, application: JobApplication) -> int:
        """Add a new job application to the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO job_applications 
                (job_title, company_name, location, application_date, status, 
                 salary_range, job_description, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                application.job_title,
                application.company_name,
                application.location,
                application.application_date,
                application.status,
                application.salary_range,
                application.job_description,
                application.notes
            ))
            conn.commit()
            return cursor.lastrowid
    
    def get_all_applications(self) -> List[JobApplication]:
        """Retrieve all job applications from the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM job_applications 
                ORDER BY application_date DESC
            ''')
            rows = cursor.fetchall()
            
            applications = []
            for row in rows:
                applications.append(JobApplication(
                    id=row[0],
                    job_title=row[1],
                    company_name=row[2],
                    location=row[3],
                    application_date=row[4],
                    status=row[5],
                    salary_range=row[6],
                    job_description=row[7],
                    notes=row[8],
                    created_at=row[9],
                    updated_at=row[10]
                ))
            return applications
    
    def update_application(self, application_id: int, application: JobApplication) -> bool:
        """Update an existing job application."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE job_applications 
                SET job_title=?, company_name=?, location=?, application_date=?, 
                    status=?, salary_range=?, job_description=?, notes=?,
                    updated_at=CURRENT_TIMESTAMP
                WHERE id=?
            ''', (
                application.job_title,
                application.company_name,
                application.location,
                application.application_date,
                application.status,
                application.salary_range,
                application.job_description,
                application.notes,
                application_id
            ))
            conn.commit()
            return cursor.rowcount > 0
    
    def delete_application(self, application_id: int) -> bool:
        """Delete a job application from the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM job_applications WHERE id=?', (application_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def get_applications_df(self) -> pd.DataFrame:
        """Get all applications as a pandas DataFrame."""
        with sqlite3.connect(self.db_path) as conn:
            return pd.read_sql_query('''
                SELECT * FROM job_applications 
                ORDER BY application_date DESC
            ''', conn)
    
    def get_status_counts(self) -> dict:
        """Get count of applications by status."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT status, COUNT(*) as count 
                FROM job_applications 
                GROUP BY status
            ''')
            return dict(cursor.fetchall())