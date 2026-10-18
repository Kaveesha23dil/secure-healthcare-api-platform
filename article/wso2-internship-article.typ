#set document(title: "Secure Healthcare API Platform — A Zero-Trust API Built on WSO2 API Manager")
#set page(paper: "a4", margin: (x: 1.9cm, top: 1.7cm, bottom: 1.9cm), numbering: "1 / 1")
#set text(font: "Libertinus Serif", size: 10pt, lang: "en", region: "US")
#set par(justify: true, leading: 0.7em)
#set heading(numbering: none)

// ------------------------------------------------------------------ palette
#let navy     = rgb("#0f172a")
#let tealDeep = rgb("#0f766e")
#let teal     = rgb("#0d9488")
#let tealLight= rgb("#ccfbf1")
#let mist     = rgb("#f0fdfa")
#let cardboard= rgb("#f8fafc")
#let hairline = rgb("#e2e8f0")
#let ink      = rgb("#334155")
#let inkSoft  = rgb("#64748b")
#let roseDeep = rgb("#be123c")
#let amber    = rgb("#92400e")

// ------------------------------------------------------------------ helpers
#let accent-block(titlecolor: tealDeep, title: "", body: []) = block(
  fill: mist, stroke: (left: 3pt + teal), radius: 6pt, width: 100%,
  inset: (x: 13pt, y: 11pt),
  [
    #text(fill: titlecolor, weight: "bold", size: 10pt, font: "Inter 18pt")[#title]
    #par(spacing: 2pt)[#text(fill: ink, size: 9pt)[#body]]
  ],
)

#let codeblock(body) = block(
  fill: cardboard, stroke: 0.6pt + hairline, radius: 4pt, width: 100%,
  inset: (x: 11pt, y: 9pt),
  text(font: "DejaVu Sans Mono", size: 8pt, body),
)

#let coverchip(name) = box(
  width: 100%, fill: rgb("#134e4a"), stroke: 0.6pt + rgb("#2dd4bf"), radius: 3pt,
  inset: (x: 4pt, y: 2.5pt),
  align(center, text(fill: rgb("#99f6e4"), size: 6.8pt, font: "Inter 18pt")[#name]),
)

#let statchip(v, label) = block(
  fill: mist, stroke: 0.6pt + rgb("#99f6e4"), radius: 5pt, width: 100%,
  inset: (x: 7pt, y: 7pt),
  [
    #align(center, text(fill: tealDeep, weight: "bold", size: 13pt)[#v])
    #align(center, text(fill: inkSoft, size: 7.5pt)[#label])
  ],
)

#let stepcard(n, label, body) = block(
  fill: mist, stroke: 0.6pt + rgb("#99f6e4"), radius: 5pt, width: 100%,
  inset: (x: 9pt, y: 7pt),
  [
    #box(circle(fill: teal, radius: 7pt, text(size: 8pt, fill: white, weight: "bold")[#n]))
    #box[#h(3pt)#text(fill: navy, weight: "bold", size: 9pt, font: "Inter 18pt")[#label]]
    #v(2pt)
    #text(fill: ink, size: 8pt)[#body]
  ],
)

// ------------------------------------------------------------------ heading styling
#show heading.where(level: 1): it => {
  v(9pt)
  text(fill: navy, weight: "bold", size: 14pt, font: "Inter 18pt")[#it.body]
  v(1.5pt)
  line(length: 100%, stroke: 1.6pt + gradient.linear(teal, white, angle: 0deg))
  v(4pt)
}

#show heading.where(level: 2): it => {
  v(4pt)
  text(fill: tealDeep, weight: "bold", size: 10.5pt, font: "Inter 18pt")[#it.body]
  v(2pt)
}

