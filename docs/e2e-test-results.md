# End-to-end test results

This document records the current working-tree result without claiming validation against an unavailable WSO2 runtime.

| Check | Result | Evidence or blocker |
|---|---|---|
| E2E TypeScript check | Passed | `npm run typecheck` |
| CI-safe unauthenticated browser check | Blocked locally | Chromium download timed out twice; Playwright reported its executable absent |
| Real WSO2 role flows | Blocked | No running/private WSO2 environment or test credentials supplied |
| Patient/admin workflows and isolation | Blocked | Require WSO2 and seeded fictional data |
| Doctor workflow | Partially specified | No doctor appointment-list endpoint; assigned reference required |
| Concurrent booking E2E | Blocked | No deterministic shared-slot orchestration API; covered at database level by Pytest |
| Rate limiting | Opt-in/blocked | Requires an isolated WSO2 throttling environment |
| Gateway routing/request ID | Blocked | Requires live WSO2 path |
| E2E discovery | Passed | 20 Chromium tests discovered in 7 spec files |
| Docker Compose syntax | Passed | `docker compose config --quiet` completed before image builds |
| Docker image builds | Blocked locally | Docker Desktop Linux engine pipe was not running |

Frontend lint, typecheck, 16 unit tests, and production build passed. Backend Ruff lint/format, strict MyPy, and 28 Pytest tests passed. These results do not convert blocked WSO2 scenarios into passes.

After a real run, record its command, environment, timestamp, totals, and artifact link. Never add credentials, tokens, patient data, or sensitive logs.
