from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import Appointment, AppointmentStatusHistory, AvailabilitySlot, Doctor, Patient

DOCTOR_SCOPES = {"appointment:read", "appointment:update", "appointment:cancel"}


def assigned_appointment(db: Session) -> Appointment:
    patient = db.query(Patient).filter(Patient.patient_reference == "FP-A").one()
    doctor = db.query(Doctor).filter(Doctor.user.has(external_subject="doctor-a")).one()
    slot = db.query(AvailabilitySlot).filter(AvailabilitySlot.doctor_id == doctor.id).first()
    slot.status = "reserved"
    appointment = Appointment(
        patient_id=patient.id,
        doctor_id=doctor.id,
        slot_id=slot.id,
        status="booked",
        reason="Fictional assigned consultation",
    )
    db.add(appointment)
    db.commit()
    return appointment


def test_doctor_can_read_and_transition_assigned_appointment(
    client: TestClient, db: Session, authenticate
) -> None:
    appointment = assigned_appointment(db)
    authenticate("doctor-a", {"doctor"}, DOCTOR_SCOPES)
    assert client.get(f"/api/v1/appointments/{appointment.id}").status_code == 200
    response = client.patch(f"/api/v1/appointments/{appointment.id}", json={"status": "checked-in"})
    assert response.status_code == 200
    assert db.query(AppointmentStatusHistory).filter_by(appointment_id=appointment.id).count() == 1


def test_doctor_cannot_access_or_update_unassigned_appointment(
    client: TestClient, db: Session, authenticate
) -> None:
    appointment = assigned_appointment(db)
    authenticate("doctor-b", {"doctor"}, DOCTOR_SCOPES)
    assert client.get(f"/api/v1/appointments/{appointment.id}").status_code == 404
    assert (
        client.patch(
            f"/api/v1/appointments/{appointment.id}", json={"status": "checked-in"}
        ).status_code
        == 404
    )
