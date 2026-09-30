"""
Session and engine helper for tests and migrations.
รองรับ: CON-TECH-01
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def create_memory_engine(db_url: str = "sqlite:///:memory:"):
    """Create an SQLite engine for migration and test runs.
    รองรับ: CON-TECH-01
    """
    return create_engine(db_url)


def create_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()
