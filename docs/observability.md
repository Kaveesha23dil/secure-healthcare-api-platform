# Observability

FastAPI creates or validates an `X-Request-ID`, returns it on responses, and emits structured request completion/error logs with request ID, method, path, status, and duration. Domain services write audit events for appointment views and mutations, doctor mutations, and availability creation. Playwright verifies the response header through WSO2 when that environment is available and retains failure evidence.

An end-to-end correlation claim is valid only after WSO2 is configured to preserve or generate `X-Request-ID` and the same identifier is observed in gateway telemetry, FastAPI logs, and the relevant audit record. The repository does not implement a searchable log platform, Prometheus, Grafana, or OpenSearch.

Never log Authorization headers, cookies, passwords, OAuth codes/verifiers, appointment reasons, bodies, emails, or patient attributes. Restrict audit access and configure retention per environment. Alert on elevated 401/403/429/5xx rates, backend-JWT failures, audit write failures, abnormal conflicts, and correlation loss.
