# JsonDispatch – Developer Guide

Welcome! This site hosts the JsonDispatch specification and examples.

* **What is it?** A lightweight, production-ready JSON **response** spec.
* **Why use it?** Stable envelope (`success`/`fail`/`error`), server-generated tracing with `X-Request-Id`, and clear
  version signaling via `X-Api-Version`.

## Contents

* [1. Introduction](#1-introduction)
* [2. Media Types & Versioning](#2-media-types--versioning)
* [3. Request & Response Identification](#3-request--response-identification)
* [4. Response Envelope (the outer wrapper)](#4-response-envelope-the-outer-wrapper)
* [5. Response Examples](#5-response-examples)
* [6. Error Handling](#6-error-handling)
* [7. Properties & References (power features)](#7-properties--references-power-features)
* [8. Links](#8-links)
* [9. Best Practices](#9-best-practices)
* [10. Appendix](#10-appendix)

---

# 1. Introduction

### 1.1 What is JsonDispatch?

JsonDispatch is a **lightweight API response specification** built on top of JSON.
It defines a predictable, flexible response envelope for REST APIs so clients always know where to look for the status,
data, and helpful metadata.

Think of it as the **contract** between your backend and your clients (mobile, web, services). Instead of every project
reinventing its own shape, JsonDispatch gives you:

* **Consistency** — the same envelope across all endpoints.
* **Traceability** — every response carries a server-generated `X-Request-Id`.
* **Clarity** — clean separation between `success`, `fail`, and `error`.
* **Flexibility** — optional `_references`, `_properties`, and `_links` for richer responses.

### 1.2 Why another spec?

If you’ve worked with APIs before, you’ve probably seen:

* `{ "ok": true }` here,
* `{ "status": "success", "payload": … }` there,
* and somewhere else… a raw stack trace in JSON. 😬

This chaos makes it hard to build **generic clients**, reason about failures, and correlate logs across services.
JsonDispatch standardizes the response shape while staying practical and easy to adopt in real systems.

### 1.3 Core principles

JsonDispatch is built around a few simple rules:

1. **Never remove, only add**
   Responses evolve, but we don’t break clients. Deprecate fields instead of deleting them.

2. **Trace everything (server-generated IDs)**
   The server **must** generate and return a unique `X-Request-Id` on every response (clients don’t send it). This makes
   correlation and debugging straightforward.

3. **Clear status semantics**

    * `success` → everything worked
    * `fail` → the request was invalid (validation, preconditions, etc.)
    * `error` → the server or a dependency failed

4. **Flexible metadata when you need it**

    * `_references` → turn IDs into human-friendly values
    * `_properties` → describe the data shape, pagination, and deprecations
    * `_links` → make collections navigable

5. **Versioned but predictable**

    * **Response** carries `X-Api-Version` (full SemVer) — clients can log and reason about the exact server
      implementation.
    * **Requests** use `Content-Type` to indicate the request body media type (when applicable).
    * **`Accept` stays `application/json`** — clients don’t need custom accept negotiation to consume JsonDispatch.

---

# 2. Media Types & Versioning

As your API evolves, clients need a stable way to understand **which shape they’re getting** and how to **migrate** when
it changes. JsonDispatch solves this by versioning **request media types** and signaling the **exact server version** in
a response header.

---

### 2.1 Media type explained (with examples)

**For requests with a body**, set a JsonDispatch vendor media type in `Content-Type`:

```text
application/vnd.infocyph.jd.v1+json
```

**Breakdown**

* **`application`** → application payload (static)
* **`vnd.infocyph`** → your vendor namespace (configurable)
* **`jd`** → JsonDispatch spec identifier (static for this spec)
* **`v1`** → **major** version of the request format (configurable)
* **`+json`** → JSON syntax suffix (static)

> **Responses** can simply use `Content-Type: application/json` while still following the JsonDispatch envelope.

**Examples**

* Project “Acme”: `application/vnd.acme.jd.v1+json`
* Personal/OSS (not recommended for org APIs): `application/prs.yourname.jd.v1+json`

### 2.2 Versioning strategy (major/minor/patch)

JsonDispatch follows **Semantic Versioning**:

* **Major (v1 → v2)**: breaking changes to the **envelope or field types**.
* **Minor (1.2 → 1.3)**: **add-only** changes (backward compatible).
* **Patch (1.3.0 → 1.3.1)**: text/bug fixes (no structural impact).

**Rules**

* The **request media type** carries the **major**: `…jd.v1+json`.
* The **response** includes `X-Api-Version: <MAJOR.MINOR.PATCH>` so clients can log the exact server version they
  received.
* **Do not** use `Accept` for version negotiation; keep it `application/json` if you send it at all.

### 2.3 Required & recommended headers

**Requests (with body)**

* **MUST** send:
  `Content-Type: application/vnd.<vendor>.jd.v<MAJOR>+json`
  Example: `Content-Type: application/vnd.infocyph.jd.v1+json`

* **SHOULD NOT** use `Accept` for versioning. If present, keep it:
  `Accept: application/json`

**Responses**

* **MUST** send:
  `X-Api-Version: <MAJOR.MINOR.PATCH>` (e.g., `1.4.0`)

* **MAY** send:
  `Content-Type: application/json` *(recommended default)*

  > Servers can still set a vendor media type on responses if they want, but `application/json` is sufficient and
  preferred.

> `X-Request-Id`, `X-Correlation-Id`, and other tracing headers are covered in **Section 3**.

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

Clients signal **request major** via `Content-Type` (when they send a body), and servers announce the **exact
implementation** via `X-Api-Version` in the **response**. No `Accept` gymnastics, and responses stay plain
`application/json`.

---

Excellent — let’s rewrite **Section 3** so it matches your latest protocol rules:

* `X-Request-Id` is **always generated by the server**, not the client.
* `X-Correlation-Id` is optional; it can be **client-supplied or system-propagated**, but never required.
* `X-Api-Version` is **response-only**.
* Requests stay clean (`Accept: application/json`, `Content-Type` for body only).
* Responses remain `application/json`.

---

# 3. Request & Response Identification

In production, the hardest bugs are the ones you can’t trace.
JsonDispatch enforces **consistent tracing identifiers** on every response so developers can connect logs, monitor
latency, and debug across distributed systems — automatically.

### 3.1 `X-Request-Id` – server-generated trace ID

Every **response** must include a globally unique **request identifier** generated by the **server**.
Clients do **not** send this header.

**Rules**

* Generated once per inbound request (UUID v4, ULID, or equivalent unique token).
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

For systems instrumented with distributed-tracing tools such as **OpenTelemetry**, **Jaeger**, or **Zipkin**,
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
| `status`      | string | ✅        | Overall result — `success`, `fail`, or `error`   |
| `message`     | string | ⚪        | Short, human-readable explanation                |
| `data`        | mixed  | ⚪        | Main payload (object, array, or scalar)          |
| `_references` | object | ⚪        | ID-to-label mapping dictionary                   |
| `_properties` | object | ⚪        | Metadata describing structure, count, or schema  |
| `_links`      | object | ⚪        | Navigation links (pagination, related resources) |

> ⚪ = optional, depending on the `status` value and context.

### 4.2 `status` — Success, Fail, or Error

The `status` field defines the overall outcome of the request.

* **`success`** → The request completed successfully, and data is returned.
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
The format should remain **consistent** for the same `(version, method, and endpoint)` combination.

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

`_properties` gives structure-level metadata that describes your payload — useful for UI builders, pagination, or
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
It can include pagination links, related resources, or documentation references.

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

Excellent — here’s **Section 5 (Response Examples)** rewritten to follow your new, final design rules:

✅ Response-only (no request headers like `Accept: application/vnd…`)
✅ Request `Content-Type` is used when the client sends a body
✅ Response `Content-Type` = `application/json`
✅ `X-Request-Id` and `X-Api-Version` are **server-generated only**
✅ Clear, developer-friendly tone with practical examples

---

# 5. Response Examples

Examples are the fastest way to understand JsonDispatch.
Below are common scenarios — **success**, **fail**, **error**, and **paginated** responses — exactly as they should
appear in production.

### 5.1  A Simple Success Response

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

### 5.2  A Fail Response (Validation Issue)

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

### 5.3  An Error Response (System Failure)

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

### 5.4  Paginated Collection Response

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

### 5.5  References in Action

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

### 6.3 Error Codes (`code`) — Symbolic and Actionable

The optional top-level `code` field adds a **business-level meaning** beyond the HTTP status.
It’s ideal for client logic, dashboards, and automation.

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

### 6.4 Recommended HTTP Status Mapping

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

### 6.5 Key Takeaways

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
It helps clients understand the payload’s structure, count, pagination, and even its lifecycle (like deprecation or
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
| Describe structure, pagination, or schema    | ✅                 |                   |
| Translate IDs or codes to labels             |                   | ✅                 |
| Mark field as deprecated or link to template | ✅                 |                   |
| Enumerate possible options or states         |                   | ✅                 |

---

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
  A string should never become an object, and an object should never become an array.

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
These best practices ensure consistency, observability, and developer happiness.

### 10.1 Always log `X-Request-Id`

* The **server generates** a unique `X-Request-Id` for each response.
* Include it in all logs, traces, and monitoring dashboards.
* When an issue occurs, that single ID traces the request end-to-end.

> ✅ Treat it as your **primary debugging handle**.

### 10.2 Deprecating Fields Safely

* Never silently remove or rename fields.
* Mark deprecated ones using `_properties.deprecation`.
* Provide a migration link in the deprecation URL.

#### Example

```json
{
  "_properties": {
    "oldField": {
      "type": "string",
      "name": "legacy",
      "deprecation": "https://api.example.com/docs/v2/legacy"
    }
  }
}
```

This ensures backward compatibility while clearly signaling change.

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

### 10.4 Security & Data Hygiene

JsonDispatch focuses on clarity, but safety comes first.

* **Never leak sensitive internals.**
  Avoid raw DB IDs, stack traces, or system messages.

* **Use UUIDs or opaque tokens** instead of incremental IDs.

* **Validate all `_links` and `_references`.**
  Ensure URLs are trusted and do not allow injection.

* **Keep public error responses minimal.**
  Logs can store detailed stack traces, but responses should remain user-safe.

#### Safe Example

```json
{
  "status": "error",
  "message": "Temporary backend outage",
  "code": "DB_CONN_TIMEOUT",
  "data": [
    {
      "status": 503,
      "source": "db-service",
      "title": "Timeout",
      "detail": "Please try again later."
    }
  ]
}
```

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

# 11. Appendix

The Appendix provides **reference materials, reserved conventions, and developer tools** for teams implementing or
integrating JsonDispatch.

It’s meant as a **quick lookup section** — not something you memorize, but something you check when building middleware,
validation tools, or test clients.

### 11.1 Reserved Headers (Response Only)

These headers are **core to JsonDispatch** and reserved for server responses.
They should **never** be redefined for other purposes.

| Header                           | Direction | Required | Description                                                                           |
|----------------------------------|-----------|----------|---------------------------------------------------------------------------------------|
| **`Content-Type`**               | Response  | ✅        | Defines the JsonDispatch response format (e.g. `application/vnd.infocyph.jd.v1+json`) |
| **`X-Api-Version`**              | Response  | ✅        | Full semantic version of the server’s JsonDispatch implementation                     |
| **`X-Request-Id`**               | Response  | ✅        | Unique identifier generated by the server for this specific request/response          |
| **`X-Correlation-Id`**           | Response  | ⚪        | Optional; groups multiple related requests under one workflow                         |
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
| `data`        | Primary content (object, array, or list of errors)    |
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
* Automatically append `_links`, `_properties`, and `_references` if provided.

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