// ------------------------------------------------------------------ cover
#block(
  fill: gradient.linear(rgb("#115e59"), navy, angle: 90deg),
  inset: (x: 24pt, y: 22pt), radius: 9pt, width: 100%,
)[
  #text(fill: white, weight: "bold", size: 25pt, font: "Inter 18pt")[Secure Healthcare API Platform]
  #v(5pt)
  #text(fill: tealLight, size: 12pt, style: "italic")[A Zero-Trust, Contract-First API for Healthcare Appointment Scheduling — Built on WSO2 API Manager 4.7.0, FastAPI, and PostgreSQL]
  #v(11pt)
  #line(length: 100%, stroke: 0.6pt + rgb("#2dd4bf"))
  #v(10pt)
  #grid(
    columns: (1fr, 1fr, 1fr, 1fr),
    column-gutter: 4pt, row-gutter: 4pt,
    coverchip[WSO2 API Manager 4.7.0],
    coverchip[FastAPI],
    coverchip[PostgreSQL 17],
    coverchip[OpenAPI 3.0.3],
    coverchip[OAuth2 + PKCE],
    coverchip[RS256 / JWKS],
    coverchip[APIOps],
    coverchip[Docker],
  )
]

#v(9pt)
#grid(columns: (1.4fr, 3fr, 1.6fr), column-gutter: 8pt)[
  block(fill: cardboard, radius: 4pt, inset: (x: 9pt, y: 6pt))[#text(fill: inkSoft, size: 8pt)[Portfolio Article] \ #v(1pt) #text(fill: ink, size: 9pt, weight: "bold")[Kaveesha Dilshan]]
  block(fill: cardboard, radius: 4pt, inset: (x: 9pt, y: 6pt), align: center)[#text(fill: inkSoft, size: 8pt)[August 2026]]
  block(fill: cardboard, radius: 4pt, inset: (x: 9pt, y: 6pt), align: right)[#text(fill: tealDeep, size: 8pt)[github.com/Kaveesha23dil/secure-healthcare-api-platform]]
]

#v(8pt)
#accent-block(
  title: "Abstract",
  body: [
    Healthcare systems are among the most valuable and sensitive digital assets, which is why an API platform must be secure by design rather than secure by accident. This project answers one question: *how do you enforce security at every layer of a healthcare appointment API, not just at the login screen?*

  The result is a zero-trust, contract-first clinical scheduling platform in which WSO2 API Manager 4.7.0 serves as the governance perimeter — validating OAuth2 tokens, enforcing operation scopes, throttling subscriptions, and issuing cryptographically signed backend assertions — while a FastAPI service independently verifies those assertions and enforces fine-grained role and record-ownership policies down to individual appointments. The article walks through the architecture, the WSO2 integration, the threat model, and the engineering practices behind 31 passing tests.
  ],
)

#v(6pt)
#grid(
  columns: (1fr,) * 5, column-gutter: 6pt, row-gutter: 6pt,
  statchip("31", "passing unit / integration / security tests"),
  statchip("52", "source files clean under strict MyPy"),
  statchip("100%", "Ruff lint & format compliance"),
  statchip("10", "steps in the zero-trust request flow"),
  statchip("2", "independent authorization tiers"),
)

// ================================================================== 1
#heading(level: 1)[1.  The Problem: Healthcare APIs Need More Than a Login Page]

#par[
  Patient data is the most targeted and heavily regulated category of data in the digital ecosystem. A single accidentally exposed record can erode trust, violate privacy expectations, and cause real personal harm. Traditional web applications stop at "is the user authenticated?" — but for an appointment platform, that question must be followed by a chain of harder questions: *is the token still valid? does it carry the right scope? is the caller allowed to touch this doctor, this schedule, this appointment — or only their own?*
]

#par[
  I designed this platform around strict trust boundaries, a structured threat model (STRIDE combined with OWASP API Security risks), and a defense-in-depth posture in which every layer fails closed. To stay rigorous, the project uses a contract-first methodology: an authoritative OpenAPI 3.0.3 specification defines every data model, query parameter, scope, error model (RFC 9457 Problem Details), and idempotency requirement before any runtime code is written. All patient, doctor, and schedule data is entirely fictional, and the system is an educational demonstration with no compliance claims.
]

// ================================================================== 2
#heading(level: 1)[2.  Architecture at a Glance]

The platform is a containerized, four-tier system in which each boundary owns a specific security responsibility.

