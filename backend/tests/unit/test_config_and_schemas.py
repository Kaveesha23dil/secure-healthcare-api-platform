import pytest
from pydantic import ValidationError

from app.core.config import Settings
from app.schemas.appointment import CreateAppointmentRequest, UpdateAppointmentRequest


def test_production_rejects_debug_and_wildcard() -> None:
    with pytest.raises(ValidationError):
        Settings(app_env="production", app_debug=True)
    with pytest.raises(ValidationError):
        Settings(app_env="production", allowed_origins="*")


def test_create_appointment_forbids_mass_assignment() -> None:
    with pytest.raises(ValidationError):
        CreateAppointmentRequest(
            doctorId="01e44bfb-2672-4ca1-b03e-b5ec9410fdd7",
            slotId="83f2505d-7e7d-4217-a834-415b78b04ec1",
            reason="General consultation",
            patientId="bad",
        )
    with pytest.raises(ValidationError):
        UpdateAppointmentRequest(status="invalid")
