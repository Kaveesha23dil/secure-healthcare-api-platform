# WSO2 Runtime Validation

Validation updated: 2026-08-28 (Asia/Colombo)

## Environment

| Item | Observed value |
|---|---|
| Operating system | Windows |
| WSO2 API Manager | 4.7.0.13 installed under `C:\Users\kavee\Downloads\wso2am-4.7.0.13` |
| Java | JDK 21.0.12 available and used for WSO2 certificate inspection |
| Python | 3.12.13 |
| Docker client/server | 29.2.0 / 29.2.0 |
| Installation mode | WSO2 installed directly on Windows; FastAPI and PostgreSQL run with Docker Compose |
| FastAPI endpoint used | `http://localhost:8000` |
| WSO2 backend endpoint | `http://localhost:8000` |
| Gateway URL | `https://localhost:8243` |
| API context/version | `/healthcare` / `1.0.0` |
| Invocation context | `/healthcare/1.0.0` |
| Backend JWT header | `X-JWT-Assertion` |

## Repository and runtime observations

- The WSO2 integration was merged into `main` by pull request 3, not into `develop`. `origin/develop` remained at the API-design merge. The validation branch was therefore fast-forwarded to `origin/main`; `develop` was not modified.
- A pre-existing uncommitted edit to `docs/authorization-matrix.md` was preserved and excluded from this validation work.
- Docker Compose defines services named `db` and `api`; the task brief's `database` service name does not exist.
- Docker Desktop initially took longer than 55 seconds to expose its Linux engine, but subsequently became ready.
- Default PostgreSQL host port 5432 was unavailable. Runtime validation used `POSTGRES_PORT=55432` and `API_PORT=18000` without changing committed configuration.
- WSO2 is installed outside the repository. Publisher and Developer Portal were accessible, the API was imported/deployed/published, an application was subscribed, and gateway OAuth behavior was manually validated.
- The WSO2 process was stopped during the final backend-JWT connectivity check. Consequently, Windows connection to port 8243 was refused and the API container could not reach the JWKS endpoint.
- The public certificate for the configured `wso2carbon` signing key is mounted read-only into the API container. No private key or access token is stored in the repository.

## Contract and security configuration reviewed

Configured OAuth scopes:

`doctor:read`, `doctor:write`, `availability:read`, `availability:write`, `appointment:create`, `appointment:read`, `appointment:read:all`, `appointment:update`, `appointment:cancel`, `patient:read`, `patient:write`, and `admin:manage`.

Configured roles: `patient`, `doctor`, and `administrator`. The role-to-scope mapping follows least privilege in `wso2/config/role-scope-mapping.yaml`.

The WSO2 OpenAPI contract uses context `/healthcare`, version `1.0.0`, exposes public `GET /health`, does not expose `/ready`, and does not append `/api/v1` to the backend base URL. Automated tests confirm that both OpenAPI files parse, references resolve, operation IDs are unique, operation paths match, and resource scopes match the mapping file.

FastAPI's `wso2_backend_jwt` mode accepts identity only from a cryptographically verified assertion in `X-JWT-Assertion`. It validates the configured signature algorithm, issuer, audience, expiry/not-before time, subject, role, and scope claims. Plain identity headers are ignored. Patient ownership, doctor assignment, and administrator authorization remain backend checks.

## JWT claims

Expected configurable claim names are `sub`, `roles`, and `scope`, with standard issuer, expiry, key identifier, and signing algorithm fields. Automated tests verify these mappings. WSO2's standard generator uses issuer `wso2.org/products/am`, does not emit `aud` by default, and publishes signing keys at the Classic Gateway super-tenant endpoint `https://<gateway-host>:8243/jwks`. Installation-specific claim mappings must still be confirmed from the local assertion without logging or storing the complete token.

## Test matrix

| Test | Expected | Actual | Status |
|---|---|---|---|
| Backend health | HTTP 200 | `GET http://localhost:8000/health` returned 200 | Passed |
| Backend readiness | HTTP 200 | Previously validated by the backend test suite | Passed |
| Swagger UI | HTTP 200 | Previously validated during backend runtime testing | Passed |
| Runtime OpenAPI | HTTP 200 | Previously validated during backend runtime testing | Passed |
| PostgreSQL connectivity | Healthy and migrations usable | Container healthy; Alembic used PostgreSQL | Passed |
| Static OpenAPI validation | Valid YAML, refs, IDs, paths, scopes | Covered by passing integration tests | Passed |
| API import | Resources imported; `/ready` absent | Imported in Publisher | Passed |
| Gateway deployment | Revision deployed | Deployed manually | Passed |
| API publication | Visible in Developer Portal | Published and visible | Passed |
| Application subscription | Application subscribed | Completed manually | Passed |
| Valid gateway health request | OAuth token accepted | Gateway health request returned 200 | Passed |
| Valid protected backend-JWT request | Gateway to FastAPI to PostgreSQL round trip | Pending final manual `GET /api/v1/doctors` test | Not run |
| Missing-token rejection | Gateway returns 401 | Manual gateway request returned 401 | Passed |
| Missing-scope rejection | Gateway/backend returns 403 | Manual token without `doctor:read` returned 403 | Passed |
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
| Pytest | Passed: 31 tests, including malformed, expired, invalid-signature, public-certificate, and endpoint authorization cases |
| Alembic upgrade | Passed against PostgreSQL |
| Alembic current | `20260801_0001 (head)` |
| Alembic heads | `20260801_0001 (head)` |
| API container | Running and healthy |
| PostgreSQL container | Running and healthy |

## Remaining manual work

1. Start WSO2 API Manager and wait for the `WSO2 Carbon started` message. It was stopped at the end of automated validation.
2. Confirm the installed `deployment.toml` enables `[apim.jwt]` with `enable = true`, `encoding = "base64url"`, `header = "X-JWT-Assertion"`, and `signing_algorithm = "SHA256withRSA"`.
3. In Developer Portal, generate a production token containing `doctor:read` and invoke `GET /api/v1/doctors` through `/healthcare/1.0.0`.
4. Confirm the response is HTTP 200, then inspect only safe backend log events (`backend_jwt_verified` or a rejection type). Do not log the assertion or decoded claims.

Gateway OAuth, missing-token, and missing-scope behavior have been validated. Full backend-JWT success is not yet claimed: the final protected request still needs to traverse WSO2 Gateway to FastAPI after WSO2 is restarted.
