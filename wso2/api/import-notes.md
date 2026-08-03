# Import Notes

Import `healthcare-api-wso2.yaml` through Publisher Portal, set context to `/healthcare`, version to `1.0.0`, and confirm the resulting invocation context is `/healthcare/1.0.0` for the selected APIM deployment. The selected WSO2 version is not pinned, so portal-managed endpoints, throttling, backend JWT, and lifecycle settings are intentionally preferred over speculative vendor extensions.

The placeholder backend is `http://host.docker.internal:8000`. `localhost` works only when WSO2 and FastAPI share a host namespace. Use `host.docker.internal` for WSO2-in-Docker to host FastAPI, or the Compose service name such as `http://api:8000` when both share a Docker network.

The imported resource path already contains `/api/v1`; do not add `/api/v1` to the backend endpoint or the result will be duplicated. `/ready` is deliberately absent and must remain private.
