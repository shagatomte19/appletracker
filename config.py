import os
from pathlib import Path

# Database configuration
DATABASE_PATH = Path("job_applications.db")
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Streamlit configuration
PAGE_TITLE = "🎯 Job Application Tracker"
PAGE_ICON = "🎯"
LAYOUT = "wide"

# Status options
STATUS_OPTIONS = [
    "Applied",
    "Phone Screen",
    "Technical Interview", 
    "Onsite Interview",
    "Final Interview",
    "Offered",
    "Accepted",
    "Rejected",
    "Withdrawn",
    "Follow-up"
]

# Status colors for visualization
STATUS_COLORS = {
    "Applied": "#3b82f6",
    "Phone Screen": "#f59e0b", 
    "Technical Interview": "#f97316",
    "Onsite Interview": "#ef4444",
    "Final Interview": "#8b5cf6",
    "Offered": "#10b981",
    "Accepted": "#059669",
    "Rejected": "#dc2626",
    "Withdrawn": "#6b7280",
    "Follow-up": "#8b5cf6"
}