#grid(
  columns: (1fr, 1em, 1fr, 1em, 1fr, 1em, 1fr),
  column-gutter: 0pt, row-gutter: 4pt,
  box(width: 100%, fill: rgb("#e0e7ff"), stroke: 0.7pt + rgb("#a5b4fc"), radius: 5pt, inset: (x: 6pt, y: 6pt), align(center, text(fill: navy, size: 8.2pt, weight: "bold", font: "Inter 18pt")[Client])),
  align(center, text(fill: teal, size: 10.5pt, weight: "bold")[→]),
  box(width: 100%, fill: rgb("#ccfbf1"), stroke: 0.7pt + teal, radius: 5pt, inset: (x: 6pt, y: 6pt), align(center, text(fill: tealDeep, size: 8.2pt, weight: "bold", font: "Inter 18pt")[WSO2 API Manager])),
  align(center, text(fill: teal, size: 10.5pt, weight: "bold")[→]),
  box(width: 100%, fill: rgb("#fef3c7"), stroke: 0.7pt + rgb("#fcd34d"), radius: 5pt, inset: (x: 6pt, y: 6pt), align(center, text(fill: rgb("#92400e"), size: 8.2pt, weight: "bold", font: "Inter 18pt")[FastAPI Backend])),
  align(center, text(fill: teal, size: 10.5pt, weight: "bold")[→]),
  box(width: 100%, fill: rgb("#fee2e2"), stroke: 0.7pt + rgb("#fca5a5"), radius: 5pt, inset: (x: 6pt, y: 6pt), align(center, text(fill: roseDeep, size: 8.2pt, weight: "bold", font: "Inter 18pt")[PostgreSQL])),
  text(fill: inkSoft, size: 6.5pt)[OAuth2 PKCE flow · bearer token],
  h(0pt),
  text(fill: inkSoft, size: 6.5pt)[OAuth2 validation · scopes · throttling · signed assertions],
  h(0pt),
  text(fill: inkSoft, size: 6.5pt)[RS256 verification · role & ownership checks],
  h(0pt),
  text(fill: inkSoft, size: 6.5pt)[ACID transactions · slot uniqueness · audit],
)

#accent-block(
  title: "Why WSO2 API Manager is the Perimeter",
  body: [
    The gateway is untrusted-facing and enforces policy before any request reaches the domain layer: it validates the OAuth2 access token, verifies that the token carries the required operation scope, enforces subscription quotas, strips any client-supplied identity headers (preventing spoofing), and finally issues its own short-lived RSA-signed backend JWT that the FastAPI service can trust.
  ],
)

// ================================================================== 3
#heading(level: 1)[3.  WSO2 API Manager: The Governance Heart]

WSO2 API Manager 4.7.0 is not an add-on here — it is the enforcement point around which the entire request lifecycle is designed. The API is imported into the *Publisher Portal* from the OpenAPI contract under context `/healthcare`, version `1.0.0`, deployed to the Classic Gateway (HTTPS port `8243`), and published to the catalog.

| Component of WSO2 | Role in this platform |
| :--- | :--- |
| *Publisher Portal* (`/publisher`) | Imports the OpenAPI 3.0.3 contract, maps backend endpoints, defines policies, and drives the API lifecycle (Created → Deployed → Published) |
| *Developer Portal* (`/devportal`) | Application registration (`HealthcareWebApp`), tier subscriptions, OAuth2 token generation (Authorization Code + PKCE), API exploration |
| *Admin Portal* (`/admin`) | Custom throttling policy configuration (the `5PerMin` demonstration tier) |
| *Classic Gateway* (`:8243`) | Token validation, scope enforcement, rate limiting, header stripping, and routing of validated traffic to FastAPI |
| *Signed Backend JWT* | Gateway signs a short-lived assertion with its RSA key (`SHA256withRSA`) and forwards it in the `X-JWT-Assertion` header |

