from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, UUIDPrimaryKeyMixin, utc_now


class AppointmentStatusHistory(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "appointment_status_history"

    appointment_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("appointments.id"), index=True)
    previous_status: Mapped[str | None] = mapped_column(String(24), nullable=True)
    new_status: Mapped[str] = mapped_column(String(24))
    changed_by_subject: Mapped[str] = mapped_column(String(255))
    changed_by_role: Mapped[str] = mapped_column(String(32))
    reason: Mapped[str | None] = mapped_column(String(255), nullable=True)
    changed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    appointment = relationship("Appointment", back_populates="status_history")
