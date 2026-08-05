# WSO2 Runtime Validation

Validation date: 2026-08-05 (Asia/Colombo)

## Environment

| Item | Observed value |
|---|---|
| Operating system | Windows |
| WSO2 API Manager | 4.7.0 selected for a future local installation; runtime not installed |
| Java | OpenJDK Corretto 17.0.19; `JAVA_HOME` is unset |
| Required Java for selected release | JDK 21, according to the current WSO2 installation documentation |
| Python | 3.12.13 |
| Docker client/server | 29.2.0 / 29.2.0 |
| Installation mode | Planned Option A: WSO2 installed directly on Windows |
| FastAPI endpoint used | `http://localhost:18000` (local validation override because port 8000/5432 startup used conflicting defaults) |
| Planned WSO2 backend endpoint | `http://localhost:18000` for this validation session; use `http://localhost:8000` when the default API port is available |
| Planned gateway URL | `https://localhost:8243` |
| API context/version | `/healthcare` / `1.0.0` |
| Invocation context | `/healthcare/1.0.0` |
| Backend JWT header | `X-JWT-Assertion` |

## Repository and runtime observations

- The WSO2 integration was merged into `main` by pull request 3, not into `develop`. `origin/develop` remained at the API-design merge. The validation branch was therefore fast-forwarded to `origin/main`; `develop` was not modified.
- A pre-existing uncommitted edit to `docs/authorization-matrix.md` was preserved and excluded from this validation work.
- Docker Compose defines services named `db` and `api`; the task brief's `database` service name does not exist.
- Docker Desktop initially took longer than 55 seconds to expose its Linux engine, but subsequently became ready.
- Default PostgreSQL host port 5432 was unavailable. Runtime validation used `POSTGRES_PORT=55432` and `API_PORT=18000` without changing committed configuration.
- No WSO2 distribution was found at `C:\wso2` or a top-level `C:\wso2am-*` directory.
- No local `.env`, access token, consumer secret, private key, certificate, WSO2 binary distribution, or WSO2 runtime log was found in the repository by the targeted scan.

## Contract and security configuration reviewed

Configured OAuth scopes:

`doctor:read`, `doctor:write`, `availability:read`, `availability:write`, `appointment:create`, `appointment:read`, `appointment:read:all`, `appointment:update`, `appointment:cancel`, `patient:read`, `patient:write`, and `admin:manage`.

Configured roles: `patient`, `doctor`, and `administrator`. The role-to-scope mapping follows least privilege in `wso2/config/role-scope-mapping.yaml`.

The WSO2 OpenAPI contract uses context `/healthcare`, version `1.0.0`, exposes public `GET /health`, does not expose `/ready`, and does not append `/api/v1` to the backend base URL. Automated tests confirm that both OpenAPI files parse, references resolve, operation IDs are unique, operation paths match, and resource scopes match the mapping file.

FastAPI's `wso2_backend_jwt` mode accepts identity only from a cryptographically verified assertion in `X-JWT-Assertion`. It validates the configured signature algorithm, issuer, audience, expiry/not-before time, subject, role, and scope claims. Plain identity headers are ignored. Patient ownership, doctor assignment, and administrator authorization remain backend checks.

## JWT claims

Expected configurable claim names are `sub`, `roles`, and `scope`, with standard issuer, audience, expiry, key identifier, and signing algorithm fields. These names were verified in automated tests only. They were **not confirmed against a real WSO2 4.7.0 assertion**, because no WSO2 runtime or assertion was available. Installation-specific values for issuer, audience, and JWKS URL must not be guessed.

## Test matrix

| Test | Expected | Actual | Status |
|---|---|---|---|
| Backend health | HTTP 200 | `GET http://localhost:18000/health` returned 200 | Passed |
| Backend readiness | HTTP 200 | `GET http://localhost:18000/ready` returned 200 | Passed |
| Swagger UI | HTTP 200 | `GET http://localhost:18000/docs` returned 200 | Passed |
| Runtime OpenAPI | HTTP 200 | `GET http://localhost:18000/openapi.json` returned 200 | Passed |
| PostgreSQL connectivity | Healthy and migrations usable | Container healthy; Alembic used PostgreSQL | Passed |
| Static OpenAPI validation | Valid YAML, refs, IDs, paths, scopes | Covered by passing integration tests | Passed |
| API import | Resources imported; `/ready` absent | Publisher unavailable because WSO2 is not installed | Blocked |
| Gateway deployment | Revision deployed | WSO2 runtime unavailable | Blocked |
| API publication | Visible in Developer Portal | WSO2 runtime unavailable | Blocked |
| Application subscription | `HealthcareWebApp` subscribed | WSO2 runtime unavailable | Blocked |
| Valid gateway request | Gateway to FastAPI to PostgreSQL round trip | No gateway or OAuth token available | Not run |
| Missing-token rejection | Gateway returns 401 | Automated FastAPI assertion-header test passes; real gateway test not run | Blocked |
| Missing-scope rejection | Gateway/backend returns 403 | Scope enforcement covered by automated tests; real gateway test not run | Blocked |
| Patient ownership rejection | Concealed 404 | Backend automated authorization tests pass; real gateway test not run | Blocked |
| Doctor assignment rejection | 404 or contract-defined 403 | Backend automated authorization tests pass; real gateway test not run | Blocked |
| Administrator authorization | Patient receives 403 | Backend automated authorization tests pass; real gateway test not run | Blocked |
| Forged-header rejection | Headers ignored | Automated WSO2 security test passes; real gateway test not run | Blocked |
| Rate-limit rejection | HTTP 429 | WSO2 throttling policy unavailable | Not run |

## Quality results

| Check | Result |
|---|---|
| Ruff | Passed: all checks passed |
| Ruff formatting | Passed: 69 files already formatted |
| MyPy | Passed: no issues in 52 source files |
| Pytest | Passed: 28 tests; 2 warnings |
| Alembic upgrade | Passed against PostgreSQL |
| Alembic current | `20260801_0001 (head)` |
| Alembic heads | `20260801_0001 (head)` |
| API container | Running and healthy |
| PostgreSQL container | Running and healthy |

## Remaining manual work

1. Install JDK 21 and set `JAVA_HOME` without removing the existing Java installation.
2. Download the WSO2 API Manager 4.7.0 all-in-one ZIP from the official WSO2 download page and extract it to a short external path such as `C:\wso2\wso2am-4.7.0`. Do not place it in this repository.
3. Confirm `<WSO2_HOME>\bin`, `<WSO2_HOME>\repository\conf`, and `<WSO2_HOME>\repository\logs` exist. Open PowerShell in `<WSO2_HOME>\bin` and run `.\api-manager.bat --run`; wait for the `WSO2 Carbon started` message and keep that terminal open.
4. Verify Publisher, Developer, and Admin portals over local TLS. Preserve the default `deployment.toml` before changes.
5. Import `wso2/api/healthcare-api-wso2.yaml`; configure scopes, fictional roles/users, operation mappings, and demonstration throttling policies.
6. Configure the exact WSO2 4.7.0 backend-JWT properties using official version-specific documentation. Confirm assertion issuer, audience, JWKS URL, claim names, `kid`, and algorithm without recording the complete assertion.
7. Deploy and publish a revision, create and subscribe `HealthcareWebApp`, generate a temporary token into `WSO2_ACCESS_TOKEN`, and run the gateway/security/rate-limit scripts.

No end-to-end WSO2 success is claimed. A real request has not yet traversed client to WSO2 Gateway to FastAPI to PostgreSQL and back.
