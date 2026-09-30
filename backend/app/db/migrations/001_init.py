"""
Initial migration for Booking feature: create tables slots, bookings, audit_logs.
รองรับ: CON-TECH-01, DOM-PDPA-01, IF-HIS-01
"""
from __future__ import annotations

import argparse

from sqlalchemy import inspect
from sqlalchemy.engine import Engine

from app.db.session import create_memory_engine


def upgrade(engine: Engine):
    """Create all booking tables in the target engine.
    รองรับ: CON-TECH-01, DOM-PDPA-01, IF-HIS-01
    """
    from app.db.models import Base

    Base.metadata.create_all(bind=engine)
    return sorted(inspect(engine).get_table_names())


def downgrade(engine: Engine):
    """Drop all booking tables from the target engine.
    รองรับ: CON-TECH-01, DOM-PDPA-01, IF-HIS-01
    """
    from app.db.models import Base

    Base.metadata.drop_all(bind=engine)


def main():
    parser = argparse.ArgumentParser(description="Run the initial booking migration.")
    parser.add_argument(
        "--database-url",
        default="sqlite:///:memory:",
        help="Database URL to migrate. Defaults to an in-memory SQLite database.",
    )
    args = parser.parse_args()

    engine = create_memory_engine(args.database_url)
    tables = upgrade(engine)
    required_tables = {"slots", "bookings", "audit_logs"}

    if not required_tables.issubset(set(tables)):
        missing = sorted(required_tables - set(tables))
        raise RuntimeError(f"Missing required tables: {missing}")

    print("Tables:", tables)
    print("Migration executed successfully.")


if __name__ == "__main__":
    main()
