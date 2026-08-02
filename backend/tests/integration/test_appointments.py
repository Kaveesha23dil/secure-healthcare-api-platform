from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import AuditEvent, AvailabilitySlot, Doctor

SCOPES = {"appointment:create", "appointment:read", "appointment:cancel"}


def booking_payload(db: Session) -> dict[str, str]:
    slot = (
        db.query(AvailabilitySlot)
        .filter(AvailabilitySlot.status == "available")
        .order_by(AvailabilitySlot.start_time.desc())
        .first()
    )
    return {
        "doctorId": str(slot.doctor_id),
        "slotId": str(slot.id),
        "reason": "General fictional consultation",
    }


def test_patient_books_views_lists_and_cancels(
    client: TestClient, db: Session, authenticate
) -> None:
    authenticate("patient-a", {"patient"}, SCOPES)
    created = client.post("/api/v1/appointments", json=booking_payload(db))
    assert created.status_code == 201
    appointment_id = created.json()["id"]
    assert client.get(f"/api/v1/appointments/{appointment_id}").status_code == 200
    assert len(client.get("/api/v1/patients/me/appointments").json()["items"]) == 1
    cancelled = client.patch(f"/api/v1/appointments/{appointment_id}", json={"status": "cancelled"})
    assert cancelled.status_code == 200
    assert cancelled.json()["status"] == "cancelled"
    assert db.query(AuditEvent).count() >= 3


def test_mass_assignment_and_validation_rejected(
    client: TestClient, db: Session, authenticate
) -> None:
    authenticate("patient-a", {"patient"}, SCOPES)
    value = booking_payload(db)
    value["patientId"] = "01e44bfb-2672-4ca1-b03e-b5ec9410fdd7"
    assert client.post("/api/v1/appointments", json=value).status_code == 422
    value = booking_payload(db)
    value["reason"] = "x" * 501
    assert client.post("/api/v1/appointments", json=value).status_code == 422


def test_duplicate_wrong_doctor_past_and_cancelled_rejected(
    client: TestClient, db: Session, authenticate
) -> None:
    authenticate("patient-a", {"patient"}, SCOPES)
    value = booking_payload(db)
    assert client.post("/api/v1/appointments", json=value).status_code == 201
    assert client.post("/api/v1/appointments", json=value).status_code == 409
    available = (
        db.query(AvailabilitySlot)
        .filter(AvailabilitySlot.status == "available")
        .order_by(AvailabilitySlot.start_time.desc())
        .first()
    )
    wrong = db.query(Doctor).filter(Doctor.id != available.doctor_id).first()
    assert (
        client.post(
            "/api/v1/appointments",
            json={"doctorId": str(wrong.id), "slotId": str(available.id), "reason": "Fiction"},
        ).status_code
        == 404
    )
    past = db.query(AvailabilitySlot).order_by(AvailabilitySlot.start_time).first()
    past.status = "available"
    db.commit()
    assert (
        client.post(
            "/api/v1/appointments",
            json={"doctorId": str(past.doctor_id), "slotId": str(past.id), "reason": "Fiction"},
        ).status_code
        == 409
    )
    cancelled = db.query(AvailabilitySlot).filter(AvailabilitySlot.status == "cancelled").first()
    assert (
        client.post(
            "/api/v1/appointments",
            json={
                "doctorId": str(cancelled.doctor_id),
                "slotId": str(cancelled.id),
                "reason": "Fiction",
            },
        ).status_code
        == 409
    )


def test_patient_cannot_complete(client: TestClient, db: Session, authenticate) -> None:
    authenticate("patient-a", {"patient"}, SCOPES)
    created = client.post("/api/v1/appointments", json=booking_payload(db))
    appointment_id = created.json()["id"]
    assert client.patch(
        f"/api/v1/appointments/{appointment_id}", json={"status": "completed"}
    ).status_code in {403, 409}