#par[
  Configuring `[apim.jwt]` in `deployment.toml` enables backend JWT generation with a header of `X-JWT-Assertion`, base64url encoding, and SHA256withRSA signing. The gateway embeds the authenticated subject (`sub`), mapped roles (`roles`), and granted scopes (`scope`) into the assertion — giving the backend a cryptographically verifiable identity context rather than a merely network-implied one.
]

// ================================================================== 4
#heading(level: 1)[4.  The 10-Step Zero-Trust Request Flow]

Every protected API call traverses ten discrete security steps, split across the gateway and the application:

#grid(
  columns: (1fr, 1fr), column-gutter: 7pt, row-gutter: 6pt,
  stepcard(1, "Client Token Acquisition", "OAuth2 Authorization Code with PKCE; tokens are kept memory-only inside the React client and an attendable nonce/state binds the flow."),
  stepcard(2, "Gateway Invocation", "The client calls the API through the WSO2 Classic Gateway at https://localhost:8243/healthcare/1.0.0."),
  stepcard(3, "OAuth2 Token Validation", "WSO2 verifies the bearer token's signature, expiry, and active state before anything else happens."),
  stepcard(4, "Perimeter Scope Check", "WSO2 confirms the token carries the required operation scope (for example `doctor:read`)."),
  stepcard(5, "Subscription & Throttling", "The `5PerMin` tier is applied; requests beyond the quota are halted with HTTP `429`."),
  stepcard(6, "Signed Assertion Injection", "The client's `X-JWT-Assertion` header is stripped and a freshly signed assertion is generated by the gateway."),
  stepcard(7, "Forward to Backend", "The request plus signed assertion is forwarded to the FastAPI service."),
  stepcard(8, "Cryptographic Verification", "FastAPI validates the RS256 signature via JWKS/certificate, plus issuer, algorithm, expiry, and not-before claims."),
  stepcard(9, "Fine-Grained Authorization", "Role policies and record-ownership checks run at the application layer, defaulting to deny."),
  stepcard(10, "Transaction & Response", "Authorized operations execute inside a PostgreSQL transaction; sanitized responses return through the gateway."),
)

#par[
  The important design detail is *independence*: even if a token passed the gateway, the backend never trusts it blindly. It re-verifies the assertion cryptographically, then answers the questions the gateway cannot — *does this subject own this record?*
]

// ================================================================== 5
#heading(level: 1)[5.  Two-Tier Authorization: Scopes at the Edge, Verification at the Core]

Scopes authorize *operations*; roles authorize *people*; record ownership authorizes *specific rows*. The platform deliberately separates these so a failure in one layer never grants access by itself.

#heading(level: 2)[5.1  Perimeter layer — WSO2 Gateway]
Validation is performed on token integrity, activity, and expiry; required OAuth2 scopes are checked per operation (e.g. `appointment:create`, `doctor:write`); and subscription quotas and rate limits are enforced with a standardized `429`.

#heading(level: 2)[5.2  Application layer — FastAPI]
In `AUTH_MODE=wso2_backend_jwt`, FastAPI rejects plain identity headers entirely (`X-User-ID`, `X-Role`, ...) and accepts identity only from the signed `X-JWT-Assertion`. It verifies:
+ the *RSA signature* against WSO2's public certificate or the gateway JWKS endpoint (with bounded caching and key rotation support),
+ the *algorithm allowlist* (`RS256` only — no `alg=none`, no symmetric-confusion),
+ the *issuer* (`wso2.org/products/am`) and *time claims* (`exp`, `nbf`),
+ the *subject, role, and scope claim mappings* configured for the environment.

Then it enforces role-scope matrices and object-level rules:
- *IDOR protection (BOLA):* appointments are queried with *both* the requested ID and the verified subject's identity; mismatches return a concealed `404 Not Found` instead of `403`, denying enumeration of UUIDs.
- *Patient isolation:* a patient may only read appointments linked to their verified subject UUID.
- *Doctor assignment:* a doctor may only update appointments genuinely assigned to them.
- *Mass-assignment rejection:* request schemas forbid unknown fields such as `patientId` or `status` from client input.

// ================================================================== 6
#heading(level: 1)[6.  Consistency Under Concurrency]

