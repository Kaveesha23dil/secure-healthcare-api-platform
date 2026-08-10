# Secure Healthcare API Platform

> **Current phase:** WSO2 API Manager integration assets and signed backend-JWT validation. Portal installation and runtime configuration remain manual.

## Problem statement

Healthcare APIs commonly suffer from inconsistent authentication, excessive permissions, missing rate limits, limited monitoring, weak lifecycle management, and accidental exposure of sensitive data. This educational project establishes a secure, contract-first foundation for a healthcare appointment API without using real patient information.

## Objective

Design an appointment platform where patients discover doctors and manage their own appointments, doctors manage appointments assigned to them, and administrators manage doctors, patients, schedules, and appointments. A future WSO2 API Manager layer will publish, secure, govern, version, rate-limit, document, and monitor the FastAPI backend.

## Proposed architecture

```mermaid
flowchart LR
    Client[Web or Mobile Client]
    WSO2[WSO2 API Manager]
    API[FastAPI Backend]
    DB[(PostgreSQL)]
    IDP[OAuth Identity Provider]

    Client --> WSO2
    WSO2 --> API
    API --> DB
    Client --> IDP
    IDP --> WSO2
```

The gateway validates JWTs and scopes; the backend independently enforces roles, ownership, and business rules. PostgreSQL is the authoritative data store. See [docs/architecture.md](docs/architecture.md) for trust boundaries and request flows.

## Roles

- **Patient:** views doctors and availability; creates, views, and cancels only their own appointments.
- **Doctor:** views assigned appointments and updates or cancels them when policy permits.
- **Administrator:** manages doctors, patients, schedules, and all appointments; accesses administrative reports.

Access is denied by default and granted according to least privilege. Gateway scope checks never replace backend object-level authorization.

## Planned technology stack

Python 3.12, FastAPI, SQLAlchemy, Alembic, PostgreSQL, Docker, WSO2 API Manager, OAuth 2.0, OpenID Connect, and JWT access tokens.

## MVP

- Authentication and OAuth scope protection
- Doctor directory and availability
- Patient appointment creation, viewing, and cancellation
- Doctor appointment management
- Administrative doctor, patient, schedule, and appointment management
- Rate limiting, API versioning, analytics, OpenAPI documentation, and security audit logging

## Excluded from version 1

Diagnoses, prescriptions, laboratory reports, insurance claims, video consultations, payments, medical document uploads, and all real patient data are excluded.

## Repository structure

```text
.
├── api-spec/                 # OpenAPI 3.0.3 contract
├── backend/                  # Future FastAPI implementation notes
├── database/                 # Planned relational schema
├── docs/                     # Architecture, security, and governance documents
├── tests/                    # Future test strategy
├── .env.example              # Non-secret development placeholders
├── docker-compose.yml        # Local PostgreSQL only
└── CONTRIBUTING.md           # Contribution and review policy
```

## Security principles

API-first and contract-first design, least privilege, deny by default, defense in depth, zero-trust assumptions, data minimization, secure-by-design and privacy-by-design practices. The design is informed by the OWASP API Security Top 10 and healthcare industry practices, but does **not** claim HIPAA, GDPR, or full HL7 FHIR compliance.

## Local development plan

1. Copy `.env.example` to `.env` and replace development placeholders locally.
2. Start the database and API with `docker compose up --build -d`.
3. Apply migrations with `docker compose exec api alembic upgrade head`.
4. Run backend quality checks from `backend/` with `ruff check .`, `mypy app`, and `pytest`.
5. Validate behavior against `api-spec/healthcare-api.yaml` before integrating WSO2.

WSO2 import assets, scope mappings, smoke tests, and manual setup instructions are in [`wso2/`](wso2/README.md). Gateway validation adds defense in depth; FastAPI continues enforcing verified scopes, roles, object ownership/assignment, and business rules.

## APIOps and CI/CD

Pull requests run Ruff, formatting, MyPy, Pytest, OpenAPI and breaking-change validation, secret checks, and a non-root Docker image build. Merges to `develop` can deploy through a WSO2 development self-hosted runner; staging is manually dispatched and protected by GitHub Environment approval. Production deployment is disabled and validation-only for this demo.

WSO2 `apictl` credentials come from environment secrets, while backend endpoints and generated API-project paths are environment parameters. See [`apiops/README.md`](apiops/README.md), [`apiops/docs/environment-promotion.md`](apiops/docs/environment-promotion.md), [`docs/github-environments.md`](docs/github-environments.md), and [`docs/deployment-hardening.md`](docs/deployment-hardening.md).

## Web client

The React/TypeScript client uses WSO2 Authorization Code with PKCE for patient, doctor, and administrator UX. Every protected API call targets the WSO2 Gateway; the browser never calls FastAPI directly. Start locally with `cd frontend`, `npm install`, and `npm run dev` after creating a non-secret `.env` from the example. See [`frontend/README.md`](frontend/README.md), [`docs/frontend-authentication.md`](docs/frontend-authentication.md), and [`docs/demo-scenarios.md`](docs/demo-scenarios.md).

## Roadmap

1. **Foundation (current):** scope, architecture, security design, schema plan, and OpenAPI contract.
2. **Backend (current):** FastAPI resources, migrations, authorization, concurrency controls, audit events, and automated tests.
3. **Gateway:** WSO2 publication, OAuth/OIDC integration, policies, throttling, versioning, and analytics.
4. **Hardening:** security testing, observability, operational runbooks, and controlled deprecation exercises.

## API documentation

The source of truth is [`api-spec/healthcare-api.yaml`](api-spec/healthcare-api.yaml). API conventions are defined in [`docs/api-conventions.md`](docs/api-conventions.md).

## Disclaimer

This is an educational project. All names, identifiers, contact details, and appointment examples are fictional. Never use real patient or clinical information.
