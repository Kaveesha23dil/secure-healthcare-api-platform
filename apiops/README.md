# APIOps

This directory contains repeatable validation, promotion, and WSO2 API Controller (`apictl`) deployment assets. Contracts remain environment-neutral; deployment-time parameters select the backend and WSO2 environment.

Start with `scripts/validate-api.ps1` (or `.sh`). Deployment requires an installed `apictl`, an exported API project, environment variables, and access to the target WSO2 control plane. Credentials belong in the process environment or CI environment secrets, never in this repository.

- `apictl/`: environment and API-project guidance
- `config/`: non-secret environment examples
- `scripts/`: validation, deployment, compatibility, and smoke-test entry points
- `docs/`: promotion and rollback runbooks

Production deployment is documentation-only for this student/demo project.
