from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: str

class User(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True

class AttendanceCreate(BaseModel):
    user_id: int
    check_in: datetime

class CheckoutRequest(BaseModel):
    user_id: int
    check_out: datetime

class Attendance(BaseModel):
    id: int
    user_id: int
    check_in: datetime
    check_out: Optional[datetime]
    date: str

    class Config:
        orm_mode = True

class DailyLog(BaseModel):
    user: User
    check_in: datetime
    check_out: Optional[datetime]

class MonthlyReport(BaseModel):
    user_id: int
    total_days: int
    total_hours: float