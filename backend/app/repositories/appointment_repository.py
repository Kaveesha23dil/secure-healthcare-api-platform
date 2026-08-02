from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from app.models.appointment import Appointment


class AppointmentRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get(self, appointment_id: UUID) -> Appointment | None:
        return self.db.scalar(
            select(Appointment)
            .options(joinedload(Appointment.slot))
            .where(Appointment.id == appointment_id)
        )

    def add(self, appointment: Appointment) -> Appointment:
        self.db.add(appointment)
        self.db.flush()
        return appointment

    def list_for_patient(
        self, patient_id: UUID, page: int, size: int, status: str | None = None
    ) -> tuple[list[Appointment], int]:
        filters = [Appointment.patient_id == patient_id] + (
            [Appointment.status == status] if status else []
        )
        query = (
            select(Appointment)
            .options(joinedload(Appointment.slot))
            .where(*filters)
            .order_by(Appointment.created_at.desc())
        )
        count = select(func.count()).select_from(Appointment).where(*filters)
        return list(self.db.scalars(query.offset((page - 1) * size).limit(size))), int(
            self.db.scalar(count) or 0
        )

    def list_all(
        self, page: int, size: int, status: str | None = None, doctor_id: UUID | None = None
    ) -> tuple[list[Appointment], int]:
        filters = []
        if status:
            filters.append(Appointment.status == status)
        if doctor_id:
            filters.append(Appointment.doctor_id == doctor_id)
        query = (
            select(Appointment)
            .options(joinedload(Appointment.slot))
            .where(*filters)
            .order_by(Appointment.created_at.desc())
        )
        count = select(func.count()).select_from(Appointment).where(*filters)
        return list(self.db.scalars(query.offset((page - 1) * size).limit(size))), int(
            self.db.scalar(count) or 0
        )
