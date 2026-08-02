from datetime import UTC, datetime
from math import ceil
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError
from app.core.security import AuthenticatedUser
from app.models.availability import AvailabilitySlot
from app.models.doctor import Doctor
from app.models.user import User
from app.repositories.availability_repository import AvailabilityRepository
from app.schemas.availability import AvailabilitySlotCreateRequest
from app.services.audit_service import AuditService
from app.services.doctor_service import DoctorService


class AvailabilityService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = AvailabilityRepository(db)
        self.audit = AuditService(db)

    def list(
        self, doctor_id: UUID, page: int, size: int, start: datetime | None, end: datetime | None
    ) -> tuple[list[AvailabilitySlot], int, int]:
        DoctorService(self.db).get(doctor_id)
        items, total = self.repo.list(doctor_id, page, size, start, end)
        return items, total, ceil(total / size)

    def create(
        self,
        doctor_id: UUID,
        data: AvailabilitySlotCreateRequest,
        actor: AuthenticatedUser,
        request_id: str,
        source_ip: str | None,
    ) -> AvailabilitySlot:
        doctor = DoctorService(self.db).get(doctor_id)
        own_doctor = self.db.scalar(
            select(Doctor).join(User).where(User.external_subject == actor.subject)
        )
        if "administrator" not in actor.roles and (
            "doctor" not in actor.roles or own_doctor is None or own_doctor.id != doctor.id
        ):
            raise ConflictError("The schedule is not managed by this caller.")
        if data.start_time.astimezone(UTC) <= datetime.now(UTC):
            raise ConflictError("Availability cannot be created in the past.")
        if self.repo.overlaps(doctor_id, data.start_time, data.end_time):
            raise ConflictError("The slot overlaps existing availability.")
        slot = self.repo.add(
            AvailabilitySlot(
                doctor_id=doctor_id,
                start_time=data.start_time,
                end_time=data.end_time,
                status="available",
            )
        )
        self.audit.record(
            "AVAILABILITY_CREATED", actor, "availability", slot.id, request_id, source_ip
        )
        self.db.commit()
        return slot
