"""
Session and engine helper for tests and migrations.
รองรับ: CON-TECH-01
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def create_memory_engine():
    # ใช้ SQLite ในหน่วยความจำ สำหรับรัน migration และทดสอบตาม plan.md
    return create_engine("sqlite:///:memory:")


def create_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()