Scheduling race conditions are a classic API failure: two clients book the same slot within milliseconds. The platform solves this at the data layer, not just in business logic.

- Database-level protections, including the *active-slot unique constraint*, guarantee that only one of two concurrent bookings can commit; the loser receives `409 Conflict`.
- *Idempotency:* appointment creation honors a client-provided `Idempotency-Key`, caching the response so a network retry never duplicates a record.
- Every operation runs in an ACID transaction, and authorization decisions emit sanitized audit events (actor, action, outcome, trace ID) without logging tokens, contact details, or appointment reasons.

// ================================================================== 7
#heading(level: 1)[7.  Engineering Standards: Measured, Not Claimed]

Quality was treated as a deliverable with verifiable evidence:

#table(
  columns: (1.1fr, 4fr),
  inset: (x: 8pt, y: 5pt),
  align: (left, left),
  stroke: 0.5pt + hairline,
  table.cell(fill: tealDeep, text(fill: white, weight: "bold", size: 8.5pt)[Check]),
  table.cell(fill: tealDeep, text(fill: white, weight: "bold", size: 8.5pt)[Result]),
  text(size: 8.5pt, weight: "bold")[Test suite],
  text(size: 8.5pt)[31 tests passing — including malformed, expired, and invalid-signature JWTs, algorithm-confusion attempts, forged-header rejection, role/scope matrices, and ownership/assignment authorization],
  text(size: 8.5pt, weight: "bold")["Static typing"],
  text(size: 8.5pt)["Strict MyPy: no issues across 52 source files"],
  text(size: 8.5pt, weight: "bold")["Lint & format"],
  text(size: 8.5pt)["100% Ruff lint compliance; project style formatting"],
  text(size: 8.5pt, weight: "bold")["Migrations"],
  text(size: 8.5pt)["Alembic single-head migration applied against PostgreSQL 17"],
  text(size: 8.5pt, weight: "bold")["E2E"],
  text(size: 8.5pt)["Playwright end-to-end suite exercising OAuth flows and role-based UI paths"],
)

#par[
  Beyond the code, the repository includes an `apiops/` area with `apictl` project configurations, environment parameter templates, promotion/rollback documentation, and validation/deployment scripts — a small APIOps pipeline that treats API governance as code.
]

// ================================================================== 8
#heading(level: 1)[8.  Verified Runtime Evidence]

The integration was exercised against a real local WSO2 API Manager instance. The key gateway behaviors were verified manually:

#table(
  columns: (1.6fr, 1.3fr, 0.6fr, 2.6fr),
  inset: (x: 8pt, y: 5pt),
  align: (left,),
  stroke: 0.5pt + hairline,
  table.cell(fill: tealDeep, text(fill: white, weight: "bold", size: 8.5pt)[Scenario]),
  table.cell(fill: tealDeep, text(fill: white, weight: "bold", size: 8.5pt)[Expected]),
  table.cell(fill: tealDeep, text(fill: white, weight: "bold", size: 8.5pt)[Verified]),
  table.cell(fill: tealDeep, text(fill: white, weight: "bold", size: 8.5pt)[Observation]),
  [*Request without token*], [`401 Unauthorized`], [Yes], [Gateway rejects unauthenticated traffic before it reaches FastAPI],
  [*Token without required scope*], [`403 Forbidden`], [Yes], [Gateway rejects a token lacking `doctor:read`],
  [*Valid `doctor:read` token*], [`200 OK`], [Yes], [Gateway forwards the request; FastAPI returns the doctor list],
  [*Signed backend JWT*], [Verified], [Yes], [FastAPI verifies `X-JWT-Assertion` RS256 signature and claims],
  [*Exceeding 5 requests/min*], [`429 Too Many Requests`], [Yes], [WSO2 throttles with `code: 900804` — "Message throttled out"],
)

#v(5pt)
#codeblock[{
  "code": "900804",
  "message": "Message throttled out",
  "description": "You have exceeded your quota"
}]

