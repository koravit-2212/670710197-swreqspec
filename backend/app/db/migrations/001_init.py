"""
Initial migration for Booking feature: create tables slots, bookings, audit_logs.
รองรับ: CON-TECH-01, DOM-PDPA-01, IF-HIS-01
"""
from sqlalchemy import MetaData
from sqlalchemy.engine import Engine


def upgrade(engine: Engine):
    metadata = MetaData()
    metadata.reflect(bind=engine)
    # Import models to ensure tables definitions are available
    from ..db.models import Base

    Base.metadata.create_all(bind=engine)


def downgrade(engine: Engine):
    from ..db.models import Base

    Base.metadata.drop_all(bind=engine)
