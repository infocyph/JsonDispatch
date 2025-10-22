# JsonDispatch – Developer Guide

Welcome! This site hosts the JsonDispatch specification and examples.

- **What is it?** A lightweight, production-ready JSON response spec.
- **Why use it?** Stable envelope (`success`/`fail`/`error`), server-generated tracing with `X-Request-Id` and clear version signaling via `X-Api-Version`.

---

## Contents

[1. Introduction](#1-introduction)  
[1.2 Why Another Spec?](#12-why-another-spec)  
[1.3 Core Principles](#13-core-principles)

[2. Media Types & Versioning](#2-media-types--versioning)  
[2.1 Media Type Explained (with Examples)](#21-media-type-explained-with-examples)  
[2.2 Versioning Strategy (Major/Minor/Patch)](#22-versioning-strategy-majorminorpatch)  
[2.3 Required & Recommended Headers](#23-required--recommended-headers)  
[2.4 Version Selection & Migration](#24-version-selection--migration)  
[2.5 Non-JSON Responses (Reports & Exports)](#25-non-json-responses-reports--exports)  
[2.5.1 Direct File Delivery](#251-direct-file-delivery)  
[2.5.2 Orchestration via JsonDispatch (Recommended)](#252-orchestration-via-jsondispatch-recommended)  
[2.5.3 Streaming & Large Datasets](#253-streaming--large-datasets)  
[2.6 Authentication & Authorization](#26-authentication--authorization)  
[2.6.1 Authentication Token Placement](#261-authentication-token-placement)  
[2.6.2 Authentication Failure Responses](#262-authentication-failure-responses)  
[2.6.3 Authorization (403 Forbidden)](#263-authorization-403-forbidden)  
[2.6.4 API Key Authentication](#264-api-key-authentication)  
[2.6.5 OAuth 2.0 & Token Refresh](#265-oauth-20--token-refresh)

[3. Request & Response Identification](#3-request--response-identification)  
[3.1 X-Request-Id – Server-Generated Trace ID](#31-x-request-id--server-generated-trace-id)  
[3.2 X-Correlation-Id – Linking Related Operations](#32-x-correlation-id--linking-related-operations)  
[3.3 Distributed Tracing (traceparent, tracestate)](#33-distributed-tracing-traceparent-tracestate)  
[3.4 Rate Limiting](#34-rate-limiting)  
[3.4.1 Rate Limit Headers](#341-rate-limit-headers)  
[3.4.2 Rate Limit Exceeded Response](#342-rate-limit-exceeded-response)  
[3.4.3 Rate Limiting Strategies](#343-rate-limiting-strategies)

[4. Response Envelope (The Outer Wrapper)](#4-response-envelope-the-outer-wrapper)  
[4.1 Top-Level Members at a Glance](#41-top-level-members-at-a-glance)  
[4.2 `status` — Success, Fail or Error](#42-status--success-fail-or-error)  
[4.3 `message` — Keep It Human-Friendly](#43-message--keep-it-human-friendly)  
[4.4 `data` — Your Actual Payload](#44-data--your-actual-payload)  
[4.5 `_references` — Turning IDs Into Meaning](#45-_references--turning-ids-into-meaning)  
[4.6 `_properties` — Describing Data Context](#46-_properties--describing-data-context)  
[4.7 `_links` — Pagination and Beyond](#47-_links--pagination-and-beyond)  
[4.8 Envelope Summary](#48-envelope-summary)

[5. Response Examples](#5-response-examples)  
[5.1 A Simple Success Response](#51-a-simple-success-response)  
[5.2 A Fail Response (Validation Issue)](#52-a-fail-response-validation-issue)  
[5.3 An Error Response (System Failure)](#53-an-error-response-system-failure)  
[5.4 Paginated Collection Response](#54-paginated-collection-response)  
[5.5 References in Action](#55-references-in-action)  
[5.6 Async & Long-Running Operations](#56-async--long-running-operations)  
[5.6.1 Initiating an Async Job (202 Accepted)](#561-initiating-an-async-job-202-accepted)  
[5.6.2 Polling for Job Status](#562-polling-for-job-status)  
[5.6.3 Webhook Notifications](#563-webhook-notifications)  
[5.6.4 Job Failure Handling](#564-job-failure-handling)  
[5.7 Bulk Operations & Partial Success](#57-bulk-operations--partial-success)  
[5.7.1 Partial Success Response Structure](#571-partial-success-response-structure)  
[5.7.2 Atomic vs Non-Atomic Operations](#572-atomic-vs-non-atomic-operations)  
[5.7.3 Batch Result Summary](#573-batch-result-summary)

[6. Error Handling](#6-error-handling)  
[6.1 `fail` vs `error` — Know the Difference](#61-fail-vs-error--know-the-difference)  
[6.2 Error Object Structure](#62-error-object-structure)  
[6.3 Field-Level vs Request-Level Errors](#63-field-level-vs-request-level-errors)  
[6.4 Error Codes (`code`) — Symbolic and Actionable](#64-error-codes-code--symbolic-and-actionable)  
[6.5 Recommended HTTP Status Mapping](#65-recommended-http-status-mapping)  
[6.6 Key Takeaways](#66-key-takeaways)

[7. Properties & References](#7-properties--references)  
[7.1 `_properties` — Describe Your Data](#71-_properties--describe-your-data-not-just-send-it)  
[7.2 `_references` — Replace IDs with Meaning](#72-_references--replace-ids-with-meaning)  
[7.3 Choosing Between Them](#73-choosing-between-them)  
[7.4 Example — Combined in One Response](#74-example--combined-in-one-response)  
[7.5 Nested `_references` Example](#75-nested-_references-example)

[8. Links](#8-links)  
[8.1 `_links` for Pagination](#81-_links-for-pagination)  
[8.2 `_links` for Related Resources](#82-_links-for-related-resources)  
[8.3 `_links` with Metadata (Enriched Links)](#83-_links-with-metadata-enriched-links)  
[8.4 Best Practices for `_links`](#84-best-practices-for-_links)  
[8.5 `_links` for Files and Downloads](#85-_links-for-files-and-downloads)  
[8.6 `_links` for Inline Media (Thumbnails, Avatars, Previews)](#86-_links-for-inline-media-thumbnails-avatars-previews)

[9. Compatibility & Evolution](#9-compatibility--evolution)  
[9.1 Core Compatibility Rules](#91-core-compatibility-rules)  
[9.2 How to Introduce Breaking Changes](#92-how-to-introduce-breaking-changes)  
[9.3 Recommended Evolution Workflow](#93-recommended-evolution-workflow)

[10. Best Practices](#10-best-practices)  
[10.1 Always Log `X-Request-Id`](#101-always-log-x-request-id)  
[10.2 Deprecation Lifecycle (Field or Endpoint Evolution)](#102-deprecation-lifecycle-field-or-endpoint-evolution)  
[10.3 Response Media Types & Fallbacks](#103-response-media-types--fallbacks)  
[10.4 Security Headers & CORS Policy Recommendations](#104-security-headers--cors-policy-recommendations)  
[10.5 Use `_properties` and `_references` Generously](#105-use-_properties-and-_references-generously)  
[10.6 Operational Logging, Correlation, Monitoring & Security](#106-operational-logging-correlation-monitoring--security)  
[10.7 Security Best Practices](#107-security-best-practices)  
[10.7.1 Error Message Sanitization](#1071-error-message-sanitization)  
[10.7.2 Rate Limiting Error Responses](#1072-rate-limiting-error-responses)  
[10.7.3 Stack Trace Handling](#1073-stack-trace-handling)  
[10.7.4 Sensitive Data in Logs](#1074-sensitive-data-in-logs)  
[10.8 Client Library Guidelines](#108-client-library-guidelines)  
[10.8.1 Retry Strategies](#1081-retry-strategies)  
[10.8.2 Timeout Recommendations](#1082-timeout-recommendations)  
[10.8.3 Malformed Response Handling](#1083-malformed-response-handling)  
[10.8.4 Response Validation](#1084-response-validation)

[11. Appendix](#11-appendix)  
[11.1 Reserved Headers (Response Only)](#111-reserved-headers-response-only)  
[11.2 Reserved Keywords (Top-Level JSON Keys)](#112-reserved-keywords-top-level-json-keys)  
[11.3 Middleware & Utility Patterns](#113-middleware--utility-patterns)  
[11.4 Minimal JSON Schema for the Envelope (Dev Tooling)](#114-minimal-json-schema-for-the-envelope-dev-tooling)  
[11.5 Example cURL Requests (Version & Headers)](#115-example-curl-requests-version--headers)  
[11.6 Developer Notes](#116-developer-notes)

---

# 1. Introduction


JsonDispatch is a **lightweight API response specification** built on top of JSON. It defines a predictable, flexible response envelope for REST APIs so clients always know where to look for the status, data and helpful metadata.

Think of it as the **contract** between your backend and your clients (mobile, web, services). Instead of every project reinventing its own shape, JsonDispatch gives you:

- **Consistency** — The same envelope across all endpoints
- **Traceability** — Every response carries a server-generated `X-Request-Id`
- **Clarity** — Clean separation between `success`, `fail` and `error`
- **Flexibility** — Optional `_references`, `_properties` and `_links` for richer responses

## 1.2 Why another spec?

If you've worked with APIs before, you've probably seen:

- `{ "ok": true }` here
- `{ "status": "success", "payload": … }` there
- And somewhere else… a raw stack trace in JSON. 😬

This chaos makes it hard to build **generic clients**, reason about failures and correlate logs across services. JsonDispatch standardizes the response shape while staying practical and easy to adopt in real systems.

## 1.3 Core Principles

JsonDispatch is built around a few simple rules:

#### Never remove, only add

Responses evolve, but we don't break clients. Deprecate fields instead of deleting them.

#### Trace everything (server-generated IDs)

The server **must** generate and return a unique `X-Request-Id` on every response (clients don't send it). This makes correlation and debugging straightforward.

#### Clear status semantics

- `success` → Everything worked
- `fail` → The request was invalid (validation, preconditions, etc.)
- `error` → The server or a dependency failed

#### Flexible metadata when you need it

- `_references` → Turn IDs into human-friendly values
- `_properties` → Describe the data shape, pagination and deprecations
- `_links` → Make collections navigable

#### Versioned but predictable

- **Response** carries `X-Api-Version` (full SemVer) — clients can log and reason about the exact server implementation.
- **`Accept` stays `application/json`** — clients don't need custom accept negotiation to consume JsonDispatch.

---

# 2. Media types & versioning

As your API evolves, clients need a stable way to understand **which shape they're getting** and how to **migrate** when it changes. JsonDispatch solves this by versioning **request media types** and signaling the **exact server version** in a response header.

## 2.1 Media type explained (with examples)

For requests with a body, set a JsonDispatch vendor media type in `Content-Type`:

```http
Content-Type: application/vnd.infocyph.jd.v1+json
```

### Media type breakdown

- **`application`** → Application payload (static)
- **`vnd.infocyph`** → Your vendor namespace (configurable)
- **`jd`** → JsonDispatch spec identifier (static for this spec)
- **`v1`** → **Major** version of the request format (configurable)
- **`+json`** → JSON syntax suffix (static)

> **Responses** can simply use `Content-Type: application/json` while still following the JsonDispatch envelope.

### Examples

- **Project "Acme"**: `application/vnd.acme.jd.v1+json`
- **Personal/OSS** (not recommended for org APIs): `application/prs.yourname.jd.v1+json`

## 2.2 Versioning strategy (major/minor/patch)

JsonDispatch follows [semantic Versioning](https://semver.org/):
- **Major (v1 → v2)**: Breaking changes to the **envelope or field types**
- **Minor (v1.1 → v1.2)**: Backward-compatible additions
- **Patch (v1.0.0 → v1.0.1)**: Backward-compatible bug fixes

> **Key point**: The **request media type** carries the **major** version: `…jd.v1+json`.
> The server's full version is in `X-Api-Version` (e.g., `1.3.0`).

- **Do not** use `Accept` for version negotiation; keep it `application/json` if you send it at all.

## 2.3 Required & recommended headers

### Requests (with body)

- **MUST** send:
  ```http
  Content-Type: application/vnd.<vendor>.jd.v<MAJOR>+json
  ```
  Example:
  ```http
  Content-Type: application/vnd.infocyph.jd.v1+json
  ```

- **SHOULD NOT** use `Accept` for versioning. If present, keep it:
  ```http
  Accept: application/json
  ```

### Responses

- **MUST** send:
  ```http
  X-Api-Version: <MAJOR.MINOR.PATCH>
  ```
  Example:
  ```http
  X-Api-Version: 1.4.0
  ```

- **MAY** send:
  ```http
  Content-Type: application/json
  ```
  > **Note**: Servers can still set a vendor media type on responses if needed, but `application/json` is sufficient and preferred.

> `X-Request-Id`, `X-Correlation-Id` and other tracing headers are covered in **Section 3**.

### 2.4 Version selection & migration

* The **server controls** the response envelope version. Clients do **not** negotiate via `Accept`.
* When you introduce a **breaking change**, bump the **request** major (e.g., `v1 → v2`) and keep returning
  `application/json` in the response with an updated `X-Api-Version`.

**Create (client → server)**

```http
POST /articles
Content-Type: application/vnd.infocyph.jd.v1+json

{ "title": "Hello JD" }
```

**Response (server → client)**

```http
HTTP/1.1 201 Created
Content-Type: application/json
X-Api-Version: 1.4.0
X-Request-Id: 1f1f6a2e-0c8f-4f7f-9b4b-5d2d0a3f5b99

{
  "status": "success",
  "data": { ... }
}
```

**After a breaking change** (client updates request major):

```http
POST /articles
Content-Type: application/vnd.infocyph.jd.v2+json

{ "title": "Hello JD v2" }
```

**Server response**

```http
HTTP/1.1 201 Created
Content-Type: application/json
X-Api-Version: 2.0.0
X-Request-Id: 6c2a3d7e-9d5a-4b61-9b05-d1d8f6a8f4a1

{
  "status": "success",
  "data": { ... }
}
```

Clients signal **request major** via `Content-Type` (when they send a body) and servers announce the **exact
implementation** via `X-Api-Version` in the **response**. No `Accept` gymnastics and responses stay plain
`application/json`.

### 2.5 Non-JSON responses (reports & exports)

JsonDispatch defines the **response envelope for JSON**. For binary or tabular deliverables (CSV, PDF, ZIP, images), **return the native media type directly** and keep JsonDispatch for **orchestration endpoints** (job creation, metadata, links).

#### 2.5.1 Direct file delivery

When the endpoint returns a file stream:

**Request**

```http
GET /reports/activity/download?from=2025-09-01&to=2025-09-30
Accept: text/csv
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: text/csv
Content-Disposition: attachment; filename="activity-report-2025-09.csv"
X-Api-Version: 1.4.0
X-Request-Id: 7bfae01e-771c-41d4-b1cf-0ad52d8bce19
```

> Use the correct `Content-Type` (e.g., `text/csv`, `application/pdf`, `application/zip`) and add `Content-Disposition` for downloads.

#### 2.5.2 Orchestration via JsonDispatch (recommended)

Create the report **asynchronously** and return a JsonDispatch envelope with status and links:

**Request**

```http
POST /reports/activity
Content-Type: application/vnd.infocyph.jd.v1+json

{ "from": "2025-09-01", "to": "2025-09-30", "format": "csv" }
```

**Response**

```http
HTTP/1.1 202 Accepted
Content-Type: application/json
X-Api-Version: 1.4.0
X-Request-Id: 3b2c7a5a-0b2e-4b69-b1a2-1a2c3d4e5f6a
```

**Body**

```json
{
  "status": "success",
  "message": "Report job accepted",
  "data": {
    "report_id": "rep_9KfGH2",
    "state": "queued",
    "format": "csv",
    "expires_at": "2025-10-31T23:59:59Z"
  },
  "_links": {
    "self": "https://api.example.com/reports/activity/rep_9KfGH2",
    "download": {
      "href": "https://cdn.example.com/reports/rep_9KfGH2.csv",
      "meta": { "method": "GET", "expires": "2025-10-31T23:59:59Z" }
    }
  },
  "_properties": {
    "data": { "type": "object", "name": "report" }
  }
}
```

#### 2.5.3 Streaming & large datasets

For very large exports, consider **streaming** formats:

* **CSV/TSV stream:** `text/csv`
* **NDJSON stream:** `application/x-ndjson`
* **Gzip:** add `Content-Encoding: gzip` when appropriate

Pair streaming/download endpoints with a **JsonDispatch status endpoint** so clients can poll readiness and discover `_links.download`.

**Status polling**

```http
GET /reports/activity/rep_9KfGH2
Accept: application/json
```

**Response (ready)**

```http
HTTP/1.1 200 OK
Content-Type: application/json
X-Api-Version: 1.4.0
X-Request-Id: d1c9b15f-9c1e-42d5-9a9e-8b8e5a2b1c0a
```

**Body**

```json
{
  "status": "success",
  "data": {
    "report_id": "rep_9KfGH2",
    "state": "ready",
    "size_bytes": 9421331
  },
  "_links": {
    "download": "https://cdn.example.com/reports/rep_9KfGH2.csv",
    "retry": "https://api.example.com/reports/activity/rep_9KfGH2/retry"
  }
}
```

> **Rule of thumb:** Use JsonDispatch for **control, status and discovery**; use native media types for the **actual file bytes**.

## 2.6 Authentication & authorization

JsonDispatch APIs typically require authentication. This section defines where authentication credentials should be placed and how authentication failures map to the response envelope.

### 2.6.1 Authentication token placement

**Recommended:** Use the `Authorization` header with a bearer token for API authentication.

```http
GET /api/v1/users/me
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Accept: application/json
```

**Alternative patterns:**

* **API Keys:** `X-Api-Key: your-api-key-here`
* **Basic Auth:** `Authorization: Basic base64(username:password)` (HTTPS only)
* **Cookie-based:** `Cookie: session_id=abc123` (for browser clients)

> **Security note:** Never send credentials in query parameters or URL paths, as they may be logged by proxies, CDNs or web servers.

### 2.6.2 Authentication failure responses

When authentication fails (missing, invalid or expired token), return **`401 Unauthorized`** with a `fail` status.

**Example: Missing token**

```http
HTTP/1.1 401 Unauthorized
Content-Type: application/json
X-Api-Version: 1.4.0
X-Request-Id: f47ac10b-58cc-4372-a567-0e02b2c3d479
WWW-Authenticate: Bearer realm="API"
```

```json
{
  "status": "fail",
  "message": "Authentication required",
  "data": {
    "errors": [
      {
        "field": "Authorization",
        "code": "AUTH_MISSING",
        "message": "No authentication token provided"
      }
    ]
  }
}
```

**Example: Invalid or expired token**

```http
HTTP/1.1 401 Unauthorized
Content-Type: application/json
X-Api-Version: 1.4.0
X-Request-Id: 550e8400-e29b-41d4-a716-446655440000
WWW-Authenticate: Bearer realm="API", error="invalid_token"
```

```json
{
  "status": "fail",
  "message": "Invalid or expired authentication token",
  "data": {
    "errors": [
      {
        "field": "Authorization",
        "code": "AUTH_INVALID",
        "message": "Token signature verification failed"
      }
    ]
  },
  "_links": {
    "refresh": "https://api.example.com/auth/refresh",
    "login": "https://api.example.com/auth/login"
  }
}
```

### 2.6.3 Authorization (403 Forbidden)

When a user is **authenticated** but lacks **permission** to access a resource, return **`403 Forbidden`** with a `fail` status.

```http
HTTP/1.1 403 Forbidden
Content-Type: application/json
X-Api-Version: 1.4.0
X-Request-Id: 6ba7b810-9dad-11d1-80b4-00c04fd430c8
```

```json
{
  "status": "fail",
  "message": "Access denied",
  "data": {
    "errors": [
      {
        "field": "resource",
        "code": "PERMISSION_DENIED",
        "message": "You do not have permission to delete this resource"
      }
    ]
  }
}
```

### 2.6.4 API key authentication

For server-to-server communication, API keys can be used:

```http
GET /api/v1/webhooks
X-Api-Key: sk_live_51H8rQ2eZvKYlo2C8...
Accept: application/json
```

**Failed API key authentication:**

```http
HTTP/1.1 401 Unauthorized
Content-Type: application/json
X-Api-Version: 1.4.0
X-Request-Id: 7c9e6679-7425-40de-944b-e07fc1f90ae7
```

```json
{
  "status": "fail",
  "message": "Invalid API key",
  "data": {
    "errors": [
      {
        "field": "X-Api-Key",
        "code": "INVALID_API_KEY",
        "message": "The provided API key is invalid or has been revoked"
      }
    ]
  }
}
```

### 2.6.5 OAuth 2.0 & token refresh

For OAuth 2.0 flows, expired access tokens should return `401` with a hint to refresh:

```json
{
  "status": "fail",
  "message": "Access token expired",
  "data": {
    "errors": [
      {
        "field": "Authorization",
        "code": "TOKEN_EXPIRED",
        "message": "Access token has expired. Use refresh token to obtain a new one"
      }
    ]
  },
  "_links": {
    "refresh": "https://api.example.com/oauth/token"
  },
  "_properties": {
    "token": {
      "expired_at": "2025-10-22T14:30:00Z",
      "type": "Bearer"
    }
  }
}
```

> **Best practice:** Always include `WWW-Authenticate` header in 401 responses to help clients understand the authentication scheme.

---

# 3. Request & Response Identification

In production, the hardest bugs are the ones you can’t trace.
JsonDispatch enforces **consistent tracing identifiers** on every response so developers can connect logs, monitor
latency and debug across distributed systems — automatically.

### 3.1 `X-Request-Id` – server-generated trace ID

Every **response** must include a globally unique **request identifier** generated by the **server**.
Clients do **not** send this header.

**Rules**

* Generated once per inbound request (UUID v4, ULID or equivalent unique token).
* Must be a **string**.
* Included in **all responses**, including errors.
* Logged internally for correlation in monitoring and debugging.

**Example**

**Client → Server**

```http
GET /articles
Accept: application/json
```

**Server → Client**

```http
HTTP/1.1 200 OK
Content-Type: application/json
X-Api-Version: 1.4.0
X-Request-Id: 7e0e7b45-1e89-4a7f-bbd3-f7ac73fae951
```

👉 When a user reports an issue, the `X-Request-Id` from the response can be searched in logs to reconstruct the full
execution path.

### 3.2 `X-Correlation-Id` – linking related operations

When multiple requests belong to the same business operation (e.g., checkout, batch processing, workflow chains), a
shared **correlation ID** links them together.

**Rules**

* **Optional.**
* May be **provided by a client** or generated at the workflow entry point.
* The server **echoes it** in the response and **propagates** it to any downstream service calls.
* Must be a **string**, unique per logical workflow.

**Example**

**Client → Server**

```http
POST /checkout
Content-Type: application/vnd.infocyph.jd.v1+json
X-Correlation-Id: order-2025-10-05-777

{ "cartId": "C10045" }
```

**Server → Client**

```http
HTTP/1.1 201 Created
Content-Type: application/json
X-Api-Version: 1.4.0
X-Request-Id: 019fb440-4e83-4b1b-bef9-44a80771f181
X-Correlation-Id: order-2025-10-05-777
```

If the checkout flow triggers downstream services (e.g., payments, shipping), each internal call **must reuse** the same
correlation ID.

### 3.3 Distributed tracing (`traceparent`, `tracestate`)

For systems instrumented with distributed-tracing tools such as **OpenTelemetry**, **Jaeger** or **Zipkin**,
JsonDispatch is compatible with the [W3C Trace Context](https://www.w3.org/TR/trace-context/).

These headers complement (not replace) JsonDispatch identifiers:

* **`traceparent`** → carries trace ID and span ID.
* **`tracestate`** → vendor-specific trace metadata.

**Example**

```http
GET /profile
Accept: application/json
traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
tracestate: congo=t61rcWkgMzE
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json
X-Api-Version: 1.4.0
X-Request-Id: 1b0c9d4b-eaa2-40d0-8715-fc93e6fefb99
X-Correlation-Id: session-998877
traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
tracestate: congo=t61rcWkgMzE
```

**Summary**

| Header             | Direction  | Purpose                                  | Required   |
|--------------------|------------|------------------------------------------|------------|
| `X-Request-Id`     | Response → | Unique server-generated request trace ID | ✅ Yes      |
| `X-Correlation-Id` | Both ↔     | Link related requests in a workflow      | ⚪ Optional |
| `X-Api-Version`    | Response → | Server JsonDispatch version identifier   | ✅ Yes      |
| `traceparent`      | Both ↔     | Distributed tracing (W3C)                | ⚪ Optional |
| `tracestate`       | Both ↔     | Vendor-specific tracing metadata         | ⚪ Optional |

### 3.4 Rate limiting

To protect API resources and ensure fair usage, JsonDispatch recommends standard rate limiting headers that inform clients about their current usage and limits.

### 3.4.1 Rate limit headers

Include these headers in **all successful responses** (and optionally in error responses):

**Standard approach (X-prefixed headers):**

| Header                    | Description                                          | Example       |
|---------------------------|------------------------------------------------------|---------------|
| `X-RateLimit-Limit`       | Maximum requests allowed in the current window       | `1000`        |
| `X-RateLimit-Remaining`   | Requests remaining in the current window             | `987`         |
| `X-RateLimit-Reset`       | Unix timestamp when the rate limit resets            | `1698249600`  |
| `X-RateLimit-Window`      | Duration of the rate limit window (optional)         | `3600` (1h)   |

**Example response with rate limit headers:**

```http
HTTP/1.1 200 OK
Content-Type: application/json
X-Api-Version: 1.4.0
X-Request-Id: 9b7f3c2a-4e1d-4f8c-a3b2-1e5d6c8f9a0b
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 987
X-RateLimit-Reset: 1698249600
```

**IETF Draft Standard (optional alternative):**

JsonDispatch also supports the [IETF RateLimit Header Fields draft](https://datatracker.ietf.org/doc/html/draft-ietf-httpapi-ratelimit-headers) which uses non-prefixed headers:

| Header                | Description                                          | Example              |
|-----------------------|------------------------------------------------------|----------------------|
| `RateLimit-Limit`     | Maximum requests allowed in the current window       | `1000`               |
| `RateLimit-Remaining` | Requests remaining in the current window             | `987`                |
| `RateLimit-Reset`     | Seconds until the rate limit resets                  | `3600`               |
| `RateLimit-Policy`    | Rate limit policy definition                         | `1000;w=3600`        |

**Example response with IETF Draft headers:**

```http
HTTP/1.1 200 OK
Content-Type: application/json
X-Api-Version: 1.4.0
X-Request-Id: 9b7f3c2a-4e1d-4f8c-a3b2-1e5d6c8f9a0b
RateLimit-Limit: 1000
RateLimit-Remaining: 987
RateLimit-Reset: 3600
RateLimit-Policy: 1000;w=3600
```

> **Note:** The main difference is that `RateLimit-Reset` uses seconds (delta) while `X-RateLimit-Reset` uses a Unix timestamp. Choose one approach consistently across your API.

**Policy format:**

The `RateLimit-Policy` header describes the rate limit window:
- `1000;w=3600` = 1000 requests per 3600 seconds (1 hour)
- `100;w=60` = 100 requests per 60 seconds (1 minute)
- `10000;w=86400` = 10000 requests per 86400 seconds (24 hours)

**Combined approach (maximum compatibility):**

For maximum compatibility, you may send both header styles:

```http
HTTP/1.1 200 OK
Content-Type: application/json
X-Api-Version: 1.4.0
X-Request-Id: 9b7f3c2a-4e1d-4f8c-a3b2-1e5d6c8f9a0b
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 987
X-RateLimit-Reset: 1698249600
RateLimit-Limit: 1000
RateLimit-Remaining: 987
RateLimit-Reset: 3600
RateLimit-Policy: 1000;w=3600
```

> **Recommendation:** If you're building a new API, prefer the IETF Draft headers as they may become an official standard. For existing APIs, continue with X-prefixed headers for backward compatibility.

### 3.4.2 Rate limit exceeded response

When a client exceeds their rate limit, return **`429 Too Many Requests`** with a `fail` status:

```http
HTTP/1.1 429 Too Many Requests
Content-Type: application/json
X-Api-Version: 1.4.0
X-Request-Id: a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1698249600
Retry-After: 3600
```

```json
{
  "status": "fail",
  "message": "Rate limit exceeded",
  "data": {
    "errors": [
      {
        "code": "RATE_LIMIT_EXCEEDED",
        "message": "You have exceeded the rate limit of 1000 requests per hour"
      }
    ]
  },
  "_properties": {
    "rate_limit": {
      "limit": 1000,
      "remaining": 0,
      "reset_at": "2025-10-22T16:00:00Z",
      "retry_after_seconds": 3600
    }
  },
  "_links": {
    "upgrade": "https://example.com/pricing",
    "docs": "https://docs.example.com/rate-limits"
  }
}
```

> **Note:** Include the `Retry-After` header (in seconds) to tell clients when they can retry.

### 3.4.3 Rate limiting strategies

JsonDispatch supports various rate limiting strategies:

**Per-user rate limiting**

Rate limits tied to authenticated user accounts:

```http
X-RateLimit-Limit: 5000
X-RateLimit-Remaining: 4872
X-RateLimit-Reset: 1698253200
```

**Per-API-key rate limiting**

Different limits for different API keys or service tiers:

```http
X-RateLimit-Limit: 100000
X-RateLimit-Remaining: 99234
X-RateLimit-Reset: 1698253200
```

**Per-endpoint rate limiting**

Some endpoints may have stricter limits than others. Use `_properties` to communicate this:

```json
{
  "status": "success",
  "data": { ... },
  "_properties": {
    "rate_limit": {
      "endpoint_limit": 100,
      "endpoint_remaining": 87,
      "endpoint_window": "60s"
    }
  }
}
```

> **Best practice:** Always log rate limit violations with `X-Request-Id` to identify abusive patterns and help legitimate users understand their usage.

---

# 4. Response Envelope (The Outer Wrapper)

Every JsonDispatch **response** is wrapped in a predictable, minimal envelope.
This gives every API the same shape — regardless of what the data is — making client logic simpler and responses easier
to debug.

The envelope helps you quickly understand:

* what happened (`status`, `message`)
* what’s returned (`data`)
* how to interpret it (`_properties`)
* how to resolve references (`_references`)
* how to navigate further (`_links`)

### 4.1 Top-Level Members at a Glance

A JsonDispatch response body may contain these top-level members:

| Key           | Type   | Required | Purpose                                          |
|---------------|--------|----------|--------------------------------------------------|
| `status`      | string | ✅        | Overall result — `success`, `fail` or `error`   |
| `message`     | string | ⚪        | Short, human-readable explanation                |
| `data`        | mixed  | ⚪        | Main payload (object, array or scalar)          |
| `_references` | object | ⚪        | ID-to-label mapping dictionary                   |
| `_properties` | object | ⚪        | Metadata describing structure, count or schema  |
| `_links`      | object | ⚪        | Navigation links (pagination, related resources) |

> ⚪ = optional, depending on the `status` value and context.

### 4.2 `status` — Success, Fail or Error

The `status` field defines the overall outcome of the request.

* **`success`** → The request completed successfully and data is returned.
* **`fail`** → The client provided invalid input (validation, missing fields, etc.).
* **`error`** → The server or an external dependency failed to process the request.

**Example**

```json
{
  "status": "success",
  "data": {
    "id": 42,
    "title": "JsonDispatch in Action"
  }
}
```

### 4.3 `message` — Keep It Human-Friendly

`message` is a short sentence for humans (not parsers).
Use it as a quick, meaningful summary in logs or UI alerts.

| Context | Example message                  |
|---------|----------------------------------|
| success | `"Article fetched successfully"` |
| fail    | `"Invalid email address"`        |
| error   | `"Payment service unavailable"`  |

### 4.4 `data` — Your Actual Payload

Everything your API returns lives under `data`.
The format should remain **consistent** for the same `(version, method and endpoint)` combination.

| Status  | Expected `data` type | Description                          |
|---------|----------------------|--------------------------------------|
| success | object / array / any | The requested resource(s).           |
| fail    | array                | List of validation issues.           |
| error   | array                | List of system or dependency errors. |

**Example — Success Payload**

```json
"data": {
  "type": "article",
  "attributes": {
    "id": 42,
    "title": "JsonDispatch in Action",
    "category": 1
  }
}
```

### 4.5 `_references` — Turning IDs Into Meaning

Instead of making clients hard-code enums or category lookups, `_references` provides an instant dictionary for ID
resolution.

**Example**

```json
{
  "_references": {
    "category": {
      "1": "News",
      "2": "Tutorial",
      "3": "Opinion"
    }
  }
}
```

Now clients can map `"category": 2` → “Tutorial” without additional API calls.

### 4.6 `_properties` — Describing Data Context

`_properties` gives structure-level metadata that describes your payload — useful for UI builders, pagination or
deprecation notices.

Common keys include:

| Key           | Type   | Purpose                                          |
|---------------|--------|--------------------------------------------------|
| `type`        | string | Resource type (`array`, `object`, etc.)          |
| `name`        | string | Logical name of the resource                     |
| `count`       | int    | Total item count (if paginated)                  |
| `page`        | int    | Current page number (if applicable)              |
| `range`       | string | Item range in current response (e.g., `"21–40"`) |
| `template`    | url    | Optional schema or structure reference           |
| `deprecation` | url    | Optional migration or deprecation notice         |

**Example**

```json
"_properties": {
  "data": {
    "type": "array",
    "name": "articles",
    "count": 20,
    "page": 2,
    "range": "21–40",
    "deprecation": "https://api.example.com/docs/v2/articles"
  }
}
```

### 4.7 `_links` — Pagination and Beyond

`_links` makes your API navigable.
It can include pagination links, related resources or documentation references.

**Example — Pagination**

```json
{
  "_links": {
    "self": "https://api.example.com/articles?page=2",
    "next": "https://api.example.com/articles?page=3",
    "prev": "https://api.example.com/articles?page=1"
  }
}
```

**Example — Related Resources**

```json
{
  "_links": {
    "self": "https://api.example.com/articles/42",
    "author": "https://api.example.com/users/99",
    "comments": "https://api.example.com/articles/42/comments"
  }
}
```

### 4.8 Envelope Summary

| Section       | Purpose                             | Optional |
|---------------|-------------------------------------|----------|
| `status`      | Defines success/fail/error outcome  | ❌ No     |
| `message`     | Human-readable summary              | ⚪ Yes    |
| `data`        | Payload or error details            | ⚪ Yes    |
| `_references` | Lookup tables for enums or IDs      | ⚪ Yes    |
| `_properties` | Metadata about the response         | ⚪ Yes    |
| `_links`      | Pagination or relational navigation | ⚪ Yes    |

👉 Together, these create a consistent, machine-parsable yet human-friendly response pattern across all JsonDispatch
APIs.

---

# 5. Response Examples

Examples are the fastest way to understand JsonDispatch.
Below are common scenarios — **success**, **fail**, **error** and **paginated** responses — exactly as they should
appear in production.

### 5.1 A Simple Success Response

**Request**

```http
GET /articles/42
Accept: application/json
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json
X-Api-Version: 1.3.1
X-Request-Id: aabbccdd-1122-3344-5566-77889900aabb
```

**Body**

```json
{
  "status": "success",
  "message": "Article fetched successfully",
  "data": {
    "type": "article",
    "attributes": {
      "id": 42,
      "title": "JsonDispatch in Action",
      "category": 2
    }
  },
  "_references": {
    "category": {
      "1": "News",
      "2": "Tutorial",
      "3": "Opinion"
    }
  }
}
```

### 5.2 A Fail Response (Validation Issue)

**Request**

```http
POST /articles
Content-Type: application/vnd.infocyph.jd.v1+json
Accept: application/json
```

**Body**

```json
{
  "title": "Hi",
  "category": 5
}
```

**Response**

```http
HTTP/1.1 422 Unprocessable Entity
Content-Type: application/json
X-Api-Version: 1.3.1
X-Request-Id: f4b44a6e-d593-11ec-9d64-0242ac120002
```

**Body**

```json
{
  "status": "fail",
  "message": "Validation failed",
  "data": [
    {
      "status": 422,
      "source": "/data/attributes/title",
      "title": "Title too short",
      "detail": "The title must be at least 5 characters long."
    },
    {
      "status": 422,
      "source": "/data/attributes/category",
      "title": "Invalid category",
      "detail": "Category must be one of: 1, 2, 3."
    }
  ]
}
```

### 5.3 An Error Response (System Failure)

**Request**

```http
GET /articles
Accept: application/json
```

**Response**

```http
HTTP/1.1 503 Service Unavailable
Content-Type: application/json
X-Api-Version: 1.3.1
X-Request-Id: c043e23a-4b26-4a05-96c4-5c60fcc18d50
```

**Body**

```json
{
  "status": "error",
  "message": "Temporary backend outage",
  "code": "ARTICLES_SERVICE_DOWN",
  "data": [
    {
      "status": 503,
      "source": "articles-service",
      "title": "Service unavailable",
      "detail": "The Articles microservice is currently offline."
    }
  ]
}
```

### 5.4 Paginated Collection Response

**Request**

```http
GET /articles?page=2&limit=3
Accept: application/json
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json
X-Api-Version: 1.3.1
X-Request-Id: 77aa88bb-ccdd-eeff-0011-223344556677
```

**Body**

```json
{
  "status": "success",
  "message": "Articles listed successfully",
  "data": [
    {
      "type": "article",
      "attributes": {
        "id": 4,
        "title": "Scaling JsonDispatch",
        "category": 1
      }
    },
    {
      "type": "article",
      "attributes": {
        "id": 5,
        "title": "Error Handling Patterns",
        "category": 3
      }
    },
    {
      "type": "article",
      "attributes": {
        "id": 6,
        "title": "Backward Compatibility Rules",
        "category": 2
      }
    }
  ],
  "_properties": {
    "data": {
      "type": "array",
      "name": "articles",
      "count": 3,
      "page": 2,
      "range": "4–6"
    }
  },
  "_links": {
    "self": "https://api.example.com/articles?page=2&limit=3",
    "next": "https://api.example.com/articles?page=3&limit=3",
    "prev": "https://api.example.com/articles?page=1&limit=3"
  },
  "_references": {
    "category": {
      "1": "News",
      "2": "Tutorial",
      "3": "Opinion"
    }
  }
}
```

### 5.5 References in Action

Clients no longer need to fetch category labels from another endpoint:

```json
"attributes": {
  "id": 42,
  "title": "JsonDispatch in Action",
  "category": 2
}
```

Can be immediately resolved using `_references`:

```json
"_references": {
  "category": {
    "1": "News",
    "2": "Tutorial",
    "3": "Opinion"
  }
}
```

→ **`category: "Tutorial"`**

✅ **Key Takeaways**

* Responses always have `Content-Type: application/json`.
* `X-Api-Version` and `X-Request-Id` are generated by the **server**, not clients.
* The envelope is consistent — clients only need to check `status` and read `data`.


### 5.6 Async & long-running operations

Some operations take too long to complete within a typical HTTP request timeout (e.g., report generation, video processing, batch imports). JsonDispatch provides a consistent pattern for handling asynchronous jobs.

### 5.6.1 Initiating an async job (202 accepted)

When a request is accepted but processing is deferred, return **`202 Accepted`** with job information:

**Request:**

```http
POST /api/v1/reports/quarterly
Content-Type: application/vnd.infocyph.jd.v1+json
Authorization: Bearer eyJhbGci...

{
  "year": 2025,
  "quarter": 3,
  "format": "pdf"
}
```

**Response:**

```http
HTTP/1.1 202 Accepted
Content-Type: application/json
X-Api-Version: 1.4.0
X-Request-Id: 8f3d4e2a-9b1c-4f5e-8a7d-2c3b4d5e6f7a
Location: https://api.example.com/api/v1/jobs/job_7x9Kp2Qm
```

```json
{
  "status": "success",
  "message": "Report generation job created",
  "data": {
    "job_id": "job_7x9Kp2Qm",
    "state": "pending",
    "created_at": "2025-10-22T14:30:00Z",
    "estimated_completion": "2025-10-22T14:35:00Z"
  },
  "_links": {
    "self": "https://api.example.com/api/v1/jobs/job_7x9Kp2Qm",
    "cancel": {
      "href": "https://api.example.com/api/v1/jobs/job_7x9Kp2Qm",
      "meta": { "method": "DELETE" }
    }
  },
  "_properties": {
    "job": {
      "type": "report_generation",
      "priority": "normal",
      "expires_at": "2025-10-29T14:30:00Z"
    }
  }
}
```

> **Key elements:**
> - `Location` header points to the job status endpoint
> - `state` field indicates current job status (`pending`, `processing`, `completed`, `failed`)
> - `_links.self` provides the polling URL

### 5.6.2 Polling for job status

Clients poll the job status URL to check progress:

**Request:**

```http
GET /api/v1/jobs/job_7x9Kp2Qm
Accept: application/json
Authorization: Bearer eyJhbGci...
```

**Response (processing):**

```http
HTTP/1.1 200 OK
Content-Type: application/json
X-Api-Version: 1.4.0
X-Request-Id: 2b3c4d5e-6f7a-4b8c-9d0e-1f2a3b4c5d6e
```

```json
{
  "status": "success",
  "message": "Job is processing",
  "data": {
    "job_id": "job_7x9Kp2Qm",
    "state": "processing",
    "progress": 65,
    "updated_at": "2025-10-22T14:33:00Z"
  },
  "_properties": {
    "progress": {
      "percentage": 65,
      "current_step": "Generating charts",
      "total_steps": 5
    }
  }
}
```

**Response (completed):**

```http
HTTP/1.1 200 OK
Content-Type: application/json
X-Api-Version: 1.4.0
X-Request-Id: 3c4d5e6f-7a8b-4c9d-0e1f-2a3b4c5d6e7f
```

```json
{
  "status": "success",
  "message": "Job completed successfully",
  "data": {
    "job_id": "job_7x9Kp2Qm",
    "state": "completed",
    "completed_at": "2025-10-22T14:34:30Z",
    "result": {
      "file_size": 2458123,
      "file_type": "application/pdf"
    }
  },
  "_links": {
    "download": {
      "href": "https://cdn.example.com/reports/Q3-2025.pdf",
      "meta": {
        "method": "GET",
        "expires_at": "2025-10-29T14:34:30Z"
      }
    }
  }
}
```

> **Polling best practices:**
> - Use exponential backoff (start with 1s, increase to 5s, 10s, 30s)
> - Respect `Retry-After` headers if provided
> - Set a maximum polling duration (e.g., 10 minutes) before timing out

### 5.6.3 Webhook notifications

For better efficiency, clients can register webhooks instead of polling:

**Job creation with webhook:**

```http
POST /api/v1/reports/quarterly
Content-Type: application/vnd.infocyph.jd.v1+json

{
  "year": 2025,
  "quarter": 3,
  "webhook_url": "https://client.example.com/webhooks/reports"
}
```

**Webhook payload (on completion):**

```http
POST /webhooks/reports
Content-Type: application/json
X-Webhook-Signature: sha256=2f5a1b8c...
X-Request-Id: 4d5e6f7a-8b9c-4d0e-1f2a-3b4c5d6e7f8a

{
  "event": "job.completed",
  "job_id": "job_7x9Kp2Qm",
  "state": "completed",
  "completed_at": "2025-10-22T14:34:30Z",
  "_links": {
    "job": "https://api.example.com/api/v1/jobs/job_7x9Kp2Qm",
    "download": "https://cdn.example.com/reports/Q3-2025.pdf"
  }
}
```

> **Security:** Always verify webhook signatures using HMAC-SHA256 or similar.

### 5.6.4 Job failure handling

When a job fails, the status endpoint returns the failure details:

```http
HTTP/1.1 200 OK
Content-Type: application/json
X-Api-Version: 1.4.0
X-Request-Id: 5e6f7a8b-9c0d-4e1f-2a3b-4c5d6e7f8a9b
```

```json
{
  "status": "success",
  "message": "Job status retrieved",
  "data": {
    "job_id": "job_7x9Kp2Qm",
    "state": "failed",
    "failed_at": "2025-10-22T14:33:15Z",
    "error": {
      "code": "INSUFFICIENT_DATA",
      "message": "Unable to generate report: Q3 data is incomplete"
    }
  },
  "_links": {
    "retry": {
      "href": "https://api.example.com/api/v1/reports/quarterly",
      "meta": { "method": "POST" }
    }
  }
}
```

> **Note:** The outer `status` is `success` because the API call to retrieve the job status succeeded. The job's internal `state` is `failed`.

### 5.7 Bulk operations & partial success

When processing multiple items in a single request (e.g., batch create, bulk delete, import operations), some items may succeed while others fail. JsonDispatch provides a consistent pattern for representing partial success scenarios.

### 5.7.1 Partial success response structure

For operations where some items succeed and others fail, use **`207 Multi-Status`** with detailed per-item results:

**Request:**

```http
POST /api/v1/users/bulk
Content-Type: application/vnd.infocyph.jd.v1+json

{
  "users": [
    { "email": "alice@example.com", "name": "Alice" },
    { "email": "bob@example.com", "name": "Bob" },
    { "email": "invalid-email", "name": "Charlie" },
    { "email": "alice@example.com", "name": "Duplicate Alice" }
  ]
}
```

**Response:**

```http
HTTP/1.1 207 Multi-Status
Content-Type: application/json
X-Api-Version: 1.4.0
X-Request-Id: 6f7a8b9c-0d1e-4f2a-3b4c-5d6e7f8a9b0c
```

```json
{
  "status": "success",
  "message": "Bulk operation completed with partial success",
  "data": {
    "summary": {
      "total": 4,
      "succeeded": 2,
      "failed": 2
    },
    "results": [
      {
        "index": 0,
        "status": "success",
        "data": {
          "id": "usr_1A2B3C",
          "email": "alice@example.com"
        }
      },
      {
        "index": 1,
        "status": "success",
        "data": {
          "id": "usr_4D5E6F",
          "email": "bob@example.com"
        }
      },
      {
        "index": 2,
        "status": "fail",
        "errors": [
          {
            "field": "email",
            "code": "INVALID_EMAIL",
            "message": "Invalid email format"
          }
        ]
      },
      {
        "index": 3,
        "status": "fail",
        "errors": [
          {
            "field": "email",
            "code": "DUPLICATE_EMAIL",
            "message": "Email already exists"
          }
        ]
      }
    ]
  },
  "_properties": {
    "data": {
      "type": "bulk_result",
      "operation": "user_creation"
    }
  }
}
```

> **Key elements:**
> - Outer `status` is `success` (the bulk request itself succeeded)
> - `summary` provides aggregate counts
> - Each item in `results` has its own `status` (`success` or `fail`)
> - `index` maps back to the original request array position

### 5.7.2 Atomic vs non-atomic operations

**Atomic operations (all-or-nothing):**

If the operation is transactional and any failure should rollback all changes, return standard error responses:

```http
HTTP/1.1 400 Bad Request
Content-Type: application/json
X-Api-Version: 1.4.0
X-Request-Id: 7a8b9c0d-1e2f-4a3b-4c5d-6e7f8a9b0c1d
```

```json
{
  "status": "fail",
  "message": "Bulk operation failed. No changes were applied",
  "data": {
    "errors": [
      {
        "index": 2,
        "field": "email",
        "code": "INVALID_EMAIL",
        "message": "Invalid email format at index 2"
      }
    ]
  },
  "_properties": {
    "operation": {
      "type": "atomic",
      "rollback": true
    }
  }
}
```

**Non-atomic operations (best-effort):**

Use `207 Multi-Status` as shown in section 5.7.1 when partial success is acceptable.

> **API design tip:** Clearly document in your API specification whether bulk endpoints are atomic or non-atomic.

### 5.7.3 Batch result summary

For large batch operations, consider providing just the summary initially with links to detailed results:

```json
{
  "status": "success",
  "message": "Bulk import completed",
  "data": {
    "batch_id": "batch_9x8y7z",
    "summary": {
      "total": 10000,
      "succeeded": 9847,
      "failed": 153,
      "processing_time_ms": 45230
    }
  },
  "_links": {
    "failures": "https://api.example.com/api/v1/batches/batch_9x8y7z/failures",
    "successes": "https://api.example.com/api/v1/batches/batch_9x8y7z/successes",
    "download_report": "https://api.example.com/api/v1/batches/batch_9x8y7z/report.csv"
  }
}
```

> **Performance tip:** For operations processing >1000 items, use async jobs (section 5.6) instead of synchronous bulk endpoints.

---

# 6. Error Handling
---

# 6. Error Handling

Errors are where consistency matters most.
If every service formats errors differently, debugging turns into chaos.
JsonDispatch enforces a clean, uniform structure for **client-side issues** (`fail`) and **server-side issues** (
`error`) — so you always know where the problem came from.

### 6.1 `fail` vs `error` — Know the Difference

| Type        | Cause                                       | Who Fixes It   | Typical HTTP Status | Example                                 |
|-------------|---------------------------------------------|----------------|---------------------|-----------------------------------------|
| **`fail`**  | The client sent something invalid           | The **client** | 400 – 422           | Missing required fields, invalid format |
| **`error`** | The server or an external dependency failed | The **server** | 500 – 504           | Timeout, DB crash, network outage       |

Think of it like this:

* 🧑‍💻 **fail** → *“Fix your request and try again.”*
* 🧩 **error** → *“It’s not you, it’s us.”*

This split helps:

* **Clients** decide whether to retry or correct their data.
* **Developers** log and alert on real outages separately from validation noise.

### 6.2 Error Object Structure

Both `fail` and `error` responses contain an **array of objects** under `data`.
Each describes one issue in a standard format:

| Field    | Type    | Description                                               |
|----------|---------|-----------------------------------------------------------|
| `status` | integer | HTTP status code for this error                           |
| `source` | string  | Where the problem occurred — field path or subsystem name |
| `title`  | string  | Short summary of the problem                              |
| `detail` | string  | Human-readable explanation for logs or UI                 |

#### Example – Client Validation (`fail`)

```http
HTTP/1.1 422 Unprocessable Entity
Content-Type: application/json
X-Api-Version: 1.3.1
X-Request-Id: 9d2e7f6a-2f3b-45b0-9ff2-dc3d99991234
```

```json
{
  "status": "fail",
  "message": "Validation failed",
  "data": [
    {
      "status": 422,
      "source": "/data/attributes/email",
      "title": "Invalid email",
      "detail": "Email must be a valid address."
    },
    {
      "status": 422,
      "source": "/data/attributes/password",
      "title": "Password too short",
      "detail": "Password must be at least 8 characters."
    }
  ]
}
```

#### Example – Server Outage (`error`)

```http
HTTP/1.1 503 Service Unavailable
Content-Type: application/json
X-Api-Version: 1.3.1
X-Request-Id: e13a97b3-5a2d-46db-a3b2-f401239b0cba
```

```json
{
  "status": "error",
  "message": "Database unavailable",
  "code": "DB_CONN_TIMEOUT",
  "data": [
    {
      "status": 503,
      "source": "db-service",
      "title": "Timeout",
      "detail": "No response from database after 30s."
    }
  ]
}
```

### 6.3 Field-level vs request-level errors

JsonDispatch lets you express **where** an issue occurred so clients can react precisely.

**Two scopes:**

* **Field-level** — a specific input is invalid.
  Use a **JSON Pointer–style path** in `source` (e.g., `/data/attributes/email`).
* **Request-level** — the whole request failed for a non-field reason (rate limit, auth, dependency outage).
  Use a **concise string** naming the subsystem or concern (e.g., `auth`, `rate-limit`, `payments-gateway`).

**Rules**

* Prefer the most **specific** `source` you can provide.
* You **may mix** field-level and request-level items in the same `data` array.
* Keep `title` short; put human-friendly detail in `detail`.
* Don’t leak internals; subsystem names should be stable, public-safe identifiers.

**Examples**

#### Field-level (`fail`)

```json
{
  "status": "fail",
  "message": "Validation failed",
  "data": [
    {
      "status": 422,
      "source": "/data/attributes/email",
      "title": "Invalid email",
      "detail": "Email must be a valid address."
    },
    {
      "status": 422,
      "source": "/data/attributes/age",
      "title": "Out of range",
      "detail": "Age must be between 13 and 120."
    }
  ]
}
```

#### Request-level (`error`)

```json
{
  "status": "error",
  "message": "Upstream dependency unavailable",
  "code": "PAYMENTS_GATEWAY_DOWN",
  "data": [
    {
      "status": 503,
      "source": "payments-gateway",
      "title": "Service unavailable",
      "detail": "No response from provider within 30s."
    }
  ]
}
```

#### Mixed (some fields invalid, plus a request constraint)

```json
{
  "status": "fail",
  "message": "Request cannot be processed",
  "data": [
    {
      "status": 422,
      "source": "/data/attributes/items/0/sku",
      "title": "Unknown SKU",
      "detail": "SKU ABC-123 was not found."
    },
    {
      "status": 429,
      "source": "rate-limit",
      "title": "Too many requests",
      "detail": "Burst limit exceeded; retry after 15 seconds."
    }
  ]
}
```

**Client guidance**

* **Highlight fields** with pointer paths; show inline messages near inputs.
* **Banner or dialog** for request-level issues (`auth`, `rate-limit`, `maintenance`).
* Consider `status` code for **retry/backoff** behavior (see the next subsections).

### 6.4 Error Codes (`code`) — Symbolic and Actionable

The optional top-level `code` field adds a **business-level meaning** beyond the HTTP status.
It’s ideal for client logic, dashboards and automation.

**Guidelines**

* Use uppercase `UPPER_SNAKE_CASE`.
* Keep them short and descriptive.
* Document them in your internal or public API guide.
* Stay consistent across microservices.

**Examples**

| Code                      | Meaning                          |
|---------------------------|----------------------------------|
| `USER_NOT_FOUND`          | The requested user doesn’t exist |
| `DB_CONN_TIMEOUT`         | Database connection timeout      |
| `PAYMENT_GATEWAY_DOWN`    | Payment provider not reachable   |
| `ARTICLE_TITLE_TOO_SHORT` | Validation failure on title      |

### 6.5 Recommended HTTP Status Mapping

| Scenario                                | `status` | HTTP Status     |
|-----------------------------------------|----------|-----------------|
| Read / List / Create / Update Success   | success  | 200 / 201 / 204 |
| Validation error / bad input            | fail     | 400 / 422       |
| Authentication required or failed       | fail     | 401             |
| Forbidden (no permission)               | fail     | 403             |
| Not found                               | fail     | 404             |
| Conflict (duplicate / version mismatch) | fail     | 409             |
| Server exception / crash                | error    | 500             |
| Bad gateway (upstream failure)          | error    | 502             |
| Service unavailable / maintenance       | error    | 503             |
| Upstream timeout                        | error    | 504             |

### 6.6 Key Takeaways

* Clients never send `X-Request-Id` — the server generates it for traceability.
* All error and fail responses share the same envelope shape.
* Each issue in `data[]` must be explicit and readable.
* `code` + `status` + `X-Request-Id` = everything you need for quick debugging.

---

# 7. Properties & References

JsonDispatch goes beyond just returning `status` and `data`.
It introduces two companion sections — `_properties` and `_references` — to make responses **self-descriptive** and *
*context-aware** without extra API calls.

### 7.1 `_properties` — Describe Your Data, Not Just Send It

The `_properties` object carries **metadata about the `data` field**.
It helps clients understand the payload’s structure, count, pagination and even its lifecycle (like deprecation or
schema changes).

| Field         | Type         | Purpose                                                         |
|---------------|--------------|-----------------------------------------------------------------|
| `type`        | string       | Type of data (`array`, `object`, `string`, `number`, `boolean`) |
| `name`        | string       | Logical name for this data block                                |
| `template`    | string (URL) | Optional link to a JSON Schema or template definition           |
| `deprecation` | string (URL) | Optional link marking this resource as deprecated               |
| `count`       | integer      | Total number of items if the data is an array                   |
| `range`       | string       | Range of records in paginated results (e.g., `"21-40"`)         |
| `page`        | integer      | Current page number, if paginated                               |

#### Example

```json
"_properties": {
    "data": {
        "type": "array",
        "name": "articles",
        "count": 20,
        "page": 2,
        "range": "21-40",
        "deprecation": "https://api.example.com/docs/v2/articles"
    }
}
```

This tells the client:

* The `data` is an array named `articles`.
* It contains 20 items, displaying page 2 (items 21–40).
* The endpoint is deprecated in favor of the linked v2 spec.

✅ **Best practice:** Always include at least `type` and `name`.
This enables automated clients (CLI tools, SDKs, data grids) to interpret results correctly.

### 7.2 `_references` — Replace IDs with Meaning

The `_references` object defines **lookup tables** that map internal IDs or codes to human-readable labels.
It eliminates the need for extra “dictionary” or “enum” endpoints.

#### Example

```json
"_references": {
    "category": {
        "1": "News",
        "2": "Tutorial",
        "3": "Opinion"
    },
    "status": {
        "A": "Active",
        "I": "Inactive",
        "S": "Suspended"
    }
}
```

When a record includes `"category": 2`, the client can instantly render **“Tutorial”** using the mapping.

✅ **Best practice:** Keep keys short and meaningful (e.g., `category`, `status`, `role`).
These should directly correspond to the field names inside `data`.

### 7.3 Choosing Between Them

| Use Case                                     | Use `_properties` | Use `_references` |
|----------------------------------------------|-------------------|-------------------|
| Describe structure, pagination or schema    | ✅                 |                   |
| Translate IDs or codes to labels             |                   | ✅                 |
| Mark field as deprecated or link to template | ✅                 |                   |
| Enumerate possible options or states         |                   | ✅                 |

### 7.4 Example — Combined in One Response

```json
{
  "status": "success",
  "message": "Articles listed successfully",
  "data": [
    {
      "id": 1,
      "title": "Intro to JsonDispatch",
      "category": 1
    },
    {
      "id": 2,
      "title": "Error Handling Patterns",
      "category": 3
    }
  ],
  "_properties": {
    "data": {
      "type": "array",
      "name": "articles",
      "count": 2,
      "page": 1,
      "range": "1-2"
    }
  },
  "_references": {
    "category": {
      "1": "News",
      "2": "Tutorial",
      "3": "Opinion"
    }
  }
}
```

Clients can now:

* Display labels directly using `_references`.
* Understand that `data` is paginated and typed via `_properties`.
* Do all this **without extra round-trips** or hard-coded logic.

### 7.5 Nested `_references` Example

Complex datasets often include **hierarchical or multi-level relationships** — e.g. categories, subcategories or status groups.
JsonDispatch supports **nested `_references`** so you can express those relationships cleanly while keeping the payload compact.

This allows clients to resolve **multi-level identifiers** without multiple API calls.

#### Example — Category → Subcategory → Label Mapping

```json
{
  "status": "success",
  "message": "Product list with hierarchical references",
  "data": [
    { "id": 1, "name": "iPhone 15", "category": 10, "subcategory": 101 },
    { "id": 2, "name": "Galaxy S24", "category": 10, "subcategory": 102 },
    { "id": 3, "name": "MacBook Air", "category": 20, "subcategory": 201 }
  ],
  "_references": {
    "category": {
      "10": {
        "label": "Mobile",
        "children": {
          "101": "Apple",
          "102": "Samsung"
        }
      },
      "20": {
        "label": "Laptop",
        "children": {
          "201": "Apple",
          "202": "Windows"
        }
      }
    }
  },
  "_properties": {
    "data": {
      "type": "array",
      "name": "products",
      "count": 3
    }
  }
}
```

#### Explanation

| Field         | Purpose                                                  |
|---------------|----------------------------------------------------------|
| `category`    | Maps high-level IDs (`10`, `20`) to parent labels        |
| `children`    | Maps subcategory IDs to their names under each parent    |
| `label`       | A friendly label for the parent category                 |
| `_references` | Keeps the hierarchy readable and cacheable on the client |

#### Why it matters

* **Fewer round-trips** — clients can render category and subcategory labels directly.
* **Extensible** — future nesting levels (e.g., regions → countries → cities) follow the same pattern.
* **Localized references** — `_references` can hold language-specific labels if needed.

#### Client behavior

When parsing, clients should:

1. Resolve `subcategory` first within its parent `category`.
2. Fallback to top-level label if no match found.
3. Cache `_references` by version to avoid redundant lookups.

✅ **Best practice:**
Use nested `_references` only when relationships are **stable and bounded**. For dynamic trees, prefer dedicated endpoints (`/categories`, `/locations`).

---

# 8. Links

APIs aren’t just about data — they’re about **navigating between resources**.
JsonDispatch provides a `_links` object that helps clients discover where to go next without guessing or relying on
hard-coded routes.

The goal is simple:
➡️ **Make your API self-navigable** — so clients can move through it like a website, not a maze.

### 8.1 `_links` for Pagination

Whenever your response includes a collection or list, include pagination links to guide the client.

| Key     | Purpose                      |
|---------|------------------------------|
| `self`  | URL of the current page      |
| `next`  | Next page (if available)     |
| `prev`  | Previous page (if available) |
| `first` | First page in the dataset    |
| `last`  | Last page in the dataset     |

#### Example

```json
"_links": {
    "self": "https://api.example.com/articles?page=2&limit=10",
    "next": "https://api.example.com/articles?page=3&limit=10",
    "prev": "https://api.example.com/articles?page=1&limit=10",
    "first": "https://api.example.com/articles?page=1&limit=10",
    "last": "https://api.example.com/articles?page=50&limit=10"
}
```

This lets clients paginate seamlessly — no manual query-building or separate pagination logic required.

✅ **Tip:** Include `self` in every response. It makes your payload self-documenting when viewed in isolation.

### 8.2 `_links` for Related Resources

Beyond pagination, `_links` can expose **relationships** or **related resources**.
These hints tell the client where additional or contextual information lives.

#### Example

```json
"_links": {
    "self": "https://api.example.com/articles/42",
    "author": "https://api.example.com/users/99",
    "comments": "https://api.example.com/articles/42/comments",
    "related": "https://api.example.com/tutorials/jsondispatch"
}
```

Now, clients can:

* Navigate to the author or comments without extra documentation.
* Preload related data efficiently.
* Treat your API like a graph of connected resources.

### 8.3 `_links` with Metadata (Enriched Links)

Sometimes you need to describe **how** a link should be used — not just where it points.
In such cases, `_links` entries can be full objects containing an `href` and a `meta` section.

#### Example

```json
"_links": {
  "self": {
    "href": "https://api.example.com/articles/42",
    "meta": {
      "method": "GET",
      "auth": "required"
    }
  },
  "edit": {
    "href": "https://api.example.com/articles/42",
    "meta": {
      "method": "PUT",
      "auth": "editor-role"
    }
  },
  "delete": {
    "href": "https://api.example.com/articles/42",
    "meta": {
      "method": "DELETE",
      "auth": "admin-role"
    }
  }
}
```

This pattern makes `_links` expressive and safe for **HATEOAS-style** APIs.
It tells clients both *where* to go and *how* to interact, without needing extra documentation.

### 8.4 Best Practices for `_links`

* Always include `self`. It’s essential for debugging and introspection.
* Keep URLs **absolute** (never relative).
* Use **consistent naming** (`next`, `prev`, `author`, `related`, `edit`, `delete`, etc.).
* Avoid embedding authentication tokens directly in URLs.
* When possible, pair `_links` with `_properties` to describe pagination metadata (`page`, `count`, etc.).

### 8.5 `_links` for Files and Downloads

APIs frequently serve or reference **files** — such as reports, invoices, exports or media.
JsonDispatch supports this cleanly through `_links`, using either **direct URLs** or **expirable signed URLs** under a dedicated `file` or `download` key.

This keeps your responses self-descriptive, avoids embedding raw file data and enables clients to access assets securely.

#### Example — Direct File Link (Public Resource)

```json
{
  "status": "success",
  "message": "Activity report generated successfully",
  "data": {
    "report_id": "RPT-2025-10-06",
    "type": "activity",
    "period": "2025-09",
    "size": "2.4 MB"
  },
  "_links": {
    "self": "https://api.example.com/reports/RPT-2025-10-06",
    "file": "https://cdn.example.com/reports/RPT-2025-10-06.pdf"
  },
  "_properties": {
    "data": {
      "type": "object",
      "name": "report"
    }
  }
}
```

✅ Use this when files are **public or long-lived** (e.g., CDN-hosted assets or documentation).

#### Example — Signed File Link (Secure or Temporary Access)

```json
{
  "status": "success",
  "message": "Report ready for download",
  "data": {
    "report_id": "RPT-2025-10-06",
    "type": "activity",
    "expires_in": 900
  },
  "_links": {
    "self": "https://api.example.com/reports/RPT-2025-10-06",
    "download": {
      "href": "https://api.example.com/reports/RPT-2025-10-06/download?token=eyJhbGciOiJIUzI1...",
      "meta": {
        "method": "GET",
        "auth": "required",
        "expires": "2025-10-06T12:30:00Z"
      }
    }
  }
}
```

✅ Use this when:

* Files are **user-specific** or **sensitive** (exports, invoices, personal data).
* Links must **expire** or require **authentication**.
* You want to guide clients explicitly on how to fetch the file (via `meta`).

#### Example — Multiple File Formats

```json
{
  "_links": {
    "pdf": "https://cdn.example.com/reports/RPT-2025-10-06.pdf",
    "csv": "https://cdn.example.com/reports/RPT-2025-10-06.csv",
    "json": "https://api.example.com/reports/RPT-2025-10-06.json"
  }
}
```

Clients can choose their preferred format programmatically — ideal for exports or analytics dashboards.

#### Best Practices

| Guideline                                            | Why                                                       |
|------------------------------------------------------|-----------------------------------------------------------|
| Always use HTTPS links                               | Prevents man-in-the-middle interception                   |
| Include `meta` when authentication or expiry applies | Clients can display expiry timers or handle refresh logic |
| Avoid embedding file data inline                     | Reduces payload size and memory footprint                 |
| Prefer `download` over generic link names            | Keeps semantics consistent across endpoints               |

**✅ Summary**

File links under `_links` make your API:

* **Predictable** → consistent structure for downloads
* **Secure** → signed URLs and metadata guidance
* **Portable** → clients can consume them without custom conventions

Perfect — here’s the next addition, **8.6 Inline Media References (Thumbnails, Avatars, etc.)**, written in the same tone, format and Markdown structure as your doc.
It directly complements **8.5 File Link Example**, keeping `_links` consistent across data and media use cases.


### 8.6 `_links` for Inline Media (Thumbnails, Avatars, Previews)

Not every file link is a downloadable document — many APIs include **media previews** such as user avatars, product thumbnails or video stills.
JsonDispatch keeps this consistent by defining them under `_links.media` or `_links.image`, so clients can handle them predictably.

#### Example — Simple Inline Media Links

```json
{
  "status": "success",
  "message": "User profile fetched successfully",
  "data": {
    "id": 99,
    "name": "A. B. M. Mahmudul Hasan",
    "role": "admin"
  },
  "_links": {
    "self": "https://api.example.com/users/99",
    "avatar": "https://cdn.example.com/avatars/99-thumb.jpg"
  },
  "_properties": {
    "data": {
      "type": "object",
      "name": "user"
    }
  }
}
```

✅ Ideal for lightweight references such as **user photos**, **brand icons** or **thumbnail images**.


#### Example — Media with Multiple Resolutions or Types

```json
{
  "_links": {
    "self": "https://api.example.com/products/2001",
    "image": {
      "small": "https://cdn.example.com/products/2001/small.jpg",
      "medium": "https://cdn.example.com/products/2001/medium.jpg",
      "large": "https://cdn.example.com/products/2001/large.jpg"
    }
  }
}
```

Clients can choose which variant to use — perfect for responsive frontends or apps that cache different image sizes.


#### Example — Rich Media Metadata

When returning multiple images, videos or icons, each media entry can include metadata for display and accessibility:

```json
{
  "_links": {
    "thumbnail": {
      "href": "https://cdn.example.com/products/2001/thumb.webp",
      "meta": {
        "width": 120,
        "height": 120,
        "type": "image/webp",
        "alt": "Product preview image"
      }
    },
    "video_preview": {
      "href": "https://cdn.example.com/products/2001/preview.mp4",
      "meta": {
        "duration": 12,
        "type": "video/mp4",
        "poster": "https://cdn.example.com/products/2001/thumb.jpg"
      }
    }
  }
}
```

✅ This allows advanced clients (e.g. web dashboards, mobile apps) to render previews, use proper MIME types and preload efficiently.


#### Best Practices

| Guideline                                                                           | Reason                                       |
| ----------------------------------------------------------------------------------- | -------------------------------------------- |
| Use separate keys for image vs. video (e.g. `avatar`, `thumbnail`, `video_preview`) | Keeps structure clear and predictable        |
| Include `meta.type` for MIME hints (`image/png`, `video/mp4`)                       | Helps browsers and SDKs preload correctly    |
| Prefer WebP or AVIF for image efficiency                                            | Saves bandwidth for clients                  |
| Use `_links` — not `_references` — for any URL-based assets                         | Keeps semantics clean (navigation vs lookup) |


**✅ Summary**

Inline media links under `_links` let APIs describe:

* **Where** assets are located (`href`)
* **What** they are (`meta.type`, `meta.alt`)
* **How** to use them (variants, resolutions, roles)

They make your API **visual-friendly**, **cache-efficient** and **self-documenting** — no guesswork or extra endpoints needed.

---

# 9. Compatibility & Evolution

JsonDispatch is designed for **long-lived APIs** that evolve gracefully without breaking existing clients.
The guiding principle is simple:

> ⚙️ **Evolve forward, never break back.**

### 9.1 Core Compatibility Rules

When making changes to your API responses:

* **Never remove a field.**
  Old clients may still depend on it.

* **Never change the type** of an existing field.
  A string should never become an object and an object should never become an array.

* **Only add new fields** (preferably optional ones with sensible defaults).

* **Deprecate before removing.**
  Mark old fields with `_properties.deprecation` and provide documentation for migration.

#### Example

```json
{
  "_properties": {
    "legacyTitle": {
      "type": "string",
      "name": "legacy-title",
      "deprecation": "https://api.example.com/docs/v2/articles#title"
    }
  }
}
```

This approach ensures:

* Older clients keep working as expected.
* Newer clients can progressively adopt new structures.

### 9.2 How to Introduce Breaking Changes

When a breaking change becomes necessary:

1. Increment the **major version** in the response’s `Content-Type`.

   ```http
   Content-Type: application/vnd.infocyph.jd.v2+json
   X-Api-Version: 2.0.0
   ```

2. Maintain the old major version (v1) in production for a transition period.
   Deprecate it gradually using communication and version headers.

3. Publish updated documentation for each major version side-by-side.

4. Avoid “soft breaks” (changing existing semantics without version bumps). Always be explicit.

### 9.3 Recommended Evolution Workflow

| Step | Action                      | Example                            |
|------|-----------------------------|------------------------------------|
| 1    | Add field                   | Add `_properties.template`         |
| 2    | Mark old field deprecated   | `_properties.oldField.deprecation` |
| 3    | Announce upcoming version   | Changelog + docs                   |
| 4    | Introduce new major version | `v2` media type                    |
| 5    | Sunset old version          | Remove after clients migrate       |

---

# 10. Best Practices

JsonDispatch provides structure — but your team’s discipline keeps it reliable.
These best practices ensure consistency, observability and developer happiness.

### 10.1 Always log `X-Request-Id`

* The **server generates** a unique `X-Request-Id` for each response.
* Include it in all logs, traces and monitoring dashboards.
* When an issue occurs, that single ID traces the request end-to-end.

> ✅ Treat it as your **primary debugging handle**.

### 10.2 Deprecation Lifecycle (Field or Endpoint Evolution)

Deprecation in JsonDispatch isn’t just about marking things as “old.”
It’s about **communicating intent clearly** — to humans and machines — so clients can migrate smoothly without breaking.

Below is the **recommended lifecycle** for any field, structure or endpoint change.

| Phase                           | Description                                                | Duration / Expectation                     | Implementation Pattern                                                     | Example                                                                              |
|:--------------------------------|:-----------------------------------------------------------|:-------------------------------------------|:---------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|
| **1. Active (Default)**         | Field is stable and supported.                             | Ongoing                                    | Regular use; documented and visible.                                       | `"title": "Hello World"`                                                             |
| **2. Announce Deprecation**     | You’ve introduced a replacement field or version.          | 1 release cycle minimum before enforcement | Mark in `_properties.deprecation` with URL + replacement reference.        | `"legacyTitle": { "deprecation": "https://api.example.com/docs/v2/articles#title" }` |
| **3. Dual Support Phase**       | Both old and new fields coexist; clients update gradually. | 1–2 release cycles                         | Continue returning both values; prefer new one in docs and examples.       | Old → `legacyTitle`, New → `title`                                                   |
| **4. Soft Removal (Warn Only)** | Old field still exists but returns a notice or `null`.     | 1 cycle max                                | Include `_properties.legacyTitle.deprecation` + log warnings in responses. | `"legacyTitle": null` + metadata link                                                |
| **5. Hard Removal**             | Field is no longer returned; major version bump required.  | Next major release                         | Remove from payload; update JSON Schema and docs.                          | Removed in `v2`                                                                      |


#### Example — Deprecation Metadata in Action

```json
{
  "status": "success",
  "message": "Article listed with deprecated field notice",
  "data": {
    "id": 42,
    "legacyTitle": "Hello JD (legacy)",
    "title": "Hello JsonDispatch"
  },
  "_properties": {
    "legacyTitle": {
      "type": "string",
      "deprecation": "https://api.example.com/docs/v2/articles#title"
    },
    "title": {
      "type": "string",
      "name": "title"
    }
  }
}
```

✅ The `_properties.legacyTitle.deprecation` URL gives developers a clear migration path — and automated tools can detect deprecation without guessing.


#### Quick Rules of Thumb

| Rule                                          | Why                                     |
| --------------------------------------------- | --------------------------------------- |
| Never remove without prior deprecation notice | Prevents client crashes                 |
| Always provide documentation link             | Enables auto-migration and transparency |
| Keep dual support phase predictable           | Lets clients plan migration windows     |
| Announce removals in release notes            | Keeps API consumers informed            |
| Bundle hard removals with major version bumps | Aligns with Semantic Versioning         |

### 10.3 Response Media Types & Fallbacks

Clients are not required to send vendor-specific `Accept` headers.
Your server defines the media type in responses:

| Header            | Example                               | Description                             |
|-------------------|---------------------------------------|-----------------------------------------|
| **Content-Type**  | `application/vnd.infocyph.jd.v1+json` | Defines the JsonDispatch version in use |
| **X-Api-Version** | `1.3.2`                               | Full semantic version of implementation |

If a client requests plain JSON (`Accept: application/json`), return the **default stable major version** — but still
include the correct headers for transparency.

#### Example

```http
HTTP/1.1 200 OK
Content-Type: application/vnd.infocyph.jd.v1+json
X-Api-Version: 1.3.2
X-Request-Id: b3e9e7c4-9b7b-44c3-a8f3-8c39e612d882
```

### 10.4 Security Headers & CORS Policy Recommendations

Even the most elegant API format is useless if it leaks data or opens up attack surfaces.
JsonDispatch defines **how** you format responses — but your platform must enforce **how** they’re delivered securely.

Below are recommended **security headers**, **CORS patterns** and **exposure rules** that align with JsonDispatch’s design.

#### 10.4.1 Required Security Headers

| Header                          | Example                                        | Purpose                                                                                        |
|:--------------------------------|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------|
| **`Content-Security-Policy`**   | `default-src 'none'; frame-ancestors 'none';`  | Prevents browsers from embedding or executing API responses in iframes or cross-site contexts. |
| **`Strict-Transport-Security`** | `max-age=31536000; includeSubDomains; preload` | Enforces HTTPS and prevents downgrade attacks.                                                 |
| **`X-Content-Type-Options`**    | `nosniff`                                      | Blocks MIME-type sniffing, ensuring `application/json` stays JSON.                             |
| **`X-Frame-Options`**           | `DENY`                                         | Prevents clickjacking or UI redress attacks.                                                   |
| **`Referrer-Policy`**           | `no-referrer`                                  | Avoids leaking private API URLs in browser referrers.                                          |
| **`Cache-Control`**             | `no-store, no-cache, must-revalidate`          | Prevents sensitive responses (e.g., tokens, user info) from being cached.                      |
| **`Permissions-Policy`**        | `geolocation=(), microphone=(), camera=()`     | Locks down API-origin capabilities when served via browsers.                                   |

> **Tip:** You can centralize these headers at reverse proxy level (e.g., Nginx, Caddy or API Gateway) — they don’t need to live inside your application code.

#### 10.4.2 CORS (Cross-Origin Resource Sharing)

If your API is accessed from browsers, define **explicit and minimal** CORS policies.

**Recommended Example**

```http
Access-Control-Allow-Origin: https://app.example.com
Access-Control-Allow-Methods: GET, POST, PUT, PATCH, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type, X-Request-Id, X-Correlation-Id, Authorization
Access-Control-Expose-Headers: X-Request-Id, X-Api-Version, X-Correlation-Id
Access-Control-Max-Age: 600
```

✅ Key points:

* Always **whitelist origins**, never use `*` for authenticated APIs.
* **Expose** `X-Request-Id`, `X-Api-Version` and `X-Correlation-Id` so browser-based clients can log and correlate them.
* Cache preflight (`OPTIONS`) responses to reduce latency.

#### 10.4.3 Authentication & Error Safety

* Never echo back **raw credentials**, tokens or stack traces in `error` responses.
  Use safe `code` and `message` fields instead.

* Return **consistent HTTP status codes** (`401`, `403`) for unauthorized access — don’t over-share.

* When using JWT or HMAC signatures, ensure timestamps and expirations are validated server-side.

* **Log `X-Request-Id` with auth context**, but never include sensitive tokens in the same line — to prevent log correlation attacks.

#### 10.4.4 Example Safe Error Response (Auth Context)

```json
{
  "status": "fail",
  "message": "Authentication required",
  "data": [
    {
      "status": 401,
      "source": "auth-service",
      "title": "Invalid or missing token",
      "detail": "Please provide a valid Authorization header."
    }
  ]
}
```

This tells the user exactly what’s wrong — without exposing internals.

####  10.4.5 Summary: Security Sanity Checklist

| ✅ Task                                       | Why it matters                   |
|----------------------------------------------|----------------------------------|
| HTTPS enforced (`Strict-Transport-Security`) | Prevents MITM attacks            |
| No open `Access-Control-Allow-Origin: *`     | Blocks cross-site token leakage  |
| `nosniff` and `DENY` headers applied         | Stops MIME confusion & framing   |
| Only expose safe headers (`X-*`)             | Prevents internal header leakage |
| Minimal, consistent error structure          | Avoids sensitive info exposure   |


### 10.5 Use `_properties` and `_references` Generously

They’re not fluff — they make your responses **self-describing**.

* `_properties` → guides clients about structure and pagination.
* `_references` → eliminates enum lookups or duplicate API calls.

Example:

```json
{
  "_references": {
    "status": {
      "A": "Active",
      "I": "Inactive"
    }
  },
  "_properties": {
    "data": {
      "type": "array",
      "name": "users",
      "count": 50,
      "page": 1
    }
  }
}
```

### 10.6 Operational Logging, Correlation, Monitoring & Security

JsonDispatch isn’t just a response format — it’s the foundation of your API **observability contract**.
When used consistently, it becomes the single source of truth for **debugging, monitoring, auditing and compliance**.

#### 10.6.1 Unified Structured Logging

Every service should emit structured logs with consistent keys — machine-parseable and human-readable.

| Field              | Source   | Purpose                                      |
|--------------------|----------|----------------------------------------------|
| `timestamp`        | system   | When the event occurred                      |
| `level`            | system   | Severity (`INFO`, `WARN`, `ERROR`)           |
| `service`          | config   | Service name (`checkout-api`, `risk-worker`) |
| `route`            | request  | HTTP method + path                           |
| `status`           | response | HTTP status code                             |
| `duration_ms`      | response | Request duration                             |
| `x_request_id`     | header   | Per-request trace ID                         |
| `x_correlation_id` | header   | Workflow-level trace ID                      |
| `user_id`          | context  | Acting user or system ID                     |
| `remote_ip`        | request  | Client IP (sanitized if needed)              |

**Example log line**

```
[2025-10-06T10:22:51Z] INFO  service=checkout-api
  route=POST /checkout duration=284ms status=201
  request_id=019fb440-4e83-4b1b-bef9-44a80771f181
  correlation_id=order-2025-10-05-777 user_id=U9912
```

✅ **Tip:** Always start each log entry with `request_id` for fast filtering in log pipelines.

#### 10.6.2 Cross-Service Correlation Flow

Each inbound call generates a unique **`X-Request-Id`**, while **`X-Correlation-Id`** persists across the entire workflow.

| Service           | `X-Correlation-Id`     | `X-Request-Id` | Role            |
|-------------------|------------------------|----------------|-----------------|
| `checkout-api`    | `order-2025-10-05-777` | `019f…`        | Entry point     |
| `payment-api`     | Propagated             | `020a…`        | Downstream call |
| `shipping-worker` | Propagated             | `021b…`        | Background task |

```
order-2025-10-05-777
├── [checkout-api] 019f…
├── [payment-api]  020a…
└── [shipping-job] 021b…
```

Search by `correlation_id` to see the entire transaction chain.


#### 10.6.3 Integration with APM & Trace Systems

Attach JsonDispatch IDs to your tracing spans for full observability.

**Example span attributes**

```json
{
  "trace_id": "00f067aa0ba902b7",
  "request_id": "019fb440-4e83-4b1b-bef9-44a80771f181",
  "correlation_id": "order-2025-10-05-777",
  "service.name": "checkout-api",
  "http.status_code": 201,
  "duration_ms": 284
}
```

✅ **Best Practice:** Mirror these IDs in logs, traces and metrics — enabling one-click navigation from error to trace to log line.

#### 10.6.4 Health & Readiness Endpoints

Expose `/health` and `/ready` endpoints using the JsonDispatch envelope.
This ensures monitoring tools receive a consistent, parsable format.

**Example**

```http
GET /health
Accept: application/json
```

```http
HTTP/1.1 200 OK
Content-Type: application/json
X-Api-Version: 1.4.0
X-Request-Id: 44f0d7e2-c9b2-4a61-9b2a-1cf41b922021
```

```json
{
  "status": "success",
  "message": "Service healthy",
  "data": {
    "uptime": "4d 06h 22m",
    "load": 0.21,
    "dependencies": {
      "database": "ok",
      "redis": "ok",
      "queue": "delayed(1)"
    }
  },
  "_properties": {
    "data": { "type": "object", "name": "health" }
  }
}
```

*Return `status:error` with `503` if any dependency fails.*

#### 10.6.5 Metrics & Monitoring Snapshots

Expose lightweight `/metrics` or `/stats` endpoints for quantitative insights.

```json
{
  "status": "success",
  "message": "Metrics snapshot",
  "data": {
    "requests_per_minute": 1240,
    "average_latency_ms": 182,
    "active_users": 341,
    "error_rate_percent": 0.6
  },
  "_properties": {
    "data": {
      "type": "object",
      "name": "metrics",
      "template": "https://spec.infocyph.com/jsondispatch/metrics.schema.json"
    }
  }
}
```

This allows Grafana, Prometheus exporters or custom dashboards to consume metrics in the same JSON format as all other responses.

#### 10.6.6 Security & Audit Hooks

JsonDispatch headers and IDs also power **audit trails** and **forensic analysis**.
Integrate them into your audit subsystem.

**Audit Log Entry Example**

```json
{
  "timestamp": "2025-10-06T11:44:10Z",
  "action": "USER_DELETE",
  "actor_id": "admin-42",
  "target_id": "user-983",
  "result": "success",
  "request_id": "bafc98e0-33a1-41e9-90e4-0234cf19a311",
  "correlation_id": "session-2384",
  "ip": "203.0.113.12"
}
```

**Security Best Practices**

* 🔒 **Mask sensitive fields** (PII, credentials, tokens) before logging.
* 🧩 **Validate `_links` URLs** to prevent malicious injection.
* 🧮 **Use UUIDs or hashes** instead of numeric IDs in responses.
* 🕵️ **Correlate admin actions** via `X-Request-Id` in audit reports.
* 🧱 **Rotate and retain logs** per compliance policy (GDPR, PCI-DSS, ISO 27001).
* 📈 **Trigger alerts** when error rates exceed thresholds, grouped by `service` and `correlation_id`.

#### 10.6.7 Operational Governance Checklist

| Category        | Key Practice                                             | Why It Matters                 |
|-----------------|----------------------------------------------------------|--------------------------------|
| **Tracing**     | Generate `X-Request-Id` for every response               | Root-cause visibility          |
| **Correlation** | Reuse `X-Correlation-Id` across related calls            | End-to-end transaction tracing |
| **Logging**     | Emit structured JSON logs                                | Machine-readable monitoring    |
| **Security**    | Mask sensitive info before logging                       | Data protection & compliance   |
| **Monitoring**  | Return JsonDispatch envelopes for `/health` & `/metrics` | Uniform automation             |
| **Audit**       | Store IDs with every admin or financial action           | Forensic traceability          |
| **Alerts**      | Integrate with APM / log aggregator                      | Real-time anomaly detection    |

✅ **Key Takeaway**

JsonDispatch is not just a response contract — it’s the **observability spine** of your platform.
When tracing, metrics, logs and audits all share the same IDs and envelope style,
your API ecosystem becomes **self-diagnosing, self-auditing and self-healing**.

# 11. Appendix

The Appendix provides **reference materials, reserved conventions and developer tools** for teams implementing or
integrating JsonDispatch.

It’s meant as a **quick lookup section** — not something you memorize, but something you check when building middleware,
validation tools or test clients.

### 11.1 Reserved Headers (Response Only)

These headers are **core to JsonDispatch** and reserved for server responses.
They should **never** be redefined for other purposes.

| Header                           | Direction | Required | Description                                                                           |
|----------------------------------|-----------|----------|---------------------------------------------------------------------------------------|
| **`Content-Type`**               | Response  | ✅        | Defines the JsonDispatch response format (e.g. `application/vnd.infocyph.jd.v1+json`) |
| **`X-Api-Version`**              | Response  | ✅        | Full semantic version of the server’s JsonDispatch implementation                     |
| **`X-Request-Id`**               | Response  | ✅        | Unique identifier generated by the server for this specific request/response          |
| **`X-Correlation-Id`**           | Response  | ⚪        | Optional; groups multiple related requests under one workflow                         |
| **`X-RateLimit-Limit`**          | Response  | ⚪        | Optional; maximum requests allowed in the current window                              |
| **`X-RateLimit-Remaining`**      | Response  | ⚪        | Optional; requests remaining in the current window                                    |
| **`X-RateLimit-Reset`**          | Response  | ⚪        | Optional; Unix timestamp when the rate limit resets                                   |
| **`RateLimit-Limit`**            | Response  | ⚪        | Optional; IETF Draft alternative for maximum requests allowed                         |
| **`RateLimit-Remaining`**        | Response  | ⚪        | Optional; IETF Draft alternative for requests remaining                               |
| **`RateLimit-Reset`**            | Response  | ⚪        | Optional; IETF Draft alternative (seconds until reset, not timestamp)                 |
| **`RateLimit-Policy`**           | Response  | ⚪        | Optional; IETF Draft policy format (e.g., `1000;w=3600`)                              |
| **`Retry-After`**                | Response  | ⚪        | Optional; seconds to wait before retrying (for 429 and 503 responses)                 |
| **`Deprecation`**                | Response  | ⚪        | Optional; indicates the endpoint is deprecated (true or RFC 8594 date)                |
| **`Sunset`**                     | Response  | ⚪        | Optional; RFC 8594 date when the endpoint will be removed                             |
| **`WWW-Authenticate`**           | Response  | ⚪        | Optional; authentication scheme for 401 responses                                     |
| **`traceparent` / `tracestate`** | Response  | ⚪        | Optional; W3C Trace Context headers if distributed tracing is enabled                 |

> ⚠️ Clients **should not** send `X-Request-Id` or `X-Api-Version` —
> these are server-assigned identifiers for traceability and audit purposes.

#### Example (Response Headers)

```http
Content-Type: application/vnd.infocyph.jd.v1+json
X-Api-Version: 1.3.1
X-Request-Id: aabbccdd-1122-3344-5566-77889900aabb
X-Correlation-Id: order-2025-09-30-777
```

If you also use [W3C Trace Context](https://www.w3.org/TR/trace-context/):

```http
traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
tracestate: infocyph=api-2025
```

### 11.2 Reserved Keywords (Top-Level JSON Keys)

JsonDispatch reserves certain top-level fields in the response body.
Avoid reusing them for other meanings.

| Reserved Key  | Purpose                                               |
|---------------|-------------------------------------------------------|
| `status`      | Overall outcome (`success`, `fail`, `error`)          |
| `message`     | Human-readable message                                |
| `data`        | Primary content (object, array or list of errors)     |
| `code`        | Business-level error code (only in `error` responses) |
| `_references` | Lookup tables for IDs → labels                        |
| `_properties` | Metadata describing structure or pagination           |
| `_links`      | Navigational or relational links                      |

If you need more top-level fields, group them under a `meta` object or use prefixed names (e.g. `app_status`).

### 11.3 Middleware & Utility Patterns

JsonDispatch is language-agnostic.
Here’s what a typical implementation might include:

**Middleware responsibilities**

* Attach `Content-Type` and `X-Api-Version`.
* Generate `X-Request-Id` for each request.
* Optionally include `X-Correlation-Id` if workflow-aware.
* Enrich logs and tracing context automatically.

**Response builders**

* Provide helper methods like:

    * `JsonDispatch::success($data, $message)`
    * `JsonDispatch::fail($errors, $message)`
    * `JsonDispatch::error($code, $errors, $message)`
* Automatically append `_links`, `_properties` and `_references` if provided.

**Logging integration**

* Every log entry should carry `X-Request-Id`.
* Distributed logs can also use `X-Correlation-Id` for multi-service correlation.

### 11.4 Minimal JSON Schema for the Envelope (Dev Tooling)

A lightweight JSON Schema to validate **response envelopes**.
This helps test suites and monitoring agents verify that your API always returns valid JsonDispatch shapes.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://spec.infocyph.com/jsondispatch/v1/envelope.schema.json",
  "title": "JsonDispatch v1 Envelope",
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "status": {
      "type": "string",
      "enum": [
        "success",
        "fail",
        "error"
      ]
    },
    "message": {
      "type": "string"
    },
    "code": {
      "type": "string"
    },
    "data": {},
    "_references": {
      "type": "object"
    },
    "_properties": {
      "type": "object"
    },
    "_links": {
      "type": "object"
    }
  },
  "required": [
    "status"
  ]
}
```

This schema validates:

* `status` must always exist.
* Reserved fields must use correct types.
* No unexpected top-level keys.

### 11.5 Example cURL Requests (Version & Headers)

**Basic request (client → server):**

```bash
curl -H 'Accept: application/json' \
  https://api.example.com/articles/42
```

**Server response (JsonDispatch-compliant):**

```http
HTTP/1.1 200 OK
Content-Type: application/vnd.infocyph.jd.v1+json
X-Api-Version: 1.3.1
X-Request-Id: 60c1bbca-b1c8-49d0-b3ea-fe41d23290bd
```

**Body:**

```json
{
  "status": "success",
  "message": "Article fetched successfully",
  "data": {
    "id": 42,
    "title": "JsonDispatch in Action"
  }
}
```

**Request with correlation (for multi-step workflows):**

```bash
curl -H 'Accept: application/json' \
  -H 'X-Correlation-Id: order-2025-10-05-xyz' \
  https://api.example.com/checkout
```

**Server response:**

```http
HTTP/1.1 201 Created
Content-Type: application/vnd.infocyph.jd.v1+json
X-Api-Version: 1.3.1
X-Request-Id: 8d4e2a1b-c821-4b97-8430-44c7b9651d79
X-Correlation-Id: order-2025-10-05-xyz
```

**Body:**

```json
{
  "status": "success",
  "message": "Checkout initiated successfully",
  "data": {
    "order_id": "ORD-2391A",
    "state": "processing"
  }
}
```

### 11.6 Developer Notes

* The server is the **only authority** for JsonDispatch headers.
  Clients may provide `X-Correlation-Id` (optional), but never `X-Request-Id`.

* `Content-Type` defines the **envelope version** (`application/vnd.infocyph.jd.v1+json`).

* Always include `X-Api-Version` in responses — even for errors.

* JsonDispatch responses remain **valid JSON** even for plain `application/json` clients.