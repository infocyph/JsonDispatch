# 1. Introduction

### 1.1 What is JsonDispatch?

JsonDispatch is a **lightweight API response specification** built on top of JSON.
It defines a predictable, flexible response envelope for REST APIs.

Think of it as the **contract** between your backend and your clients (mobile apps, frontends, other services).
Instead of every project reinventing its own response shape, JsonDispatch gives you:

* **Consistency**: same response shape across all endpoints.
* **Traceability**: every response is tied to a unique ID (via headers).
* **Clarity**: clear separation of success, fail and error cases.
* **Flexibility**: support for references, properties and links out of the box.

### 1.2 Why another spec?

If you’ve worked with APIs before, you know the pain:

* One service returns `{ "ok": true }`
* Another returns `{ "status": "success", "payload": … }`
* A third one dumps raw SQL error messages in the body 🤦

This makes it hard to build **generic clients** or debug issues.

There are existing specs like [JSON:API](https://jsonapi.org/), but they can feel heavy or rigid for smaller teams.
JsonDispatch is **inspired by JSON:API** but focuses on:

* **Developer happiness** → easy to adopt and extend.
* **Production realities** → built-in request IDs, error separation, backward compatibility.
* **Minimal learning curve** → you can get started in minutes.

### 1.3 Core principles

JsonDispatch is built around a few simple rules:

1. **Never remove, only add**

    * Responses evolve, but we don’t break clients.
    * Deprecate fields instead of deleting them.
2. **Trace everything**

    * Every response carries a unique `X-Request-Id`.
    * Makes debugging and log correlation much easier.
3. **Clear status semantics**

    * `success` = everything worked.
    * `fail` = client did something wrong (validation, missing data).
    * `error` = server or external system failed.
4. **Flexible metadata**

    * `_references` let you resolve IDs into human-readable values.
    * `_properties` describe the shape and lifecycle of data.
    * `_links` give you pagination and related resource navigation.
5. **Versioned but predictable**

    * API evolution is handled via content negotiation (`Accept` header).
    * Major versions change the envelope; minor versions only add new fields.

---

# 2. Media Types & Versioning

When your API grows, you’ll need a way to **evolve responses without breaking clients**.
JsonDispatch handles this with **media types** and **semantic versioning**.

### 2.1 Media type explained (with examples)

Every API response has a `Content-Type`. With JsonDispatch, you’ll use a **vendor media type** like:

```
application/vnd.infocyph.jd.v1+json
```

**Breakdown**

* **`application`** → application payload
* **`vnd.infocyph`** → vendor namespace (your company/project)
* **`jd`** → JsonDispatch spec identifier (short form)
* **`v1`** → **major** version of the response structure
* **`+json`** → base format is JSON (generic parsers can still handle it)

Even if a client isn’t JsonDispatch-aware, the `+json` suffix ensures it can parse the payload as standard JSON.

### 2.2 Versioning strategy (major/minor/patch)

JsonDispatch follows [Semantic Versioning](https://semver.org/):

* **Major (v1 → v2)**: breaking change in structure (e.g., `data` format changes from object → array).
* **Minor (1.2 → 1.3)**: new fields added (e.g., `_links.previous` introduced).
* **Patch (1.3.0 → 1.3.1)**: bug fixes, text corrections, no structural impact.

**Rule of thumb**:

* Media type (`…v1+json`) → only changes on **major** bumps.
* Header (`X-Api-Version`) → carries full SemVer (major.minor.patch).

### 2.3 Headers you’ll see in every response

Alongside the body, JsonDispatch adds these standard headers:

* **`Content-Type`** → e.g. `application/vnd.infocyph.jd.v1+json`
* **`X-Api-Version`** → full version string, e.g. `1.3.1`
* **`X-Request-Id`** → unique ID for tracing this specific request
* **`X-Correlation-Id`** (optional) → used if this request is part of a workflow or batch

### 2.4 How clients pick the right version (content negotiation)

Clients request the version they want via the `Accept` header:

```http
GET /articles
Accept: application/vnd.infocyph.jd.v1+json
```

Server responds with:

```http
HTTP/1.1 200 OK
Content-Type: application/vnd.infocyph.jd.v1+json
X-Api-Version: 1.3.1
X-Request-Id: 60c1bbca-b1c8-49d0-b3ea-fe41d23290bd
```

The client now knows:

* The response structure is **major v1**.
* The server implementation is at **1.3.1**.
* The request can be traced via `X-Request-Id`.

**Fallback rule:**
If a client only sends `Accept: application/json`, the server should return the **default stable version** (usually the
latest major).

---

# 3. Request & Response Identification

When you’re running APIs in production, the hardest bugs are the ones you can’t trace.
JsonDispatch bakes **tracing identifiers** right into the protocol so every request and response is linkable in your
logs.

### 3.1 `X-Request-Id` – tracing every call

Every request **must** carry a unique identifier.

* **If the client provides one** → the server **must echo it back** unchanged.
* **If the client doesn’t provide one** → the server **must generate one**.

Format:

* UUID, ULID, or any globally unique ID.
* Must be a **string**.

Example:

**Request:**

```http
GET /articles
X-Request-Id: 123e4567-e89b-12d3-a456-426614174000
```

**Response:**

```http
HTTP/1.1 200 OK
X-Request-Id: 123e4567-e89b-12d3-a456-426614174000
Content-Type: application/vnd.infocyph.jd.v1+json
```

👉 With this, you can open your logs and instantly filter all activity for a given request.

### 3.2 `X-Correlation-Id` – linking multiple requests together

Sometimes a single business operation spans multiple requests:

* A mobile app calls your API
* Your API calls three downstream services
* Each downstream service logs separately

To tie these together, use **`X-Correlation-Id`**.

* Clients can generate it at the start of a workflow.
* Servers must propagate it to all downstream calls.
* All responses must echo it back.

Example:

**Client → API**

```http
POST /checkout
X-Correlation-Id: order-2025-09-30-777
```

**API → Payment Service**

```http
POST /charge
X-Correlation-Id: order-2025-09-30-777
```

Now, when debugging an order, you can trace it across all services.

### 3.3 Distributed tracing (Trace Context support)

For larger systems, JsonDispatch recommends supporting [W3C Trace Context](https://www.w3.org/TR/trace-context/):

* **`traceparent`** → defines the trace ID and span ID
* **`tracestate`** → carries vendor-specific metadata

These headers work alongside `X-Request-Id` and `X-Correlation-Id`.
If you already run distributed tracing tools (Jaeger, Zipkin, OpenTelemetry), you can plug JsonDispatch into them
seamlessly.

Example:

```http
GET /profile
X-Request-Id: 60c1bbca-b1c8-49d0-b3ea-fe41d23290bd
X-Correlation-Id: session-998877
traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
tracestate: congo=t61rcWkgMzE
```

---

# 4. Response Envelope (the outer wrapper)

Every JsonDispatch response comes wrapped in a **consistent envelope**.
This way, clients always know where to look for **status, data, errors, references and links**.

### 4.1 Top-level members at a glance

A JsonDispatch response body may contain these keys:

| Key           | Type   | Required | Purpose                                      |
|---------------|--------|----------|----------------------------------------------|
| `status`      | string | ✅        | Overall state: `success`, `fail`, or `error` |
| `message`     | string | ⚪        | Human-friendly explanation                   |
| `data`        | mixed  | ⚪        | Main payload (object, array, scalar)         |
| `_references` | object | ⚪        | Lookup tables for ID → label/value mapping   |
| `_properties` | object | ⚪        | Metadata about fields or groups              |
| `_links`      | object | ⚪        | Links for pagination, navigation, references |

⚪ = optional, depending on status type (see details below).

### 4.2 `status`: success, fail, error

The **most important flag** in the response:

* **`success`** → request completed and data is returned
* **`fail`** → client-side issue (validation, missing data, bad request)
* **`error`** → server-side or external issue (exceptions, dependency failures)

Example:

```json
{
  "status": "success",
  "data": {
    ...
  }
}
```

### 4.3 `message`: keeping it human-friendly

A short, descriptive string for humans (not machines).

* For `success`: `"Data retrieved successfully"`
* For `fail`: `"Invalid email address"`
* For `error`: `"Payment service unavailable"`

👉 Think of it as a log-friendly summary.

### 4.4 `data`: where your payload lives

The actual **response content**.

* For **success**: contains the requested resource(s).
* For **fail**: an array of validation issues.
* For **error**: an array of system errors.

Data must remain **consistent** per `(version, URL, method)` combo — no surprise type swaps.

Example (success):

```json
"data": {
"type": "article",
"source": "self",
"attributes": {
"title": "JsonDispatch in Action",
"category": 1
}
}
```

### 4.5 `_references`: turning IDs into meaning

Instead of forcing clients to hardcode label mappings, provide a dictionary.

Example:

```json
"_references": {
"category": {
"1": "News",
"2": "Tutorial",
"3": "Opinion"
}
}
```

Now clients can display `category: 1` → “News” without extra calls.

### 4.6 `_properties`: describing your data

Properties help describe **metadata** about your payload:

* Type of resource (`array`, `object`, `string`)
* Display name
* Links to templates or deprecation notices
* Pagination hints (count, range, page)

Example:

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

### 4.7 `_links`: pagination and beyond

Links make your API **navigable**.
You can include pagination, related resources, or helpful references.

Example:

```json
"_links": {
"self": "https://api.example.com/articles?page=2",
"next": "https://api.example.com/articles?page=3",
"prev": "https://api.example.com/articles?page=1"
}
```

You’re free to extend with more (e.g., `author`, `related`, `docs`).

---

# 5. Response Examples

Examples are the fastest way to “get” JsonDispatch. Below you’ll find **success, fail, error, pagination and references
in action**.

### 5.1 A simple success response

**Request:**

```http
GET /articles/42
Accept: application/vnd.infocyph.jd.v1+json
```

**Response:**

```http
HTTP/1.1 200 OK
Content-Type: application/vnd.infocyph.jd.v1+json
X-Api-Version: 1.3.1
X-Request-Id: aabbccdd-1122-3344-5566-77889900aabb
```

**Body:**

```json
{
  "status": "success",
  "message": "Article fetched successfully",
  "data": {
    "type": "article",
    "source": "self",
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

### 5.2 A fail response (validation issue)

**Request:**

```http
POST /articles
Accept: application/vnd.infocyph.jd.v1+json
```

**Response:**

```http
HTTP/1.1 422 Unprocessable Entity
Content-Type: application/vnd.infocyph.jd.v1+json
X-Api-Version: 1.3.1
X-Request-Id: f4b44a6e-d593-11ec-9d64-0242ac120002
```

**Body:**

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

### 5.3 An error response (system failure)

**Request:**

```http
GET /articles
Accept: application/vnd.infocyph.jd.v1+json
```

**Response:**

```http
HTTP/1.1 503 Service Unavailable
Content-Type: application/vnd.infocyph.jd.v1+json
X-Api-Version: 1.3.1
X-Request-Id: c043e23a-4b26-4a05-96c4-5c60fcc18d50
```

**Body:**

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

### 5.4 Paginated collection

**Request:**

```http
GET /articles?page=2&limit=3
Accept: application/vnd.infocyph.jd.v1+json
```

**Response:**

```http
HTTP/1.1 200 OK
Content-Type: application/vnd.infocyph.jd.v1+json
X-Api-Version: 1.3.1
X-Request-Id: 77aa88bb-ccdd-eeff-0011-223344556677
```

**Body:**

```json
{
  "status": "success",
  "message": "Articles listed successfully",
  "data": [
    {
      "type": "article",
      "source": "self",
      "attributes": {
        "id": 4,
        "title": "Scaling JsonDispatch",
        "category": 1
      }
    },
    {
      "type": "article",
      "source": "self",
      "attributes": {
        "id": 5,
        "title": "Error Handling Patterns",
        "category": 3
      }
    },
    {
      "type": "article",
      "source": "self",
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
      "range": "4-6"
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

### 5.5 References in action

Notice how clients don’t need to call a second API to resolve category IDs:

```json
"attributes": {"id": 42, "title": "JsonDispatch in Action", "category": 2}
```

Becomes:

```
category → "Tutorial"
```

Thanks to the `_references` object:

```json
"_references": {
"category": {
"1": "News",
"2": "Tutorial",
"3": "Opinion"
}
}
```

---

# 6. Error Handling

Errors are where consistency matters most.
If every service logs errors differently, debugging becomes chaos. JsonDispatch separates **client-side issues** from **server-side issues** so you always know where to look.

### 6.1 The difference between `fail` vs `error`

* **`fail`** → The client sent something invalid.

    * Bad input, missing fields, constraint violations, precondition failed.
    * Think: *“Fix your request and try again.”*
* **`error`** → The server (or an external dependency) failed.

    * Service down, timeout, unhandled exception.
    * Think: *“It’s not you, it’s us.”*

This distinction helps:

* **Clients** → show the right message (validation vs retry later).
* **Developers** → log failures separately from outages.

### 6.2 Error object structure (with examples)

Both `fail` and `error` responses carry **an array of error objects** inside `data`.
Each object can have:

| Field    | Type   | Description                                             |
|----------|--------|---------------------------------------------------------|
| `status` | int    | HTTP status code for this error                         |
| `source` | string | Where the error occurred (field path or subsystem name) |
| `title`  | string | Short label for the error                               |
| `detail` | string | Human-readable explanation                              |

#### Example – Fail (validation error)

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
    }
  ]
}
```

#### Example – Error (system outage)

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

### 6.3 Using error codes effectively

JsonDispatch adds an optional **`code`** field (string) for symbolic error codes:

* Not tied to HTTP status → represents **business meaning**.
* Helps with automation, logging, client-side handling.

Examples:

* `USER_NOT_FOUND`
* `DB_CONN_TIMEOUT`
* `PAYMENT_GATEWAY_DOWN`
* `ARTICLE_TITLE_TOO_SHORT`

**Best practice:**

* Keep them short and UPPER_SNAKE_CASE.
* Document them in your API docs.
* Map them consistently across services.

**HTTP status guidance (quick table):**

| Situation                               | `status` | HTTP status     |
|-----------------------------------------|----------|-----------------|
| OK (read/list/create/update/delete)     | success  | 200 / 201 / 204 |
| Validation error / bad input            | fail     | 400 / 422       |
| Auth required / failed                  | fail     | 401             |
| Forbidden (no permission)               | fail     | 403             |
| Not found                               | fail     | 404             |
| Conflict (duplicate / version mismatch) | fail     | 409             |
| Server crash / exception                | error    | 500             |
| Upstream bad gateway                    | error    | 502             |
| Service unavailable / maintenance       | error    | 503             |
| Upstream timeout                        | error    | 504             |

---

# 7. Properties & References (power features)

JsonDispatch goes beyond a simple status+data envelope.
It gives you two **power features** to make your responses more useful and self-describing:

* **`_properties`** → metadata about the structure and lifecycle of your data.
* **`_references`** → dictionaries that turn IDs into meaningful values.

### 7.1 Properties (`_properties`) – metadata for data groups

The `_properties` object helps describe **how to interpret your data**.
This is especially useful for clients building UIs or caching logic.

Common fields you can include:

| Key           | Type   | Purpose                                                                 |
|---------------|--------|-------------------------------------------------------------------------|
| `type`        | string | The type of resource (`array`, `object`, `string`, `number`, `boolean`) |
| `name`        | string | A unique identifier for the section                                     |
| `template`    | url    | A schema or template reference (optional)                               |
| `deprecation` | url    | A link showing deprecation/migration info (optional)                    |
| `count`       | int    | Number of items if this is an array (optional)                          |
| `range`       | string | Item range in paginated results (e.g.,`"21-40"`)                        |
| `page`        | int    | Current page index (optional)                                           |

#### Example:

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

* You’re looking at an array called `articles`.
* It has 20 items, showing page 2, covering items 21–40.
* And oh, there’s a deprecation notice with a migration path.

### 7.2 References (`_references`) – value lookup tables

The `_references` object provides **ID → value mappings** so clients don’t need hardcoded dictionaries or extra calls.

It’s like saying: *“Whenever you see this ID in the payload, here’s what it actually means.”*

#### Example:

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

So when a resource has `"category": 2`, the client can render **“Tutorial”** immediately.

### 7.3 When to use which

* Use **`_properties`** when you need to **describe the shape** of data.

    * Type, count, pagination, deprecation, schema.
* Use **`_references`** when you need to **translate values**.

    * Categories, statuses, enums, codes → human-readable names.

Clients don’t need to guess and you don’t need to write separate mapping endpoints.

---

# 8. Links

APIs aren’t just about data — they’re about **navigating between resources**.
JsonDispatch uses a `_links` object to make your API responses self-navigable, so clients know where to go next without
guesswork.

### 8.1 Pagination links

When returning a collection (list of items), include pagination links to help clients move around:

* `self` → the current page
* `next` → the next page (if any)
* `prev` → the previous page (if any)
* `first` → the first page
* `last` → the last page

#### Example:

```json
"_links": {
"self": "https://api.example.com/articles?page=2&limit=10",
"next": "https://api.example.com/articles?page=3&limit=10",
"prev": "https://api.example.com/articles?page=1&limit=10",
"first": "https://api.example.com/articles?page=1&limit=10",
"last": "https://api.example.com/articles?page=50&limit=10"
}
```

### 8.2 Resource links

Beyond pagination, you can use `_links` to point to **related resources**.
This makes your API more discoverable without extra documentation.

#### Example:

```json
"_links": {
"self": "https://api.example.com/articles/42",
"author": "https://api.example.com/users/99",
"comments": "https://api.example.com/articles/42/comments",
"related": "https://api.example.com/tutorials/jsondispatch"
}
```

Clients can now fetch the author, comments, or related tutorials just by following the links.

### 8.3 Extending links with metadata

Links can also carry **extra info**.
Instead of just giving a URL, you can include objects with metadata:

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
}
}
```

This makes `_links` more powerful: they don’t just tell clients *where* to go, but also *how* to interact.

---

# 9. Compatibility & Extensions

JsonDispatch isn’t built in isolation. It takes inspiration from [JSON:API](https://jsonapi.org/) — a well-established
spec — but adapts it for **real-world developer needs** like traceability, backward compatibility and richer metadata.

Think of JsonDispatch as:
👉 *“JSON:API-inspired, but production-ready and developer-friendly.”*

### 9.1 How JsonDispatch compares to JSON:API

| Feature           | JSON:API                             | JsonDispatch                                      |
|-------------------|--------------------------------------|---------------------------------------------------|
| Versioning        | Not in body, usually in docs/headers | Explicit via media type +`X-Api-Version`          |
| Request ID        | Not part of spec                     | Mandatory:`X-Request-Id` header                   |
| Status separation | Uses `errors` for all failures       | Distinguishes `fail` (client) vs `error` (server) |
| References        | `relationships` + `included`         | Simple `_references` lookup tables                |
| Metadata          | `meta` (free-form)                   | `_properties` (structured)                        |
| Links             | `links` (standardized)               | `_links` (same idea, extended)                    |
| Backward compat   | Not enforced                         | Strict “never remove, only add” rule              |

### 9.2 What we borrow directly from JSON:API

Whenever JsonDispatch doesn’t define something, we **adopt JSON:API conventions**:

* **Error object format** → our `fail`/`error` data structure matches JSON:API’s `errors` array (`status`, `source`,
  `title`, `detail`).
* **Links** → our `_links` object maps 1:1 with JSON:API’s `links`.
* **Meta** → when `_properties` doesn’t fit, fall back to JSON:API’s `meta` structure.

This ensures that developers familiar with JSON:API will feel at home.

### 9.3 JsonDispatch-only extensions

JsonDispatch goes beyond JSON:API with features designed for production systems:

* **`X-Request-Id`** → every response is traceable.
* **`X-Correlation-Id`** → link multiple requests in a workflow.
* **`_references`** → human-friendly lookups for enums/IDs.
* **`_properties`** → structured metadata (type, name, pagination, deprecation, templates).
* **Backward compatibility rule** → never remove, only add fields.
* **Deprecation support** → via `_properties.deprecation`.

### 9.4 Backward compatibility rules

JsonDispatch is built for long-lived APIs. The golden rule is:

* **Never remove a field.**
* **Never change the type of an existing field.**
* **Only add new fields, with defaults.**
* If something must change → mark old field as deprecated in `_properties` and introduce a new one.

This means:

* Old clients keep working.
* New clients can adopt improvements gradually.

Example:

```json
"_properties": {
"oldField": {
"type": "string",
"name": "legacy-title",
"deprecation": "https://api.example.com/docs/v2/articles#title"
}
}
```

---

# 10. Best Practices

JsonDispatch gives you structure, but how you *use* it makes the difference between a clean, reliable API and a messy
one.
Here are some recommended practices to keep your APIs healthy and developer-friendly.

### 10.1 Always log `X-Request-Id`

* Generate or echo `X-Request-Id` for every request.
* Include it in **all logs**, monitoring dashboards and error reports.
* When a user reports a bug, you can say: *“Give me the request ID”* and instantly trace it through the system.

👉 Treat it as the **primary correlation key** in debugging.

### 10.2 Deprecating fields the safe way

* Don’t remove or rename fields directly.
* Mark them as deprecated using `_properties.deprecation`.
* Point to documentation explaining the replacement.

Example:

```json
"_properties": {
"oldField": {
"type": "string",
"name": "legacy",
"deprecation": "https://api.example.com/docs/v2/legacy"
}
}
```

This way:

* Old clients still work.
* New clients know what to migrate to.

### 10.3 Fallbacks for clients (plain `application/json`)

Not every client will send `Accept: application/vnd...`.

* If a client only requests `application/json`, serve the **latest stable major** version of your API.
* Always include headers:

    * `Content-Type` → which version they actually got
    * `X-Api-Version` → full SemVer

Example:

```http
Content-Type: application/vnd.infocyph.jd.v1+json
X-Api-Version: 1.3.2
```

This ensures compatibility with generic JSON consumers.

### 10.4 Security tips (don’t leak sensitive info)

JsonDispatch is about **clarity**, but not all data should be shared.

* **Never expose internal IDs** (like database primary keys) unless safe. Use UUIDs or hashes instead.
* **Don’t return stack traces** or raw exception messages in `error` responses. Stick to `code`, `title` and `detail`.
* **Validate `_links` and `_references`** to avoid injection of malicious URLs.
* **Keep error messages user-safe** — logs can have full details, responses should not.

Example of safe error response:

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

---

# 11. Appendix

This section collects **reserved items, keywords and resources** that help keep APIs consistent across teams and
projects.

Here’s your updated **Appendix 11.1** with the **Headers quick reference** applied inline.

---

### 11.1 Reserved headers in JsonDispatch

These headers are considered **core to the spec** and should not be repurposed for other meanings:

* **`X-Request-Id`** → unique identifier per request/response (**required**)
* **`X-Correlation-Id`** → links multiple related requests (**optional but recommended**)
* **`X-Api-Version`** → full semantic version of the server’s JsonDispatch implementation (**required**)

⚠️ If you’re already using [W3C Trace Context](https://www.w3.org/TR/trace-context/), you may also see:

* `traceparent`
* `tracestate`

These work alongside, not instead of, JsonDispatch headers.

#### Quick reference

**Request headers:**

```http
Accept: application/vnd.infocyph.jd.v1+json
X-Request-Id: <uuid>
X-Correlation-Id: <string>          ; optional
traceparent: <w3c-trace-context>     ; optional
tracestate: <w3c-trace-state>        ; optional
```

**Response headers:**

```http
Content-Type: application/vnd.infocyph.jd.v1+json
X-Api-Version: 1.3.1
X-Request-Id: <same-as-request-or-generated>
X-Correlation-Id: <echo-if-present>
```

### 11.2 Reserved keywords in responses

JsonDispatch uses specific keys in the response body.
To avoid conflicts, **do not use these at the top level** for unrelated purposes:

* `status`
* `message`
* `data`
* `_references`
* `_properties`
* `_links`
* `code` (only in error responses)

If you need additional top-level fields, use a prefix or group them under `meta` (borrowed from JSON:API).

### 11.3 Useful libraries & middleware

JsonDispatch is format-agnostic — you can implement it in any language.
Here are common helpers you might want to provide (or build):

* **Middleware** (PSR-15 style for PHP, Express middleware for Node.js, etc.) to:

    * Generate/propagate `X-Request-Id` and `X-Correlation-Id`.
    * Attach `X-Api-Version`.
* **Response builders** that:

    * Provide helpers for `success()`, `fail()`, `error()` responses.
    * Attach `_references`, `_properties` and `_links` consistently.
* **Logging utilities** to ensure every log line contains `X-Request-Id` and (if available) `X-Correlation-Id`.

### 11.4 Minimal JSON Schema for the Envelope (dev tooling)

A minimal JSON Schema for validating the **JsonDispatch response envelope**.
Use this as a base; you can extend it with stricter `data` schemas per endpoint.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://spec.infocyph.com/jsondispatch/v1/envelope.schema.json",
  "title": "JsonDispatch v1 Envelope",
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "status": { "type": "string", "enum": ["success", "fail", "error"] },
    "message": { "type": "string" },
    "code": { "type": "string" },
    "data": {},
    "_references": { "type": "object" },
    "_properties": { "type": "object" },
    "_links": { "type": "object" }
  },
  "required": ["status"]
}
```

This schema ensures:

* `status` is always present and valid.
* Other fields are optional but must be of the correct type.


### 11.5 Example Requests with cURL (content negotiation)

Developers can test version negotiation easily with `curl`.

**Request explicit version:**

```bash
curl -H 'Accept: application/vnd.infocyph.jd.v1+json' \
     -H 'X-Request-Id: 123e4567-e89b-12d3-a456-426614174000' \
     https://api.example.com/articles/42
```

**Response:**

```http
HTTP/1.1 200 OK
Content-Type: application/vnd.infocyph.jd.v1+json
X-Api-Version: 1.3.1
X-Request-Id: 123e4567-e89b-12d3-a456-426614174000
```

**Fallback with plain JSON:**

```bash
curl -H 'Accept: application/json' \
     https://api.example.com/articles/42
```

**Server response (still JsonDispatch under the hood):**

```http
HTTP/1.1 200 OK
Content-Type: application/vnd.infocyph.jd.v1+json
X-Api-Version: 1.3.1
X-Request-Id: 77aa88bb-ccdd-eeff-0011-223344556677
```

