from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime, timedelta
from threading import Barrier

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.models import Appointment, AvailabilitySlot, Doctor, Patient, User


def test_database_constraint_allows_only_one_active_booking(tmp_path) -> None:
    engine = create_engine(f"sqlite+pysqlite:///{tmp_path / 'booking.db'}")
    Base.metadata.create_all(engine)
    sessions = sessionmaker(bind=engine, expire_on_commit=False)
    with sessions.begin() as db:
        user_a = User(external_subject="race-a", display_name="Race A", role="patient")
        user_b = User(external_subject="race-b", display_name="Race B", role="patient")
        db.add_all([user_a, user_b])
        db.flush()
        patient_a = Patient(user_id=user_a.id, patient_reference="RACE-A")
        patient_b = Patient(user_id=user_b.id, patient_reference="RACE-B")
        doctor = Doctor(
            display_name="Dr. Concurrency Example",
            specialization="Testing",
            clinic_name="Fictional Clinic",
        )
        db.add_all([patient_a, patient_b, doctor])
        db.flush()
        slot = AvailabilitySlot(
            doctor_id=doctor.id,
            start_time=datetime.now(UTC) + timedelta(days=1),
            end_time=datetime.now(UTC) + timedelta(days=1, minutes=30),
        )
        db.add(slot)
        db.flush()
        ids = patient_a.id, patient_b.id, doctor.id, slot.id
    barrier = Barrier(2)

    def book(patient_id) -> str:
        with sessions() as db:
            db.add(
                Appointment(
                    patient_id=patient_id,
                    doctor_id=ids[2],
                    slot_id=ids[3],
                    status="booked",
                    reason="Fictional concurrent request",
                )
            )
            barrier.wait()
            try:
                db.commit()
            except IntegrityError:
                db.rollback()
                return "conflict"
            return "created"

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(book, ids[:2]))
    assert sorted(results) == ["conflict", "created"]
    with sessions() as db:
        assert db.query(Appointment).filter(Appointment.slot_id == ids[3]).count() == 1
