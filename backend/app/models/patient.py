from sqlalchemy import ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Patient(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "patients"

    user_id: Mapped[object] = mapped_column(Uuid, ForeignKey("users.id"), unique=True, index=True)
    patient_reference: Mapped[str] = mapped_column(String(64), unique=True)
    phone_number: Mapped[str | None] = mapped_column(String(32), nullable=True)
    user = relationship("User", back_populates="patient")
    appointments = relationship("Appointment", back_populates="patient")
