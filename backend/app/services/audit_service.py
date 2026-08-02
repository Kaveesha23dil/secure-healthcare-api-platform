from uuid import UUID

from sqlalchemy.orm import Session

from app.core.security import AuthenticatedUser
from app.models.audit_event import AuditEvent
from app.repositories.audit_repository import AuditRepository


class AuditService:
    def __init__(self, db: Session) -> None:
        self.repo = AuditRepository(db)

    def record(
        self,
        event_type: str,
        actor: AuthenticatedUser,
        resource_type: str,
        resource_id: UUID | None,
        request_id: str,
        source_ip: str | None,
        result: str = "success",
        metadata: dict[str, object] | None = None,
    ) -> None:
        safe_metadata = {
            k: v
            for k, v in (metadata or {}).items()
            if k not in {"token", "reason", "password", "email", "phone"}
        }
        self.repo.add(
            AuditEvent(
                event_type=event_type,
                actor_subject=actor.subject,
                actor_role=actor.primary_role,
                resource_type=resource_type,
                resource_id=resource_id,
                result=result,
                request_id=request_id,
                source_ip=source_ip,
                event_metadata=safe_metadata,
            )
        )
