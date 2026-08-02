from datetime import UTC, datetime
from math import ceil
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import AuthorizationError, ConflictError, ResourceNotFoundError
from app.core.security import AuthenticatedUser
from app.models.appointment import Appointment, AppointmentStatus
from app.models.appointment_status_history import AppointmentStatusHistory
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.user import User
from app.repositories.appointment_repository import AppointmentRepository
from app.repositories.availability_repository import AvailabilityRepository
from app.repositories.patient_repository import PatientRepository
from app.schemas.appointment import CreateAppointmentRequest
from app.services.audit_service import AuditService
from app.services.authorization_service import AuthorizationService

TRANSITIONS: dict[str, frozenset[str]] = {
    "proposed": frozenset({"booked", "cancelled"}),
    "booked": frozenset({"checked-in", "cancelled", "no-show"}),
    "checked-in": frozenset({"completed", "cancelled"}),
    "completed": frozenset(),
    "cancelled": frozenset(),
    "no-show": frozenset(),
}


class AppointmentService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = AppointmentRepository(db)
        self.patients = PatientRepository(db)
        self.slots = AvailabilityRepository(db)
        self.audit = AuditService(db)

    def _patient(self, actor: AuthenticatedUser) -> Patient | None:
        return self.patients.by_subject(actor.subject)

    def _doctor(self, actor: AuthenticatedUser) -> Doctor | None:
        return self.db.scalar(
            select(Doctor)
            .join(User)
            .where(User.external_subject == actor.subject, User.active.is_(True))
        )

    def create(
        self,
        data: CreateAppointmentRequest,
        actor: AuthenticatedUser,
        request_id: str,
        source_ip: str | None,
    ) -> Appointment:
        AuthorizationService.require_role(actor, "patient")
        patient = self._patient(actor)
        if patient is None:
            raise ResourceNotFoundError("Patient")
        try:
            slot = self.slots.get_for_update(data.slot_id)
            if slot is None or slot.doctor_id != data.doctor_id:
                raise ResourceNotFoundError("Availability slot")
            start = (
                slot.start_time if slot.start_time.tzinfo else slot.start_time.replace(tzinfo=UTC)
            )
            if slot.status != "available":
                raise ConflictError("The availability slot cannot be booked.")
            if start <= datetime.now(UTC):
                raise ConflictError("Past availability cannot be booked.")
            appointment = self.repo.add(
                Appointment(
                    patient_id=patient.id,
                    doctor_id=data.doctor_id,
                    slot_id=data.slot_id,
                    status=AppointmentStatus.BOOKED.value,
                    reason=data.reason,
                )
            )
            slot.status = "reserved"
            self.db.add(
                AppointmentStatusHistory(
                    appointment_id=appointment.id,
                    previous_status=None,
                    new_status="booked",
                    changed_by_subject=actor.subject,
                    changed_by_role=actor.primary_role,
                )
            )
            self.audit.record(
                "APPOINTMENT_CREATED", actor, "appointment", appointment.id, request_id, source_ip
            )
            self.db.commit()
            return appointment
        except IntegrityError as exc:
            self.db.rollback()
            raise ConflictError("The availability slot is already booked.") from exc

    def get_authorized(
        self,
        appointment_id: UUID,
        actor: AuthenticatedUser,
        request_id: str | None = None,
        source_ip: str | None = None,
    ) -> Appointment:
        appointment = self.repo.get(appointment_id)
        if appointment is None:
            raise ResourceNotFoundError("Appointment")
        AuthorizationService.can_access_appointment(
            actor, appointment, self._patient(actor), self._doctor(actor)
        )
        if request_id:
            self.audit.record(
                "APPOINTMENT_VIEWED", actor, "appointment", appointment.id, request_id, source_ip
            )
            self.db.commit()
        return appointment

    def update(
        self,
        appointment_id: UUID,
        target: str,
        actor: AuthenticatedUser,
        request_id: str,
        source_ip: str | None,
    ) -> Appointment:
        appointment = self.get_authorized(appointment_id, actor)
        patient = self._patient(actor)
        doctor = self._doctor(actor)
        is_patient = patient is not None and appointment.patient_id == patient.id
        is_doctor = doctor is not None and appointment.doctor_id == doctor.id
        is_admin = "administrator" in actor.roles
        if target not in TRANSITIONS[appointment.status]:
            raise ConflictError("The requested status transition is not allowed.")
        if is_patient and target != "cancelled":
            raise AuthorizationError()
        if not (is_patient or is_doctor or is_admin):
            raise ResourceNotFoundError("Appointment")
        previous = appointment.status
        appointment.status = target
        if target == "cancelled":
            appointment.cancelled_at = datetime.now(UTC)
            appointment.slot.status = "available"
        self.db.add(
            AppointmentStatusHistory(
                appointment_id=appointment.id,
                previous_status=previous,
                new_status=target,
                changed_by_subject=actor.subject,
                changed_by_role=actor.primary_role,
            )
        )
        event = "APPOINTMENT_CANCELLED" if target == "cancelled" else "APPOINTMENT_STATUS_CHANGED"
        self.audit.record(
            event,
            actor,
            "appointment",
            appointment.id,
            request_id,
            source_ip,
            metadata={"from": previous, "to": target},
        )
        self.db.commit()
        return appointment

    def list_mine(
        self, actor: AuthenticatedUser, page: int, size: int, status: str | None
    ) -> tuple[list[Appointment], int, int]:
        patient = self._patient(actor)
        if patient is None:
            raise ResourceNotFoundError("Patient")
        items, total = self.repo.list_for_patient(patient.id, page, size, status)
        return items, total, ceil(total / size)

    def list_all(
        self,
        actor: AuthenticatedUser,
        page: int,
        size: int,
        status: str | None,
        doctor_id: UUID | None,
    ) -> tuple[list[Appointment], int, int]:
        AuthorizationService.require_role(actor, "administrator")
        items, total = self.repo.list_all(page, size, status, doctor_id)
        return items, total, ceil(total / size)
