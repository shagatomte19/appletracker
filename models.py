from datetime import datetime
from typing import Optional, List
import sqlite3
from dataclasses import dataclass

@dataclass
class JobApplication:
    id: Optional[int]
    job_title: str
    company_name: str
    location: str
    application_date: str
    status: str
    salary_range: Optional[str] = None
    job_description: Optional[str] = None
    notes: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def to_dict(self):
        return {
            'id': self.id,
            'job_title': self.job_title,
            'company_name': self.company_name,
            'location': self.location,
            'application_date': self.application_date,
            'status': self.status,
            'salary_range': self.salary_range,
            'job_description': self.job_description,
            'notes': self.notes,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }