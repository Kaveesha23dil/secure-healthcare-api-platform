from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.patient import Patient
from app.models.user import User


class PatientRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def by_subject(self, subject: str) -> Patient | None:
        return self.db.scalar(
            select(Patient)
            .join(User)
            .where(User.external_subject == subject, User.active.is_(True))
        )

    def list(self, page: int, size: int) -> tuple[list[Patient], int]:
        query = (
            select(Patient)
            .join(User)
            .order_by(User.display_name)
            .offset((page - 1) * size)
            .limit(size)
        )
        return list(self.db.scalars(query)), int(
            self.db.scalar(select(func.count()).select_from(Patient)) or 0
        )
