from datetime import datetime
from enum import StrEnum
from uuid import UUID

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, String, Text, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class AppointmentStatus(StrEnum):
    PROPOSED = "proposed"
    BOOKED = "booked"
    CHECKED_IN = "checked-in"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no-show"


ACTIVE_STATUSES = ("proposed", "booked", "checked-in")


class Appointment(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "appointments"
    __table_args__ = (
        CheckConstraint(
            "status IN ('proposed','booked','checked-in','completed','cancelled','no-show')",
            name="status",
        ),
        Index("ix_appointments_patient_created", "patient_id", "created_at"),
        Index("ix_appointments_doctor_status", "doctor_id", "status"),
        Index(
            "uq_appointments_active_slot",
            "slot_id",
            unique=True,
            postgresql_where=text("status IN ('proposed','booked','checked-in')"),
            sqlite_where=text("status IN ('proposed','booked','checked-in')"),
        ),
    )

    patient_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("patients.id"), index=True)
    doctor_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("doctors.id"), index=True)
    slot_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("doctor_availability_slots.id"), index=True
    )
    status: Mapped[str] = mapped_column(
        String(24), default=AppointmentStatus.BOOKED.value, index=True
    )
    reason: Mapped[str] = mapped_column(Text)
    created_by: Mapped[UUID | None] = mapped_column(Uuid, nullable=True)
    updated_by: Mapped[UUID | None] = mapped_column(Uuid, nullable=True)
    cancelled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")
    slot = relationship("AvailabilitySlot", back_populates="appointments")
    status_history = relationship("AppointmentStatusHistory", back_populates="appointment")
