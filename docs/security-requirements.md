# Security Requirements

Requirements use **MUST** for mandatory controls and **SHOULD** for recommended controls requiring an explicit exception if omitted.

## Identity and token validation

- Protected operations MUST validate JWT signature using an algorithm allowlist and a trusted JWKS source.
- The backend MUST validate issuer, audience, expiration, and not-before values and fail closed on malformed claims.
- Required OAuth scopes MUST be enforced at the gateway and rechecked or conveyed through a cryptographically trusted token to the backend.
- The backend MUST enforce role authorization and object ownership/assignment independently of scopes.
- Access tokens MUST be short-lived; refresh tokens MUST be protected, rotated when supported, and never sent to resource endpoints.
- Authorization Code with PKCE MUST be used for web/mobile users; Client Credentials is limited to trusted service identities. Resource Owner Password Credentials MUST NOT be used.
- Authentication failures MUST use generic messages that do not disclose account or token state.

## Input and API controls

- Unknown request properties MUST be rejected; server-managed fields cannot be mass assigned.
- UUID path parameters and ISO 8601 date-time values with timezone offsets MUST be schema validated.
- Request body sizes, header sizes, page size, query complexity, and processing time MUST be bounded.
- Gateway and application-layer rate limits MUST protect sensitive and resource-intensive operations.
- CORS MUST use an environment-specific allowlist; wildcard origins MUST NOT be used in production.
- Secure HTTP headers MUST be returned as appropriate, including `X-Content-Type-Options: nosniff`, a restrictive `Content-Security-Policy` for any documentation UI, `Referrer-Policy`, and HSTS on HTTPS production hosts.
- Sensitive values MUST NOT appear in URLs, query strings, errors, or logs.

## Transport, storage, and transactions

- HTTPS MUST protect all external communication and authenticated service communication.
- Sensitive data at rest MUST be encrypted using managed keys; secrets MUST be injected by environment/secret management and excluded from source control.
- Appointment writes MUST use database transactions.
- Double booking MUST be prevented by a database-enforced active-slot uniqueness rule, not only an application pre-check.
- Idempotency keys SHOULD protect retried appointment creation requests.

## Errors, logs, and monitoring

- APIs MUST return RFC 9457 `application/problem+json` errors and MUST NOT return stack traces to clients.
- Security-relevant events MUST produce structured audit records: authentication failure category, authorization denial, appointment lifecycle change, doctor/patient administration, policy/configuration change, and privileged data access.
- Audit logs and application logs MUST be separated and access-controlled; tokens and sensitive payloads MUST never be logged.
- Correlation and request IDs MUST support tracing without becoming trusted authorization inputs.

## Secure delivery

- Dependency and container scanning, static code analysis, secret scanning, and automated security tests MUST run in CI.
- Authorization tests MUST cover every role/operation pair and cross-tenant/ownership case.
- Contract validation MUST detect undocumented routes, unresolved references, insecure public operations, and response drift.
- Security findings rated high or critical MUST block release unless formally risk-accepted.

## Four authorization layers

1. **Authentication:** establishes who or what presented a valid token. It answers “who is calling?” but grants no business access by itself.
2. **Scope authorization:** checks whether the OAuth grant includes a coarse capability such as `appointment:read`.
3. **Role authorization:** checks whether the authenticated subject's trusted role may perform the function, such as restricting doctor creation to administrators.
4. **Object-level authorization:** checks the subject's relationship to the exact record, such as patient ownership or doctor assignment.

All four layers apply where relevant. A request with a valid token and scope is still denied if its role or object relationship is invalid.
