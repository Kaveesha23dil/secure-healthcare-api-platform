# Final security validation

| Control | Evidence | Status |
|---|---|---|
| OAuth PKCE S256/state/nonce | Frontend implementation and unit tests | Implemented; WSO2 run pending |
| Tokens remain memory-only | Frontend token storage | Implemented |
| Browser calls gateway only | Central client and Playwright observer | Implemented; runtime proof pending |
| Missing/forged identity denied | E2E probes and backend assertion tests | Backend verified; WSO2 pending |
| Scope, role, ownership, assignment | Mappings, dependencies, security tests | Backend verified; WSO2 E2E pending |
| Patient ID cannot be mass-assigned | Schema test and browser POST assertion | Backend verified; browser pending |
| Duplicate/concurrent slot protection | Constraint and integration tests | Backend verified; deterministic E2E absent |
| Safe errors and throttling UX | Problem handlers and allowlisted UI text | Implemented; throttle run pending |
| Request ID and audit events | Middleware, services, tests | Backend verified; cross-system correlation pending |
| Secrets and fictional data | Ignored env/artifacts and CI scan | Implemented |

Residual gaps: WSO2 runtime setup is manual; doctor appointment discovery and safe current-doctor availability mutation are absent; no deterministic E2E seed/cleanup API exists; limited-scope identity, rate policy, private backend reachability, TLS, and log/audit correlation require environment validation. No regulatory-compliance claim is made.
