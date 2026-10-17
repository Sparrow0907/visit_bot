from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, Boolean, Text, BigInteger, ForeignKey, Date, Time, DateTime, String
from datetime import datetime

Base = declarative_base()

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    tg_user_id = Column(BigInteger, unique=True, index=True, nullable=False)
    first_name = Column(Text, nullable=True)
    username = Column(Text, nullable=True)
    
class Works(Base):
    __tablename__ = "works"

    id = Column(Integer, primary_key=True)
    file_id = Column(Text, nullable=False)
    title = Column(Text, nullable=True)
    price = Column(Text, nullable=True)
    description = Column(Text, nullable=True)

class Slot(Base):
    __tablename__ = "slots"

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False, index=True)   # только дата
    time_start = Column(Time, nullable=False)         # начало, напр. 15:00
    time_end = Column(Time, nullable=False)           # конец, напр. 16:00
    is_booked = Column(Boolean, default=False, nullable=False, index=True)

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    slot_id = Column(Integer, ForeignKey("slots.id"), nullable=False, unique=True)  # ← важно
    comment = Column(Text, nullable=True)
    status = Column(String(20), nullable=False, default="confirmed")

