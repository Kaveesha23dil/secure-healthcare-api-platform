from datetime import datetime
from enum import StrEnum
from uuid import UUID

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class AvailabilityStatus(StrEnum):
    AVAILABLE = "available"
    RESERVED = "reserved"
    UNAVAILABLE = "unavailable"
    CANCELLED = "cancelled"


class AvailabilitySlot(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "doctor_availability_slots"
    __table_args__ = (
        CheckConstraint("start_time < end_time", name="time_order"),
        CheckConstraint(
            "status IN ('available','reserved','unavailable','cancelled')", name="status"
        ),
        Index("ix_availability_doctor_start", "doctor_id", "start_time"),
    )

    doctor_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("doctors.id"), index=True)
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(String(24), default=AvailabilityStatus.AVAILABLE.value)
    created_by: Mapped[UUID | None] = mapped_column(Uuid, nullable=True)
    updated_by: Mapped[UUID | None] = mapped_column(Uuid, nullable=True)

    doctor = relationship("Doctor", back_populates="availability_slots")
    appointments = relationship("Appointment", back_populates="slot")
