"""Create healthcare core tables."""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision = "20260801_0001"
down_revision = None
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("external_subject", sa.String(255), nullable=False),
        sa.Column("email", sa.String(254)),
        sa.Column("display_name", sa.String(120), nullable=False),
        sa.Column("role", sa.String(32), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("role IN ('patient','doctor','administrator')", name="ck_users_role"),
        sa.UniqueConstraint("external_subject"),
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "patients",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id"), nullable=False, unique=True),
        sa.Column("patient_reference", sa.String(64), nullable=False, unique=True),
        sa.Column("phone_number", sa.String(32)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "doctors",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id"), unique=True),
        sa.Column("display_name", sa.String(120), nullable=False),
        sa.Column("specialization", sa.String(100), nullable=False),
        sa.Column("clinic_name", sa.String(160), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("created_by", sa.Uuid()),
        sa.Column("updated_by", sa.Uuid()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_doctors_active_specialization", "doctors", ["active", "specialization"])
    op.create_table(
        "doctor_availability_slots",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("doctor_id", sa.Uuid(), sa.ForeignKey("doctors.id"), nullable=False),
        sa.Column("start_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(24), nullable=False),
        sa.Column("created_by", sa.Uuid()),
        sa.Column("updated_by", sa.Uuid()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("start_time < end_time", name="ck_doctor_availability_slots_time_order"),
        sa.CheckConstraint(
            "status IN ('available','reserved','unavailable','cancelled')",
            name="ck_doctor_availability_slots_status",
        ),
    )
    op.create_index(
        "ix_availability_doctor_start", "doctor_availability_slots", ["doctor_id", "start_time"]
    )
    op.create_table(
        "appointments",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("patient_id", sa.Uuid(), sa.ForeignKey("patients.id"), nullable=False),
        sa.Column("doctor_id", sa.Uuid(), sa.ForeignKey("doctors.id"), nullable=False),
        sa.Column(
            "slot_id", sa.Uuid(), sa.ForeignKey("doctor_availability_slots.id"), nullable=False
        ),
        sa.Column("status", sa.String(24), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("created_by", sa.Uuid()),
        sa.Column("updated_by", sa.Uuid()),
        sa.Column("cancelled_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "status IN ('proposed','booked','checked-in','completed','cancelled','no-show')",
            name="ck_appointments_status",
        ),
    )
    op.create_index(
        "uq_appointments_active_slot",
        "appointments",
        ["slot_id"],
        unique=True,
        postgresql_where=sa.text("status IN ('proposed','booked','checked-in')"),
    )
    op.create_table(
        "appointment_status_history",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("appointment_id", sa.Uuid(), sa.ForeignKey("appointments.id"), nullable=False),
        sa.Column("previous_status", sa.String(24)),
        sa.Column("new_status", sa.String(24), nullable=False),
        sa.Column("changed_by_subject", sa.String(255), nullable=False),
        sa.Column("changed_by_role", sa.String(32), nullable=False),
        sa.Column("reason", sa.String(255)),
        sa.Column("changed_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "audit_events",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("event_type", sa.String(64), nullable=False),
        sa.Column("actor_subject", sa.String(255), nullable=False),
        sa.Column("actor_role", sa.String(32), nullable=False),
        sa.Column("resource_type", sa.String(64), nullable=False),
        sa.Column("resource_id", sa.Uuid()),
        sa.Column("result", sa.String(32), nullable=False),
        sa.Column("request_id", sa.String(64), nullable=False),
        sa.Column("source_ip", sa.String(64)),
        sa.Column("metadata", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_audit_events_type_created", "audit_events", ["event_type", "created_at"])


def downgrade() -> None:
    op.drop_table("audit_events")
    op.drop_table("appointment_status_history")
    op.drop_table("appointments")
    op.drop_table("doctor_availability_slots")
    op.drop_table("doctors")
    op.drop_table("patients")
    op.drop_table("users")
