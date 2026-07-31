# Threat Model

## Method and scope

This preliminary model combines STRIDE reasoning with OWASP API Security risks. Assets include identities and tokens, appointment and patient data, doctor schedules, availability, audit evidence, the API contract, and service capacity. Trust boundaries exist at the client, identity provider, future WSO2 gateway, FastAPI service, and PostgreSQL database. Ratings are qualitative and must be revisited as implementation and deployment details become known.

| Threat | Description and example attack | Affected asset | Likelihood | Impact | Risk | Planned mitigation | Verification/testing |
|---|---|---|:---:|:---:|:---:|---|---|
| Broken object-level authorization (BOLA) | A patient changes `appointmentId` in `GET /api/v1/appointments/{appointmentId}` to read another patient's appointment. | Patient privacy, appointments | High | High | Critical | Derive subject from verified JWT; ownership/assignment query predicates; safe `404`; deny by default | Automated tests using patient A's token against patient B's ID; query-policy review |
| Broken function-level authorization | A patient calls `POST /api/v1/doctors` or an admin listing endpoint. | Administrative integrity | Medium | High | High | Gateway scopes plus backend role checks; separate admin routes; default deny | Role/scope matrix tests for every operation |
| Broken authentication | Forged, expired, wrong-issuer, or wrong-audience JWT is accepted. | All protected assets | Medium | High | High | Verify signature, algorithm allowlist, issuer, audience, expiry, and key rotation; fail closed | Negative JWT suite and identity-provider integration tests |
| Excessive data exposure | Doctor listing accidentally serializes patient contacts or internal fields. | Sensitive/internal data | Medium | High | High | Explicit response DTOs; field allowlists; classification review; no ORM serialization | Contract/schema assertions and snapshot tests |
| Mass assignment | Client adds `patientId`, `status`, or audit fields to an appointment request. | Ownership and record integrity | High | High | Critical | `additionalProperties: false`; separate request models; reject unknown fields; server-owned identity/audit values | Fuzz requests with forbidden properties; expect `422` |
| Resource exhaustion | Large bodies, expensive filters, or repeated requests exhaust API/database capacity. | Availability | High | Medium | High | Body/time limits, bounded pagination, indexed queries, timeouts, concurrency limits | Load and boundary testing; observe saturation metrics |
| Unrestricted resource consumption | Automated clients create excessive appointments or enumerate data. | Capacity, appointment inventory | High | High | Critical | Per-client/user/IP quotas, rate limits, pagination maximum, anomaly monitoring | Verify `429`, quota isolation, and retry headers |
| Sensitive-data leakage | Tokens, appointment reasons, emails, or phone numbers appear in errors/logs. | Confidentiality | Medium | High | High | Redaction, separate audit/app logs, generic errors, no stack traces, log field allowlist | Log-capture tests and secret scanning |
| Access-token theft | Token is stolen from insecure storage, transport, browser logs, or telemetry. | Identity and data | Medium | High | High | HTTPS, short lifetimes, secure storage, PKCE, no token logging, refresh-token rotation/protection | Transport/config review; client security test; token leak exercise |
| Token replay | Captured bearer token is reused until expiry. | Identity and data | Medium | High | High | Short-lived audience-bound tokens, TLS, revocation/rotation where supported, anomaly detection; consider sender constraints later | Replay simulation and alert verification |
| Duplicate appointment booking | Concurrent requests book the same slot. | Scheduling integrity | High | High | Critical | Transaction plus database partial unique index/slot lock; idempotency key; conflict response | Parallel integration test; expect one success and one `409` |
| Injection attacks | Crafted filters, reasons, IDs, or headers alter SQL/log behavior. | Database, logs, service | Medium | High | High | Parameterized ORM queries, schema validation, log encoding, no dynamic SQL | SAST, SQL injection tests, fuzzing |
| Improper asset management | Old or undocumented endpoints remain reachable outside the contract. | Data and attack surface | Medium | High | High | API inventory, contract-based routing, gateway catalog, CI drift checks | Compare deployed routes with OpenAPI and gateway inventory |
| Unsafe API version deprecation | `/api/v1` is removed without notice or old vulnerable versions remain indefinitely. | Availability/security | Medium | Medium | Medium | Published lifecycle, sunset headers, migration window, usage monitoring, explicit shutdown approval | Deprecation rehearsal and consumer inventory review |
| Security misconfiguration | Wildcard CORS, debug mode, weak headers, default credentials, or public database port. | Entire platform | Medium | High | High | Hardened environment defaults, configuration validation, IaC review, secure headers, secret management | DAST/config scans and deployment policy tests |
| Insufficient logging and monitoring | Authorization failures, admin changes, or booking abuse are not detected. | Auditability, response capability | Medium | High | High | Structured tamper-resistant audit events, correlation IDs, alert rules, retention/access controls | Generate events and test completeness, alerts, and trace correlation |

## Critical BOLA scenario

1. Fictional patient A legitimately retrieves appointment `11111111-1111-4111-8111-111111111111`.
2. The client replaces it with patient B's appointment ID in the URL.
3. The gateway sees a valid `appointment:read` scope but does not know record ownership.
4. FastAPI must query using both the appointment ID and the verified token subject's patient identity.
5. If the relationship is absent, it returns the same safe `404` used for a nonexistent record and emits a sanitized authorization-denial audit event.

Never reveal whether the inaccessible appointment exists.

## Review cadence

Review this model when endpoints, claims, data classifications, deployment topology, dependencies, gateway policies, or database constraints change, and before each production-like release.
