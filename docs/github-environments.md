# GitHub environments

Create `development`, `staging`, and `production` under repository Settings > Environments. Internal WSO2 deployments require self-hosted runners labeled `wso2-development` or `wso2-staging`; GitHub-hosted runners cannot reach a developer's `localhost` or private network.

Development secrets: `WSO2_DEV_USERNAME`, `WSO2_DEV_PASSWORD`, `WSO2_DEV_HOST`, `WSO2_DEV_GATEWAY_URL`, and `WSO2_DEV_ACCESS_TOKEN`.

Staging secrets: `WSO2_STAGING_USERNAME`, `WSO2_STAGING_PASSWORD`, `WSO2_STAGING_HOST`, `WSO2_STAGING_GATEWAY_URL`, and `WSO2_STAGING_ACCESS_TOKEN`.

Set non-secret environment variables `BACKEND_URL`, `APICTL_API_PROJECT`, and `APICTL_PARAMS_FILE` as GitHub environment variables. Protect staging with required reviewers and restricted branches. Production must require manual reviewers if ever enabled; its workflow currently validates only.

Secrets belong in GitHub Environment secrets or an external secret manager. Rotate leaked credentials immediately: deleting them from a later commit does not invalidate prior exposure.
