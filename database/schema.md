# Planned Database Schema

PostgreSQL will use UUID primary keys (`uuid`, generated server-side), `timestamptz` for instants, UTC semantics, foreign-key integrity, parameterized access through SQLAlchemy, and Alembic migrations. Patient-sensitive attributes live only in `patients` unless a justified immutable snapshot is required.

Common auditable tables include `created_at timestamptz`, `updated_at timestamptz`, `created_by uuid`, and `updated_by uuid`; actor references may be nullable for controlled system actions. Mutable master records use `deleted_at timestamptz` for soft deletion where noted.

## Tables

### `users`

- **PK:** `id uuid`
- **Columns:** `external_subject varchar(255)`, `role varchar(32)`, `status varchar(32)`, common audit fields, `deleted_at`
- **Constraints:** unique `external_subject`; role/status check constraints
- **Indexes:** active users by role/status; unique subject index
- **Strategy:** soft-delete/disable to preserve audit relationships; do not store passwords or tokens

### `patients`

- **PK:** `id uuid`
- **FK:** `user_id -> users.id` (unique), audit actors -> `users.id`
- **Columns:** fictional `display_name`, `email`, `phone`, common audit fields, `deleted_at`
- **Constraints:** normalized email uniqueness if required; one patient per user
- **Indexes:** `user_id`, normalized email (restricted operational use)
- **Strategy:** soft delete/anonymize under retention policy; contact fields encrypted at rest; do not duplicate them in appointments

### `doctors`

- **PK:** `id uuid`
- **FK:** optional `user_id -> users.id` (unique), audit actors -> `users.id`
- **Columns:** `display_name`, `specialization`, `clinic_name`, `active boolean`, common audit fields, `deleted_at`
- **Constraints:** one linked user per doctor when linked
- **Indexes:** active specialization/display name; `user_id`
- **Strategy:** soft delete/deactivate to retain appointment history

### `doctor_availability_slots`

- **PK:** `id uuid`
- **FK:** `doctor_id -> doctors.id`, audit actors -> `users.id`
- **Columns:** `start_at timestamptz`, `end_at timestamptz`, `status varchar(24)`, common audit fields, `deleted_at`
- **Constraints:** `end_at > start_at`; unique `(doctor_id, start_at, end_at)` for non-deleted slots; allowed status values
- **Indexes:** `(doctor_id, start_at)` filtered to active future slots; `status`
- **Strategy:** cancel/soft-delete instead of removing referenced slots

### `appointments`

- **PK:** `id uuid`
- **FK:** `patient_id -> patients.id`, `doctor_id -> doctors.id`, `slot_id -> doctor_availability_slots.id`, audit actors -> `users.id`
- **Columns:** `reason text` (sensitive and length-limited), `status varchar(24)`, `version integer`, common audit fields
- **Constraints:** status in `proposed`, `booked`, `checked-in`, `completed`, `cancelled`, `no-show`; doctor must correspond to slot (enforced with a composite FK or trigger); version positive
- **Indexes:** `(patient_id, created_at desc)`, `(doctor_id, created_at desc)`, `(doctor_id, status, created_at)`, `slot_id`
- **Strategy:** lifecycle/status retention rather than ordinary deletion

**Double-booking prevention:** create a partial unique index such as:

```sql
CREATE UNIQUE INDEX uq_appointments_active_slot
ON appointments (slot_id)
WHERE status IN ('proposed', 'booked', 'checked-in');
```

Creation runs in one transaction, optionally locks the slot row, inserts the appointment and status history, and maps a unique-constraint violation to `409`. Application-only availability checks are insufficient.

### `appointment_status_history`

- **PK:** `id uuid`
- **FK:** `appointment_id -> appointments.id`, `changed_by -> users.id`
- **Columns:** `from_status`, `to_status`, `changed_at timestamptz`, `reason_code`, optional sanitized note
- **Constraints:** valid statuses and transition; immutable after insert
- **Indexes:** `(appointment_id, changed_at)`, `changed_by`
- **Audit fields:** `created_at`, `created_by`; no update fields because rows are append-only
- **Strategy:** no soft delete; retain according to appointment audit policy

### `audit_events`

- **PK:** `id uuid`
- **FK:** optional `actor_user_id -> users.id`
- **Columns:** `occurred_at timestamptz`, `event_type`, `outcome`, `actor_subject_hash`, `target_type`, `target_id uuid`, `trace_id uuid`, `request_id uuid`, `source`, sanitized `metadata jsonb`
- **Constraints:** required event type/outcome/time; append-only permissions
- **Indexes:** `(occurred_at)`, `(event_type, occurred_at)`, `(actor_user_id, occurred_at)`, `trace_id`, `(target_type, target_id)`
- **Strategy:** no soft delete; partition/expire by approved audit retention; metadata schema forbids secrets and sensitive payloads

## Integrity and lifecycle notes

- Foreign keys use restrictive deletes for historical data; soft-deleted actors remain referentially available.
- State transitions are validated by application policy inside the same transaction and recorded in history.
- Optimistic `version` checks prevent lost updates; the unique slot index prevents booking races.
- Database users are separated for migrations and runtime; runtime has no schema-owner rights.
- Backups inherit sensitive-data classification, encryption, access, and deletion requirements.
