from datetime import datetime

from database.connection import SessionLocal
from database.models import AuditLog


def log_ingestion(
    table_name,
    source_file,
    record_count
):

    db = SessionLocal()

    entry = AuditLog(
        audit_id=f"INGEST-{datetime.now().timestamp()}",
        user="pipeline",
        action="INGEST",
        table_accessed=table_name,
        record_count=record_count,
        timestamp=datetime.now(),
        purpose=f"Loaded from {source_file}",
    )

    db.add(entry)

    db.commit()

    db.close()