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