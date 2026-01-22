# Attendance Tracking System

This is a full-stack attendance tracking system with a FastAPI backend and Streamlit frontend.

## Backend Features

- User management
- Check-in and check-out tracking
- Daily logs retrieval
- Monthly reports with total hours and days

## Frontend Features

- Web interface for all backend operations
- User-friendly forms for creating users and managing attendance
- Display daily logs and monthly reports in tables

## Setup

1. Install Python 3.8 or higher.

2. Install backend dependencies:
   ```
   pip install -r backend/requirements.txt
   ```

3. Install frontend dependencies:
   ```
   pip install -r frontend/requirements.txt
   ```

4. Run the backend server:
   ```
   uvicorn backend.backend_main:app --reload
   ```

5. Run the frontend (in a new terminal):
   ```
   streamlit run frontend/frontend_main.py
   ```

The backend API will be available at http://127.0.0.1:8000 and the frontend at http://localhost:8501

## API Endpoints

- POST /users/ - Create a new user
- GET /users/{user_id} - Get user details
- POST /checkin/ - Check in a user
- POST /checkout/ - Check out a user
- GET /daily_logs/{date} - Get daily logs (YYYY-MM-DD)
- GET /monthly_report/{year}/{month} - Get monthly report

## Database

Uses SQLite database `attendance.db` in the backend folder.