#v(4pt)
#figure(
  image("../docs/images/02-subscription.png", width: 62%),
  caption: [Developer Portal — the HealthcareWebApp application is subscribed to the API with the custom `5PerMin` throttling policy.],
) <fig-sub>

#figure(
  image("../docs/images/03-401-missing-token.png", width: 62%),
  caption: [HTTP `401 Unauthorized` — unauthenticated gateway traffic is rejected immediately by WSO2 before reaching the backend.],
) <fig-401>

#figure(
  image("../docs/images/06-429-throttling.png", width: 62%),
  caption: [HTTP `429 Too Many Requests` — the gateway throttling response when the `5PerMin` quota is exceeded.],
) <fig-429>

// ================================================================== 9
#heading(level: 1)[9.  Technology Stack]

#table(
  columns: (1.1fr, 1.8fr, 1.4fr),
  inset: (x: 8pt, y: 5pt),
  align: (left,),
  stroke: 0.5pt + hairline,
  table.cell(fill: tealDeep, text(fill: white, weight: "bold", size: 8.5pt)[Layer]),
  table.cell(fill: tealDeep, text(fill: white, weight: "bold", size: 8.5pt)[Technology]),
  table.cell(fill: tealDeep, text(fill: white, weight: "bold", size: 8.5pt)[Role / Version]),
  [API Gateway], [WSO2 API Manager], [4.7.0 — OAuth2/OIDC, JWT assertions, throttling],
  [Backend], [FastAPI + Python], [Python 3.12 · Pydantic v2 · Uvicorn],
  [Database], [PostgreSQL + SQLAlchemy], [PostgreSQL 17 · SQLAlchemy 2.0 async · Alembic],
  [Security], [PyJWT + Cryptography], [RS256, X.509 cert loading, JWKS caching],
  [Client], [React + TypeScript], [Vite · TailwindCSS · OAuth2 PKCE],
  [Tooling], [Docker · Ruff · MyPy · Pytest · Playwright], [Multi-container, strict typing, CI validation, E2E],

)

// ================================================================== 10
#heading(level: 1)[10.  What I Learned — and Why WSO2]

#accent-block(
  title: "The difference between an API and an API platform",
  body: [
    Building this platform taught me that an API's security story is decided by its platform, not its routes. Since WSO2 owns token validation, scope enforcement, throttling, and assertion signing, the backend is free to focus on the part only it can do — domain rules and per-record authorization. The signed backend-assertion pattern struck me as particularly elegant: it turns a network trust assumption (the boundary between gateway and service) into a cryptographic fact.
  ],
)

#par[
  The experience also reshaped how I think about governance: the contract is the single source of truth, scopes are engineered as least-privilege grants, mappings live in version-controlled YAML, and an APIOps workflow promotes a validated API from specification to deployment. These are exactly the competencies WSO2 is known for — API products, integration platforms, identity management, and API-centric engineering. I am applying for the WSO2 internship because I want to contribute to platform-scale products and learn from engineers who design the layer I have spent this project learning to respect.
]

// ================================================================== 11
#heading(level: 1)[11.  Conclusion]

This project set out to prove that security for a healthcare API can be layered, auditable, and demonstrable. The result is a contract-first platform where WSO2 API Manager governs the perimeter, FastAPI verifies identity cryptographically and enforces fine-grained authorization, and PostgreSQL guarantees consistency under concurrency — all backed by a rigorous threat model, strict typing, and a passing test suite.

#accent-block(
  title: "Repository",
  body: [github.com/Kaveesha23dil/secure-healthcare-api-platform — OpenAPI contract, WSO2 configuration, APIOps workflows, backend, frontend, E2E suite, and runtime evidence are all in one place.],
)

#v(8pt)
#block(
  fill: cardboard, stroke: 0.6pt + hairline, radius: 5pt, width: 100%,
  inset: (x: 11pt, y: 8pt),
  align(center, text(fill: inkSoft, size: 7.5pt, style: "italic")[Educational demonstration project. All patient, doctor, and schedule data is entirely fictional. No regulatory-compliance (HIPAA / GDPR / FHIR) claim is made.]),
)