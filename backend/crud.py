from sqlalchemy.orm import Session
from .models import User, Attendance
from .schemas import UserCreate, AttendanceCreate
from datetime import datetime

def create_user(db: Session, user: UserCreate):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def create_attendance(db: Session, attendance: AttendanceCreate):
    date_str = attendance.check_in.strftime("%Y-%m-%d")
    db_attendance = Attendance(user_id=attendance.user_id, check_in=attendance.check_in, date=date_str)
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

def update_checkout(db: Session, user_id: int, check_out: datetime):
    # Find the latest attendance for user without checkout
    att = db.query(Attendance).filter(Attendance.user_id == user_id, Attendance.check_out == None).order_by(Attendance.check_in.desc()).first()
    if att:
        att.check_out = check_out
        db.commit()
        db.refresh(att)
    return att

def get_daily_logs(db: Session, date: str):
    return db.query(Attendance).filter(Attendance.date == date).all()

def get_monthly_report(db: Session, year: int, month: int):
    # Calculate start and end date
    import calendar
    start_date = datetime(year, month, 1)
    _, last_day = calendar.monthrange(year, month)
    end_date = datetime(year, month, last_day)
    
    attendances = db.query(Attendance).filter(Attendance.check_in >= start_date, Attendance.check_in <= end_date).all()
    
    from collections import defaultdict
    report = defaultdict(lambda: {"total_days": 0, "total_hours": 0.0})
    
    for att in attendances:
        if att.check_out:
            hours = (att.check_out - att.check_in).total_seconds() / 3600
            report[att.user_id]["total_hours"] += hours
            report[att.user_id]["total_days"] += 1
    
    return [{"user_id": uid, **data} for uid, data in report.items()]