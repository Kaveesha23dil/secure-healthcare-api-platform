# Project Scope

## Problem statement

Healthcare APIs can suffer from inconsistent authentication, excessive permissions, missing rate limits, poor monitoring, weak API lifecycle management, and sensitive-data exposure.

## Project objective

Demonstrate how WSO2 API Manager can securely expose, govern, monitor, version, document, and rate-limit healthcare APIs while a FastAPI backend retains responsibility for role, ownership, and business-rule enforcement.

## MVP features

- User authentication
- Doctor directory and doctor availability
- Appointment creation, viewing, and cancellation
- Doctor appointment management
- Administrative doctor management
- OAuth scope protection and rate limiting
- API versioning, analytics, and OpenAPI documentation
- Security audit logging

## Out of scope for version 1

- Medical diagnoses, prescriptions, and laboratory reports
- Insurance claims, payment processing, and video consultations
- Medical document uploads
- Real patient data

## Roles and boundaries

### Patient

May view doctors and availability and create, view, or cancel only their own appointments. A patient may not view another patient's appointments, update clinical or administrative data, or manage doctors.

### Doctor

May view doctor information, view appointments assigned to them, update assigned appointment statuses, and cancel an assigned appointment when policy permits. A doctor may not view another doctor's appointments, manage users, or create/delete doctors.

### Administrator

May manage doctors, patient accounts, schedules, availability, and all appointments, and access administrative reports.

All access follows least privilege and deny-by-default rules.

## Assumptions

- OAuth/OIDC identities contain a stable subject, role claims, and approved scopes.
- WSO2 or an external identity provider will issue/validate tokens in a later phase.
- Dates are stored in UTC and exposed as ISO 8601 values with offsets.
- Availability slots have fixed start/end instants and belong to one doctor.
- FHIR concepts may inspire terminology, but the API is not FHIR compliant.

## Dependencies

- Python 3.12, FastAPI, SQLAlchemy, and Alembic
- PostgreSQL and Docker
- WSO2 API Manager and a compatible OAuth 2.0/OpenID Connect identity provider
- CI tooling for linting, contract validation, dependency scanning, and security tests

## Constraints

- No real patient data or secrets in source control, logs, examples, or fixtures.
- This phase produces no backend implementation and performs no WSO2 installation.
- Gateway authorization cannot substitute for backend ownership checks.
- APIs must remain backward-compatible within a major version or follow the deprecation policy.

## Success criteria

- The OpenAPI 3.0.3 contract parses and all local references resolve.
- Public and protected operations and required OAuth scopes are unambiguous.
- The authorization matrix covers patient, doctor, and administrator operations.
- Threats have mitigations and verifiable tests.
- The database plan prevents two active bookings for one slot.
- Documentation is sufficient to begin FastAPI implementation without redefining core policies.

## Non-functional requirements

- **Security:** HTTPS, short-lived tokens, least privilege, input validation, secure errors, and audit events.
- **Privacy:** data minimization, masking, retention limits, and fictional test data only.
- **Reliability:** transactional writes, idempotency support, concurrency protection, and health checks.
- **Performance:** pagination, bounded page sizes, indexed lookup paths, and gateway rate limits.
- **Observability:** correlation/request IDs, structured application logs, separate audit logs, and metrics without sensitive content.
- **Maintainability:** contract-first changes, versioned migrations, automated tests, and documented decisions.
- **Availability:** stateless API instances and managed database recovery are future deployment goals; no SLA is claimed.
