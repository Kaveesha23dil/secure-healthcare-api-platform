# Rollback strategy

## Application

Redeploy the previous immutable, vulnerability-reviewed Docker image tag. Verify `/health`, `/ready`, database connectivity, and an authorized gateway request before restoring traffic.

## WSO2 API

Restore and deploy the previous known-good WSO2 API revision. Confirm context, scopes, subscriptions, endpoint, throttling, backend JWT, and a smoke request. Keep exported API projects and revision identifiers as controlled artifacts.

## Database

Prefer a forward fix in production. Run a downgrade only when it is explicitly implemented, tested on a restored backup, and proven non-destructive. Never blindly downgrade a destructive migration.

## Contracts

Do not remove v1 while consumers depend on it. Publish v2 for breaking changes and use a measured deprecation window. After rollback, compare the active OpenAPI contract, inspect 4xx/5xx/429 rates, verify audit logging, and record the incident and recovery evidence.
