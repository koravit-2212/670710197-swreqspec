"""
SQLAlchemy models for Booking feature.
รองรับ: CON-TECH-01, DOM-PDPA-01, IF-HIS-01
"""
from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Time,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Slot(Base):
    """รองรับ: FR-BKG-01, FR-BKG-06
    ตารางเก็บช่วงเวลาและที่นั่ง (slots)
    """
    __tablename__ = "slots"
    id = Column(Integer, primary_key=True, autoincrement=True)
    slot_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    package_code = Column(String(32), nullable=False)
    capacity = Column(Integer, nullable=False, default=0)
    remaining = Column(Integer, nullable=False, default=0)


class Booking(Base):
    """รองรับ: FR-BKG-02, FR-BKG-04, IF-HIS-01
    ตารางเก็บการจอง (bookings). เก็บเฉพาะ `hn` ตาม IF-HIS-01
    ไม่เก็บเลขบัตรประชาชน
    """
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, autoincrement=True)
    hn = Column(String(64), nullable=False, index=True)
    slot_id = Column(Integer, ForeignKey("slots.id"), nullable=False)
    booking_date = Column(DateTime(timezone=True), server_default=func.now())
    queue_no = Column(String(32), nullable=True)  # Q-02: format pending
    status = Column(String(32), nullable=False, default="confirmed")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    slot = relationship("Slot")


class AuditLog(Base):
    """รองรับ: DOM-PDPA-01
    บันทึก audit log เมื่อเข้าถึงข้อมูลการจอง
    """
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    actor_id = Column(String(128), nullable=False)
    action = Column(String(128), nullable=False)
    hn = Column(String(64), nullable=True, index=True)
    accessed_at = Column(DateTime(timezone=True), server_default=func.now())
