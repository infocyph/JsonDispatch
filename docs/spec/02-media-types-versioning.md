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
- **Personal/OSS**: `application/prs.yourname.jd.v1+json`

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

### 2.4 Version selection & migration

* The **server controls** the response envelope version. Clients do **not** negotiate via `Accept`.
* On a **breaking change**, bump the **request** major (e.g., `v1 → v2`) and keep returning `application/json` with updated `X-Api-Version`.

(See the spec for full request/response examples.)

### 2.5 Non-JSON responses (reports & exports)

Use native media types for file bytes and JsonDispatch for **orchestration** (job creation, metadata, links). Includes direct file delivery, async orchestration, and streaming patterns (CSV, NDJSON, gzip).

### 2.6 Authentication & authorization

Use `Authorization: Bearer …` by default. Provides canonical `401`/`403` fail envelopes, API-key flows, and OAuth token refresh examples with safe `WWW-Authenticate` usage.
