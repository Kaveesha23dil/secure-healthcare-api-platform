from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, Index, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Doctor(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "doctors"
    __table_args__ = (Index("ix_doctors_active_specialization", "active", "specialization"),)

    user_id: Mapped[UUID | None] = mapped_column(
        Uuid, ForeignKey("users.id"), unique=True, nullable=True
    )
    display_name: Mapped[str] = mapped_column(String(120))
    specialization: Mapped[str] = mapped_column(String(100), index=True)
    clinic_name: Mapped[str] = mapped_column(String(160))
    active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_by: Mapped[UUID | None] = mapped_column(Uuid, nullable=True)
    updated_by: Mapped[UUID | None] = mapped_column(Uuid, nullable=True)

    user = relationship("User", back_populates="doctor")
    availability_slots = relationship("AvailabilitySlot", back_populates="doctor")
    appointments = relationship("Appointment", back_populates="doctor")
