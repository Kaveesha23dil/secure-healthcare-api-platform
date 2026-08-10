# Deployment hardening

These controls are a deployment baseline, not a claim of production readiness.

## TLS and credentials

Replace local self-signed certificates with trusted, monitored certificates. Encrypt client-to-gateway and gateway-to-backend traffic with hostname verification. Replace default WSO2 credentials, rotate service credentials, use short-lived identities where possible, and source secrets from a managed secret store.

## Network

```text
Internet -> Load Balancer / Ingress -> WSO2 API Gateway
  -> Private Network -> FastAPI -> Private PostgreSQL
```

Do not expose FastAPI or PostgreSQL directly to the internet. Restrict Publisher/Admin access, gateway egress, database ingress, and management interfaces. Signed backend assertions remain mandatory inside the private network.

## Database and WSO2

Use external PostgreSQL with encryption, backups, restore tests, a least-privilege application account, and reviewed migration gates. Prefer forward-compatible migrations. Use supported external WSO2 databases, separate management and gateway access where appropriate, back up configuration and API revisions, and never retain the default administrator password.

## Logging and monitoring

Centralize gateway, application, audit, and infrastructure logs. Mask tokens and credentials; never log patient-sensitive request bodies. Alert on API latency, HTTP 4xx/5xx, 429 responses, backend/database health, JWT validation failures, authorization denials, certificate expiry, and deployment failures.

## Backup, recovery, and secrets

Back up PostgreSQL, WSO2 configuration, exported API definitions, and deployment metadata; encrypt backups and test restoration. Never store secrets in Git, Docker images, OpenAPI YAML, README files, or client-side code. Inventory and rotate credentials after incidents.
