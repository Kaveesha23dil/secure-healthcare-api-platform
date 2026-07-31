# Contributing

## Branches and commits

Create focused branches from an up-to-date `main`: `feature/*`, `fix/*`, `docs/*`, or `security/*`. Use Conventional Commit-style messages, for example:

```text
docs: define healthcare API scope
feat: add appointment creation endpoint
fix: prevent duplicate appointment booking
security: enforce appointment ownership validation
test: add authorization tests
```

## Pull requests

- Keep changes focused; explain purpose, security/privacy impact, contract changes, migration needs, and validation evidence.
- Link the relevant issue/decision and update OpenAPI and documentation with behavior changes.
- Obtain at least one independent code review; changes to authentication, authorization, sensitive data, gateway policy, logging, database constraints, or dependencies require an explicit security review.
- Resolve review feedback and pass required CI before merge. Do not self-approve protected changes.
- Prefer squash or project-approved merge strategy and preserve a meaningful audit trail.

## Security and secrets

- Never commit passwords, API keys, bearer/refresh tokens, private keys, certificates, production URLs containing credentials, or real patient data.
- Use fictional fixtures and `.env.example` placeholders. Store local secrets only in ignored files and managed secrets in deployed environments.
- Report suspected vulnerabilities privately to maintainers; do not disclose exploitable details in a public issue.

## Tests and documentation

- Add unit/integration/contract tests for behavior changes and authorization tests for positive and negative role, scope, ownership, and assignment cases.
- Booking changes require concurrency and transaction tests; errors/logging changes require sensitive-data leakage tests.
- Run formatting, linting, type checks, dependency/secret/static analysis, OpenAPI validation, and applicable tests.
- Update the OpenAPI contract, diagrams, matrix, threat model, database plan, README, and operational guidance whenever their assumptions change.
