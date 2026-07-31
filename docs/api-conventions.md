# API Conventions

## Resources and representation

- Use plural, lowercase REST resources beneath `/api/v1`: `doctors`, `availability`, `appointments`, `patients`, and `admin`.
- Do not place verbs in resource URLs unless no resource-oriented design is practical.
- Requests and normal responses use JSON. Errors use `application/problem+json` according to RFC 9457.
- Identifiers are UUIDs. Date-time strings use ISO 8601 with an explicit timezone offset; PostgreSQL stores normalized UTC instants.
- Concepts may be inspired by HL7 FHIR, but no FHIR compliance is claimed.
- Sensitive values, bearer tokens, patient contact details, and appointment reasons must not appear in URLs.

## Pagination, filtering, and sorting

Collections accept `page` (1-based, default `1`) and `size` (default `20`, maximum `100`). Responses include `page`, `size`, `totalItems`, and `totalPages`. Supported filters and sort fields are explicit allowlists per endpoint; prefix descending fields with `-` (for example, `sort=-startAt`). Unknown or expensive expressions are rejected.

## Idempotency

Safe methods are naturally idempotent. Appointment creation accepts an `Idempotency-Key` UUID header; the server binds the key to the authenticated subject and canonical request hash for a limited retention period. Reuse with different content returns `409`. PATCH operations use transactional state-transition validation; future implementations should support conditional updates with an ETag/version.

## Correlation and request identifiers

Clients may send `X-Correlation-ID` as a UUID to link a business flow. The gateway/server generates or validates `X-Request-ID` for each hop and returns it. Neither value is an authorization credential. Unsafe values are replaced. Logs and problem details use the trace identifier without sensitive payloads.

## Versioning and deprecation

Major versions are in the base path (`/api/v1`). Compatible additions remain within a major version; breaking changes require a new major version. Deprecated operations publish `Deprecation` and `Sunset` metadata, migration guidance, and at least a documented consumer migration window. Usage is monitored before shutdown. Unsupported vulnerable versions may be retired faster through an approved security process.

## Status codes

- `200` successful read/update; `201` created; `204` successful deletion without content.
- `400` malformed request or invalid state transition; `401` missing/invalid authentication.
- `403` authenticated but functionally unauthorized when disclosure is safe.
- `404` absent or deliberately concealed resource; use for failed ownership checks to reduce enumeration.
- `409` state/idempotency/duplicate-booking conflict; `422` schema validation failure.
- `429` rate limited; `500` unexpected server failure with no internal details.

## Standard problem response

```json
{
  "type": "https://api.example.com/problems/appointment-not-found",
  "title": "Appointment not found",
  "status": 404,
  "detail": "The requested appointment does not exist or is not accessible.",
  "instance": "/api/v1/appointments/6f471ba2-28b5-41d4-9a5b-85f44bc3ae6e",
  "traceId": "4de6527d-9ea7-471a-84bc-3b87eaef2164"
}
```

Validation problems add an `errors` array with safe field paths and messages. The service never reveals whether an inaccessible record belongs to another patient and never returns stack traces or raw database errors.
