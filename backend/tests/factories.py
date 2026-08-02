from datetime import UTC, datetime, timedelta

from sqlalchemy.orm import Session

from app.models import AvailabilitySlot, Doctor, Patient, User


def create_fictional_data(db: Session) -> dict[str, object]:
    roles = {
        "patient-a": "patient",
        "patient-b": "patient",
        "doctor-a": "doctor",
        "doctor-b": "doctor",
        "admin-a": "administrator",
    }
    users = {
        name: User(
            external_subject=name,
            email=f"{name}@example.com",
            display_name=name.replace("-", " ").title(),
            role=role,
        )
        for name, role in roles.items()
    }
    db.add_all(users.values())
    db.flush()
    pa = Patient(user_id=users["patient-a"].id, patient_reference="FP-A")
    pb = Patient(user_id=users["patient-b"].id, patient_reference="FP-B")
    da = Doctor(
        user_id=users["doctor-a"].id,
        display_name="Dr. Avery Rowan",
        specialization="Family Medicine",
        clinic_name="Example Clinic",
    )
    dbb = Doctor(
        user_id=users["doctor-b"].id,
        display_name="Dr. Jordan Vale",
        specialization="Cardiology",
        clinic_name="Example Clinic",
    )
    db.add_all([pa, pb, da, dbb])
    db.flush()
    now = datetime.now(UTC)
    slots = [
        AvailabilitySlot(
            doctor_id=da.id,
            start_time=now + timedelta(days=1),
            end_time=now + timedelta(days=1, minutes=30),
        ),
        AvailabilitySlot(
            doctor_id=dbb.id,
            start_time=now + timedelta(days=2),
            end_time=now + timedelta(days=2, minutes=30),
        ),
        AvailabilitySlot(
            doctor_id=da.id,
            start_time=now - timedelta(days=2),
            end_time=now - timedelta(days=2) + timedelta(minutes=30),
        ),
        AvailabilitySlot(
            doctor_id=da.id,
            start_time=now + timedelta(days=3),
            end_time=now + timedelta(days=3, minutes=30),
            status="cancelled",
        ),
    ]
    db.add_all(slots)
    db.commit()
    return {
        **users,
        "patient_model_a": pa,
        "patient_model_b": pb,
        "doctor_model_a": da,
        "doctor_model_b": dbb,
        "slots": slots,
    }
