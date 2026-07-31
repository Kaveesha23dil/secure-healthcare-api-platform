# Data Classification and Handling

Only fictional data may be used in this educational project.

| Class | Examples | Permitted access | Logging | Encryption | Retention | Masking |
|---|---|---|---|---|---|---|
| Public | Doctor display name, specialization, clinic name, general availability | Any API consumer; write access is administrative | May be logged when operationally necessary | TLS in transit; standard platform storage controls | Retain while current; remove/stale-mark on deletion | Not normally required |
| Internal | Internal user IDs, audit metadata, API usage statistics, administrative configuration | Authorized workforce, services, and administrators | Structured logs allowed with minimization | TLS in transit; encryption at rest | Defined operational/audit schedule; delete or anonymize at expiry | Mask identifiers in broad reports where feasible |
| Sensitive | Patient name/email/telephone, appointment history/reason, doctor-patient relationship, access/refresh tokens, authentication details | Subject, assigned care role, or authorized administrator/service with a documented purpose | Patient fields minimized and masked; tokens, secrets, and authentication details never logged | HTTPS externally and encryption at rest using managed keys | Shortest legal/educational period; tokens expire promptly; test data routinely purged | Email and telephone masked; identifiers pseudonymized in analytics |

## Example fields

- **Public:** `Doctor.displayName`, `Doctor.specialization`, `AvailabilitySlot.startAt`
- **Internal:** `createdBy`, `updatedBy`, `AuditEvent.traceId`, gateway policy identifiers
- **Sensitive:** `Patient.email`, `Patient.phone`, `Appointment.reason`, bearer and refresh tokens

## Mandatory controls

- Never collect or store real patient information.
- Use HTTPS for every external connection and authenticated internal connection.
- Never place access tokens, refresh tokens, secrets, private keys, passwords, or authentication details in logs.
- Keep secrets out of source control and inject them from environment-based secret management.
- Encrypt sensitive data at rest and manage keys separately from data.
- Produce structured security audit events and keep audit logs separate from application/debug logs.
- Mask email addresses and telephone numbers in operational views and logs (for example, `f***@example.invalid` and `***-***-0142`).
- Minimize collection, response fields, and log attributes to the purpose of each operation.
- Apply documented retention limits and automated deletion/anonymization where possible.
- Restrict exports and backups to the same classification controls as the source data.
- Review access and retention policies before any production-like deployment.

Compliance with a particular healthcare or privacy regulation is not claimed.
