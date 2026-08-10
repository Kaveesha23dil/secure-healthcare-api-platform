# WSO2 API Controller

Install the `apictl` release compatible with the target WSO2 API Manager. Keep its binary and credential store outside Git. Example control-plane registrations:

```bash
apictl add env development --apim https://localhost:9443
apictl add env staging --apim https://wso2-staging.example.internal
apictl add env production --apim https://wso2-production.example.internal
apictl login development -u "$WSO2_USERNAME" -p "$WSO2_PASSWORD"
apictl get apis -e development
apictl export api -n SecureHealthcareAPI -v 1.0.0 -r admin -e development
apictl import api -f "$APICTL_API_PROJECT" -e development --update
```

Never put passwords on a shared command line or in shell history. The deployment scripts pass credentials from environment variables and do not print them. Prefer runner-supported secure input or an external secret manager where available.

The checked-in `api-project/` directory is documentation-only. Populate an API project by exporting a known-good API or using the version-compatible `apictl` project-generation workflow. Set `APICTL_API_PROJECT` to that generated directory/archive and, when needed, `APICTL_PARAMS_FILE` to a version-compatible environment parameter file kept outside Git.

`https://localhost:9443` is local-only. Staging and production must use reachable internal DNS names and trusted TLS certificates.
