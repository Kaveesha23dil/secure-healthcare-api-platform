# FastAPI Backend

Secure, contract-first implementation of the fictional healthcare appointment API. Route handlers perform HTTP translation only; services own authorization, transactions, and business rules; repositories own SQLAlchemy access; PostgreSQL owns critical integrity constraints.

## Requirements and configuration

Use Python 3.12 and PostgreSQL 17. Copy `.env.example` to `.env` for local use and replace placeholder credentials. Never commit `.env`, tokens, keys, certificates, or real patient information. Production forbids debug mode and wildcard CORS.

## Local Python setup

```bash
cd backend
python -m venv .venv
.venv/Scripts/activate
python -m pip install -e ".[dev]"
alembic upgrade head
python -m app.db.seed
uvicorn app.main:app --reload
```

On Linux/macOS activate with `source .venv/bin/activate`.

## Docker setup

From the repository root:

```bash
docker compose up --build -d
docker compose exec api alembic upgrade head
docker compose exec api python -m app.db.seed
docker compose logs -f api
```

This Compose file is development-only. The database binds to loopback, the API waits for PostgreSQL health, and no production secrets are embedded.

## Migrations

```bash
alembic revision --autogenerate -m "create healthcare core tables"
alembic upgrade head
alembic downgrade -1
```

Review every generated migration. The checked-in initial migration creates all tables, constraints, indexes, and a partial unique active-slot booking index with a valid downgrade.

## Quality checks

```bash
ruff check .
ruff format --check .
mypy app
pytest
```

Tests override authentication with immutable fictional principals; no public endpoint lets a caller select a role. SQLite supports fast isolated tests, while PostgreSQL migration and concurrency checks validate database-specific behavior.

## Endpoints

- Swagger UI: <http://localhost:8000/docs>
- Generated schema: <http://localhost:8000/openapi.json>
- Liveness: <http://localhost:8000/health>
- Database readiness: <http://localhost:8000/ready>

The authored contract remains `../api-spec/healthcare-api.yaml`. `/ready` is the sole operational extension.

## Security notes

JWT verification uses configured JWKS keys and validates an algorithm allowlist, signature, issuer, audience, expiration, and required claims. Scopes are necessary but not sufficient: services also enforce role and patient ownership/doctor assignment. Inaccessible appointments return a safe `404`. Request IDs are validated/generated and propagated to RFC 9457 problem responses and structured logs. Authorization headers, appointment reasons, passwords, tokens, full contact details, and raw bodies are excluded from logs and audit metadata.

Booking locks the slot and relies on a PostgreSQL partial unique index so concurrent active bookings cannot both commit. Valid status transitions are explicit and terminal states cannot reopen.

WSO2 API Manager is not installed in this phase. Later it may provide gateway validation, throttling, publication, analytics, and version governance; backend authorization remains mandatory.

## Troubleshooting

- `401`: configure a reachable JWKS endpoint and a correctly issued bearer token, or use test dependency overrides.
- `403`: verify both scopes and role.
- `404` for an appointment may intentionally conceal failed ownership/assignment.
- `409`: inspect slot state, duplicate booking, or status transition.
- `/ready` failure: verify `DATABASE_URL`, PostgreSQL health, and migrations.
- Migration connection errors: start `db` and ensure local credentials match `.env`.
