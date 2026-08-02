from datetime import UTC, datetime, timedelta

from sqlalchemy import select

from app.core.config import get_settings
from app.db.session import SessionLocal
from app.models import Appointment, AvailabilitySlot, Doctor, Patient, User


def seed() -> None:
    if get_settings().app_env == "production":
        raise RuntimeError("Seeding is prohibited in production")
    with SessionLocal.begin() as db:
        if db.scalar(select(User.id).limit(1)):
            return
        users = [
            User(
                external_subject="patient-a",
                email="patient.one@example.com",
                display_name="Fictional Patient One",
                role="patient",
            ),
            User(
                external_subject="patient-b",
                email="patient.two@example.com",
                display_name="Fictional Patient Two",
                role="patient",
            ),
            User(
                external_subject="doctor-a",
                email="doctor.one@example.com",
                display_name="Dr. Avery Rowan",
                role="doctor",
            ),
            User(
                external_subject="doctor-b",
                email="doctor.two@example.com",
                display_name="Dr. Jordan Vale",
                role="doctor",
            ),
            User(
                external_subject="admin-a",
                email="admin@example.com",
                display_name="Fictional Administrator",
                role="administrator",
            ),
        ]
        db.add_all(users)
        db.flush()
        patients = [
            Patient(user_id=users[0].id, patient_reference="FP-001"),
            Patient(user_id=users[1].id, patient_reference="FP-002"),
        ]
        doctors = [
            Doctor(
                user_id=users[2].id,
                display_name="Dr. Avery Rowan",
                specialization="Family Medicine",
                clinic_name="Example Clinic",
            ),
            Doctor(
                user_id=users[3].id,
                display_name="Dr. Jordan Vale",
                specialization="Cardiology",
                clinic_name="Example Clinic",
            ),
        ]
        db.add_all(patients)
        db.add_all(doctors)
        db.flush()
        slots = [
            AvailabilitySlot(
                doctor_id=doctors[i % 2].id,
                start_time=datetime.now(UTC) + timedelta(days=i + 1),
                end_time=datetime.now(UTC) + timedelta(days=i + 1, minutes=30),
            )
            for i in range(4)
        ]
        db.add_all(slots)
        db.flush()
        slots[0].status = "reserved"
        db.add(
            Appointment(
                patient_id=patients[0].id,
                doctor_id=doctors[0].id,
                slot_id=slots[0].id,
                status="booked",
                reason="Fictional routine consultation",
            )
        )


if __name__ == "__main__":
    seed()
