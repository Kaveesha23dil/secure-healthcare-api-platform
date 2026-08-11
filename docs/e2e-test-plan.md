# End-to-end test plan

## Objectives

Validate browser authentication, role routing, gateway-only API access, backend object authorization, appointment integrity, safe throttling behavior, request IDs, and failure evidence without weakening production controls.

## Environments and identities

`@ci` tests use the local Vite server and do not authenticate. `@wso2` tests require the private WSO2/FastAPI/PostgreSQL stack, the published `/healthcare/1.0.0` API, and fictional patient-one, patient-two, doctor-one, doctor-two, administrator, and limited-scope identities. Credentials exist only in local environment variables or protected GitHub Environment secrets.

## Scenarios

| Area | Automated intent | Requirement |
|---|---|---|
| Authentication | Protected redirect; real WSO2 login for each role; role-route denial | WSO2 and credentials |
| Patient | Browse doctors, book without `patientId`, view and cancel | Seeded doctor/available slot |
| Isolation | Patient and doctor cross-object reads return safe `404` | Fictional cross-owned IDs |
| Doctor | Load assigned reference and expose only valid transitions | Assigned ID; list API is absent |
| Administrator | View appointment/patient summaries; create fictional doctor | Administrator identity |
| Gateway | No direct FastAPI browser calls; missing token and forged headers denied | WSO2 |
| Integrity | Duplicate booking conflict; concurrent booking | Shared deterministic slot needed for concurrency E2E |
| Throttling | Conservative, opt-in `429` check and safe UI message | Isolated low-quota policy |
| Observability | `X-Request-ID`, safe problem responses, retained evidence | Gateway header propagation |

All mutations use fictional data. The suite is serial to reduce shared-state races. Failure artifacts are HTML/JUnit reports, screenshots, first-retry traces, and retained videos.
