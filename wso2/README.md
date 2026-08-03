# WSO2 API Manager Integration

These assets prepare the fictional healthcare API for WSO2 API Manager (APIM). They do not install APIM, create users/keys, or modify a runtime. Exact portal labels and `deployment.toml` keys vary by APIM version; verify them in that version's official documentation.

## Target flow and security boundary

```text
Client OAuth token -> WSO2 token/subscription/scope/rate validation
  -> signed X-JWT-Assertion -> FastAPI signature/claim/scope/role/object checks
  -> PostgreSQL constraints -> response through WSO2
```

WSO2 must strip any client `X-JWT-Assertion` and generate its own signed assertion. FastAPI ignores `X-User-ID`, `X-Patient-ID`, `X-Doctor-ID`, `X-Role`, and `X-Scopes`. Source-IP restrictions are defense in depth only; the signed assertion is mandatory.

## Manual setup checklist

These steps require a local runtime, portal access, administrator credentials, OAuth key generation, and local certificates and cannot be completed by this repository alone.

1. Select an APIM release and install the JDK version listed in that release's installation prerequisites.
2. Download and unpack WSO2 APIM from WSO2. Do not place the distribution in this repository.
3. Start APIM using its documented platform script and wait for Publisher, Developer, and Admin portals.
4. Open Publisher Portal, normally `https://localhost:9443/publisher`, and sign in as an authorized administrator.
5. Import `api/healthcare-api-wso2.yaml` as an OpenAPI API.
6. Set name `Secure Healthcare API`, context `/healthcare`, and version `1.0.0`.
7. Set the backend endpoint for the topology: `http://localhost:8000`, `http://host.docker.internal:8000`, or `http://api:8000`. Do not append `/api/v1`.
8. Review every imported resource and confirm `/ready` is absent and `/health` is unauthenticated.
9. Create the local scopes in `config/scopes.yaml`; names are case-sensitive for this project.
10. Map scopes to roles according to `config/role-scope-mapping.yaml` and the configured user store.
11. Attach operation scopes using `config/api-resource-scope-mapping.yaml`; administrator operations still require backend role plus `admin:manage`.
12. Create operation/application throttling policies corresponding to `config/rate-limits.yaml`. Values are demonstration-only.
13. Confirm the installed APIM version's backend JWT feature and property names, then adapt `config/deployment.toml.example` in the external APIM installation.
14. Configure APIM to overwrite/remove client `X-JWT-Assertion`, sign a short-lived backend assertion, and include the agreed subject, roles, scopes, issuer, audience, expiry, and key ID.
15. Make APIM signing keys discoverable at the configured JWKS URL and plan overlapping key rotation.
16. Restart APIM after runtime configuration changes and verify logs contain no tokens/assertions or sensitive bodies.
17. Create clearly fictional patient, doctor, and administrator identities and map their case-sensitive roles.
18. Create and deploy a new API revision to the local gateway environment.
19. Publish the API and open Developer Portal, normally `https://localhost:9443/devportal`.
20. Create `HealthcareWebApp`, subscribe it to the API, and choose only the needed subscription tier.
21. Generate OAuth keys using Authorization Code with PKCE for user clients; never save the client secret here.
22. Obtain a temporary test access token with the required scopes and export it as `WSO2_ACCESS_TOKEN`.
23. Run `scripts/gateway-smoke-test.ps1` or `.sh`; then exercise expected `401`, `403`, concealed `404`, and—only in a controlled environment—`429` behavior.
24. Review gateway analytics, application/audit logs, and FastAPI logs for request correlation and sensitive-data redaction.

## Backend modes

- `AUTH_MODE=direct_jwt`: local/direct bearer validation, retained for controlled backend development.
- `AUTH_MODE=wso2_backend_jwt`: reads only the configured signed assertion header for protected routes.
- `AUTH_MODE=test_override`: rejected unless `APP_ENV=test`, and still requires a FastAPI dependency override.

For local host access set `ALLOW_DIRECT_ACCESS=true`. For a gateway-only environment keep it `false`, set `TRUSTED_GATEWAY_HOSTS`, and enforce private routing with firewall rules, security groups, a Docker internal network, or Kubernetes NetworkPolicy. Do not enable proxy-header trust unless the proxy chain is controlled.

## Smoke tests

```powershell
./scripts/check-backend.ps1
$env:WSO2_ACCESS_TOKEN="temporary-token-not-saved"
$env:ALLOW_INSECURE_LOCAL_TLS="true" # local self-signed certificate only
./scripts/gateway-smoke-test.ps1
```

Rate-limit testing additionally requires `CONFIRM_RATE_LIMIT_TEST=true` and uses only `GET /api/v1/doctors`. It must never run against production.

## Connectivity troubleshooting

- WSO2 in Docker cannot reach host FastAPI through its own `localhost`; use `host.docker.internal`.
- Services on one Compose network should use `http://api:8000` without publishing the API port.
- A `401` from FastAPI indicates a missing/invalid backend assertion, claim mismatch, algorithm mismatch, or JWKS failure.
- A `403` indicates the verified assertion lacks a required scope or role.
- A safe `404` can intentionally conceal ownership or doctor-assignment failure.
- Confirm clock synchronization, issuer/audience spelling, `kid`, JWKS reachability, TLS trust, and gateway header overwrite behavior.
- Never “fix” connectivity by trusting plain identity headers or disabling cryptographic validation.

No end-to-end WSO2 gateway claim is valid until a real request successfully traverses WSO2, FastAPI, PostgreSQL, and back.
