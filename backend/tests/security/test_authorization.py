from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import Appointment, AvailabilitySlot, Doctor, Patient

PATIENT_SCOPES = {
    "doctor:read",
    "availability:read",
    "appointment:create",
    "appointment:read",
    "appointment:cancel",
}
ADMIN_SCOPES = {
    "doctor:read",
    "doctor:write",
    "appointment:read:all",
    "admin:manage",
    "patient:read",
}


def test_missing_token_is_401(client: TestClient) -> None:
    assert client.get("/api/v1/doctors").status_code == 401


def test_scope_required(client: TestClient, authenticate) -> None:
    authenticate("patient-a", {"patient"}, set())
    assert client.get("/api/v1/doctors").status_code == 403


def test_role_and_scope_both_required_for_admin(client: TestClient, authenticate) -> None:
    payload = {"displayName": "Dr. Fiction", "specialization": "Example", "clinicName": "Example"}
    authenticate("admin-a", {"administrator"}, {"doctor:write"})
    assert client.post("/api/v1/doctors", json=payload).status_code == 403
    authenticate("patient-a", {"patient"}, {"doctor:write", "admin:manage"})
    assert client.post("/api/v1/doctors", json=payload).status_code == 403


def test_patient_cannot_access_admin(client: TestClient, authenticate) -> None:
    authenticate("patient-a", {"patient"}, PATIENT_SCOPES)
    assert client.get("/api/v1/admin/appointments").status_code == 403


def test_admin_can_manage_doctor(client: TestClient, authenticate) -> None:
    authenticate("admin-a", {"administrator"}, ADMIN_SCOPES)
    payload = {
        "displayName": "Dr. Fiction Example",
        "specialization": "General",
        "clinicName": "Fictional Clinic",
    }
    created = client.post("/api/v1/doctors", json=payload)
    assert created.status_code == 201
    doctor_id = created.json()["id"]
    assert client.patch(f"/api/v1/doctors/{doctor_id}", json={"active": True}).status_code == 200
    assert client.delete(f"/api/v1/doctors/{doctor_id}").status_code == 204


def test_patient_ownership_is_concealed(client: TestClient, db: Session, authenticate) -> None:
    pb = db.query(Patient).filter(Patient.patient_reference == "FP-B").one()
    doctor = db.query(Doctor).first()
    slot = db.query(AvailabilitySlot).first()
    appointment = Appointment(
        patient_id=pb.id,
        doctor_id=doctor.id,
        slot_id=slot.id,
        status="booked",
        reason="Sensitive fictional reason",
    )
    db.add(appointment)
    db.commit()
    authenticate("patient-a", {"patient"}, PATIENT_SCOPES)
    response = client.get(f"/api/v1/appointments/{appointment.id}")
    assert response.status_code == 404
    assert "Sensitive" not in response.text
