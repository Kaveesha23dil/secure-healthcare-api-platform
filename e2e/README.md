# Playwright end-to-end tests

The Chromium suite exercises the React client through real WSO2 authentication and gateway routing. It never introduces test-login endpoints, role selectors, stored tokens, or real patient data.

1. Copy `.env.example` to `.env` and set the WSO2 public client, URLs, and fictional test identities.
2. Configure the WSO2 callback as `http://127.0.0.1:5173/auth/callback` and assign the documented scopes/roles.
3. Run `npm ci`, `npx playwright install chromium`, then `npm test` for CI-safe checks.
4. With WSO2, PostgreSQL, FastAPI, and the published gateway API available, set `E2E_RUN_WSO2=true` and run `npm run test:wso2`.

Rate-limit validation is destructive to shared quotas and therefore also requires `E2E_RUN_RATE_LIMIT=true`. Generated HTML, JUnit, traces, screenshots, and videos are ignored. Credential omissions produce explicit skips. Tests run serially to reduce collisions in shared fictional data.
