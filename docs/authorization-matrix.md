# Authorization Matrix

`Allow` always means the token has the listed scope **and** the backend passes role, ownership/assignment, state-transition, and business-rule checks. Everything else is denied by default.

| Operation | OAuth scope | Patient | Doctor | Administrator |
|---|---|:---:|:---:|:---:|
| View doctors | `doctor:read` | Allow | Allow | Allow |
| View doctor availability | `availability:read` | Allow | Allow | Allow |
| Create appointment | `appointment:create` | Allow (self) | Deny | Allow (administrative workflow) |
| View own appointment | `appointment:read` | Allow | Deny | Allow |
| View assigned appointment | `appointment:read` | Deny | Allow | Allow |
| View all appointments | `appointment:read:all` | Deny | Deny | Allow |
| Cancel own appointment | `appointment:cancel` | Allow | Deny | Allow |
| Cancel assigned appointment | `appointment:cancel` | Deny | Allow | Allow |
| Cancel any appointment | `appointment:update` | Deny | Deny | Allow |
| Update appointment status | `appointment:update` | Deny | Allow (assigned only) | Allow |
| Create doctor | `doctor:write` | Deny | Deny | Allow |
| Update doctor | `doctor:write` | Deny | Deny | Allow |
| Delete doctor | `doctor:write` | Deny | Deny | Allow |
| View patient list | `patient:read` | Deny | Deny | Allow |
| Manage schedules | `availability:write` | Deny | Allow (own schedule if enabled) | Allow |

## Role-to-scope mapping

| Role | Initial scopes |
|---|---|
| Patient | `doctor:read`, `availability:read`, `appointment:create`, `appointment:read`, `appointment:cancel` |
| Doctor | `doctor:read`, `availability:read`, `availability:write`, `appointment:read`, `appointment:update`, `appointment:cancel` |
| Administrator | `doctor:read`, `doctor:write`, `availability:read`, `availability:write`, `appointment:create`, `appointment:read`, `appointment:read:all`, `appointment:update`, `appointment:cancel`, `patient:read`, `patient:write`, `admin:manage` |

## OAuth grant policy

- Web and mobile users use OAuth 2.0 Authorization Code with PKCE.
- Trusted non-user services use Client Credentials with narrowly assigned service scopes.
- Resource Owner Password Credentials is prohibited.

Scope validation at the gateway proves only that a client was granted a coarse capability. FastAPI must still validate the authenticated role and the relationship between the subject and the requested doctor, patient, appointment, or schedule. Administrative endpoints also require `admin:manage` where specified by the contract.
