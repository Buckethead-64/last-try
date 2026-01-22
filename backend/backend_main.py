from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .models import Base
from .crud import create_user, get_user, create_attendance, update_checkout, get_daily_logs, get_monthly_report
from .schemas import UserCreate, User, AttendanceCreate, CheckoutRequest, Attendance, DailyLog, MonthlyReport
from datetime import datetime

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Attendance Tracking System")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=User)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)

@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/checkin/", response_model=Attendance)
def check_in(attendance: AttendanceCreate, db: Session = Depends(get_db)):
    return create_attendance(db, attendance)

@app.post("/checkout/", response_model=Attendance)
def check_out(request: CheckoutRequest, db: Session = Depends(get_db)):
    att = update_checkout(db, request.user_id, request.check_out)
    if not att:
        raise HTTPException(status_code=400, detail="No active check-in found")
    return att

@app.get("/daily_logs/{date}", response_model=list[DailyLog])
def get_daily_logs_endpoint(date: str, db: Session = Depends(get_db)):
    attendances = get_daily_logs(db, date)
    logs = []
    for att in attendances:
        user = get_user(db, att.user_id)
        logs.append(DailyLog(user=user, check_in=att.check_in, check_out=att.check_out))
    return logs

@app.get("/monthly_report/{year}/{month}", response_model=list[MonthlyReport])
def get_monthly_report_endpoint(year: int, month: int, db: Session = Depends(get_db)):
    return get_monthly_report(db, year, month)