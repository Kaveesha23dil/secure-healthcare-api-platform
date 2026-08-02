from datetime import datetime
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.availability import AvailabilitySlot


class AvailabilityRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_for_update(self, slot_id: UUID) -> AvailabilitySlot | None:
        return self.db.scalar(
            select(AvailabilitySlot).where(AvailabilitySlot.id == slot_id).with_for_update()
        )

    def list(
        self, doctor_id: UUID, page: int, size: int, start: datetime | None, end: datetime | None
    ) -> tuple[list[AvailabilitySlot], int]:
        filters = [AvailabilitySlot.doctor_id == doctor_id]
        if start:
            filters.append(AvailabilitySlot.start_time >= start)
        if end:
            filters.append(AvailabilitySlot.end_time <= end)
        query = select(AvailabilitySlot).where(*filters)
        count = select(func.count()).select_from(AvailabilitySlot).where(*filters)
        return list(
            self.db.scalars(
                query.order_by(AvailabilitySlot.start_time).offset((page - 1) * size).limit(size)
            )
        ), int(self.db.scalar(count) or 0)

    def overlaps(self, doctor_id: UUID, start: datetime, end: datetime) -> bool:
        query = select(AvailabilitySlot.id).where(
            AvailabilitySlot.doctor_id == doctor_id,
            AvailabilitySlot.start_time < end,
            AvailabilitySlot.end_time > start,
            AvailabilitySlot.status != "cancelled",
        )
        return self.db.scalar(query.limit(1)) is not None

    def add(self, slot: AvailabilitySlot) -> AvailabilitySlot:
        self.db.add(slot)
        self.db.flush()
        return slot
