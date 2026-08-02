from math import ceil
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.exceptions import BadRequestError, ResourceNotFoundError
from app.core.security import AuthenticatedUser
from app.models.doctor import Doctor
from app.repositories.doctor_repository import DoctorRepository
from app.schemas.doctor import DoctorCreateRequest, DoctorUpdateRequest
from app.services.audit_service import AuditService
from app.services.authorization_service import AuthorizationService


class DoctorService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = DoctorRepository(db)
        self.audit = AuditService(db)

    def list(
        self, page: int, size: int, specialization: str | None
    ) -> tuple[list[Doctor], int, int]:
        items, total = self.repo.list(page, size, specialization)
        return items, total, ceil(total / size)

    def get(self, doctor_id: UUID) -> Doctor:
        doctor = self.repo.get(doctor_id)
        if doctor is None or not doctor.active:
            raise ResourceNotFoundError("Doctor")
        return doctor

    def create(
        self,
        data: DoctorCreateRequest,
        actor: AuthenticatedUser,
        request_id: str,
        source_ip: str | None,
    ) -> Doctor:
        AuthorizationService.require_role(actor, "administrator")
        doctor = self.repo.add(
            Doctor(
                display_name=data.display_name,
                specialization=data.specialization,
                clinic_name=data.clinic_name,
            )
        )
        self.audit.record("DOCTOR_CREATED", actor, "doctor", doctor.id, request_id, source_ip)
        self.db.commit()
        return doctor

    def update(
        self,
        doctor_id: UUID,
        data: DoctorUpdateRequest,
        actor: AuthenticatedUser,
        request_id: str,
        source_ip: str | None,
    ) -> Doctor:
        AuthorizationService.require_role(actor, "administrator")
        doctor = self.get(doctor_id)
        changes = data.model_dump(exclude_none=True)
        if not changes:
            raise BadRequestError("At least one property is required.")
        for key, value in changes.items():
            setattr(doctor, key, value)
        self.audit.record("DOCTOR_UPDATED", actor, "doctor", doctor.id, request_id, source_ip)
        self.db.commit()
        return doctor

    def deactivate(
        self, doctor_id: UUID, actor: AuthenticatedUser, request_id: str, source_ip: str | None
    ) -> None:
        AuthorizationService.require_role(actor, "administrator")
        doctor = self.get(doctor_id)
        doctor.active = False
        self.audit.record("DOCTOR_DEACTIVATED", actor, "doctor", doctor.id, request_id, source_ip)
        self.db.commit()
