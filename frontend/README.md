# Healthcare Web Client

React/TypeScript demonstration client for the Secure Healthcare API. Protected requests go only to the WSO2 API Gateway. The frontend never contains an OAuth client secret.

## Local setup

Requirements: Node.js 22+, npm, a configured WSO2 public OAuth application, and a published healthcare API.

```powershell
cd frontend
npm install
Copy-Item .env.example .env
npm run dev
```

Configure the public client ID and local endpoints in `.env`; never add secrets or tokens. Register redirect URI `http://localhost:5173/auth/callback`, post-logout URI `http://localhost:5173/login`, and allowed origin `http://localhost:5173`. Configure gateway CORS explicitly for that origin; do not enable wildcard authenticated CORS.

Commands: `npm run lint`, `npm run typecheck`, `npm run test`, `npm run format:check`, and `npm run build`. Docker: `docker build -t secure-healthcare-web:local .`; runtime configuration is compiled into a Vite build, so build separate non-secret artifacts or use an approved runtime-config pattern per environment.

## Authentication and roles

The SPA uses Authorization Code with PKCE S256 and state. Access tokens remain in memory; reloading requires sign-in again. Only short-lived verifier/state/return-path transaction data uses session storage. No refresh-token persistence is implemented. Patient, doctor, and administrator checks affect navigation only; WSO2 and FastAPI enforce security.

Patient workflows browse doctors/availability, book without a patient ID, list `/me` appointments, and cancel eligible bookings. Administrators manage doctors and view minimized appointments/patients. The backend currently lacks a doctor-assigned list and a current-doctor profile endpoint, so those doctor screens disclose the gap instead of inventing unsafe APIs.

Troubleshooting: verify WSO2 redirect URIs, CORS, API subscription/scopes, gateway context `/healthcare/1.0.0`, local certificates, and the ID-token role claim mapping. Never bypass the gateway by pointing the browser at FastAPI.
