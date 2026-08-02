from sqlalchemy.orm import Session

from app.models.audit_event import AuditEvent


class AuditRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def add(self, event: AuditEvent) -> None:
        self.db.add(event)
        self.db.flush()
