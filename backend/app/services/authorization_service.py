from app.core.exceptions import AuthorizationError, ResourceNotFoundError
from app.core.security import AuthenticatedUser
from app.models.appointment import Appointment
from app.models.doctor import Doctor
from app.models.patient import Patient


class AuthorizationService:
    @staticmethod
    def require_role(actor: AuthenticatedUser, *roles: str) -> None:
        if not actor.roles.intersection(roles):
            raise AuthorizationError()

    @staticmethod
    def can_access_appointment(
        actor: AuthenticatedUser,
        appointment: Appointment,
        patient: Patient | None,
        doctor: Doctor | None,
    ) -> None:
        allowed = (
            "administrator" in actor.roles
            or (patient is not None and appointment.patient_id == patient.id)
            or (doctor is not None and appointment.doctor_id == doctor.id)
        )
        if not allowed:
            raise ResourceNotFoundError("Appointment")
