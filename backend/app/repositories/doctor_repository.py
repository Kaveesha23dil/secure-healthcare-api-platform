from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.doctor import Doctor


class DoctorRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get(self, doctor_id: UUID) -> Doctor | None:
        return self.db.get(Doctor, doctor_id)

    def list(
        self, page: int, size: int, specialization: str | None = None
    ) -> tuple[list[Doctor], int]:
        query = select(Doctor).where(Doctor.active.is_(True))
        count = select(func.count()).select_from(Doctor).where(Doctor.active.is_(True))
        if specialization:
            query = query.where(Doctor.specialization == specialization)
            count = count.where(Doctor.specialization == specialization)
        return list(
            self.db.scalars(
                query.order_by(Doctor.display_name).offset((page - 1) * size).limit(size)
            )
        ), int(self.db.scalar(count) or 0)

    def add(self, doctor: Doctor) -> Doctor:
        self.db.add(doctor)
        self.db.flush()
        return doctor
