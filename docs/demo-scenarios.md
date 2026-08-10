# Healthcare platform demo scenarios

These scenarios require a running, configured WSO2 environment and fictional accounts/data.

1. **Patient login:** React creates PKCE/state, WSO2 authenticates, and the patient reaches their dashboard. Demonstrates public-client OAuth without a browser secret.
2. **Browse doctors:** Patient -> React -> WSO2 Gateway -> FastAPI -> PostgreSQL -> doctor list. Demonstrates scope enforcement and gateway-only access.
3. **Book appointment:** Select a doctor and available slot; a successful request returns 201. Patient identity is derived from authentication, not the form.
4. **Duplicate booking:** A competing booking returns 409; the UI explains that the slot is unavailable and refreshes availability.
5. **Patient isolation:** Patient B requesting Patient A's appointment receives a safe 404 from backend object authorization.
6. **Doctor flow:** A doctor loads an assigned appointment reference and applies `booked -> checked-in -> completed`. A list demonstration is blocked until a doctor-assigned list endpoint exists.
7. **Unauthorized administration:** A patient calling an administrator API receives 403 even if UI routes are manipulated.
8. **Administrator:** Administrator creates/updates/deactivates a doctor and views minimized appointment and masked patient lists.
9. **Rate limiting:** WSO2 returns 429 after the configured demonstration threshold; the client presents a safe retry message.

Do not claim any scenario passed until the real gateway, OAuth application, roles, scopes, subscription, backend JWT, and fictional records are configured and observed.
