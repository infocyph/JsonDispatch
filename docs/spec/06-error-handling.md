# 6. Error Handling

Consistency matters most during failures.

## 6.1 `fail` vs `error`
- **fail** → client issues (400–422). Client must fix.
- **error** → server/dependency issues (500–504). Server must fix.

## 6.2 Error object structure
Each item in `data[]`:
- `status` (int)
- `source` (field path or subsystem)
- `title` (short)
- `detail` (human-readable)

## 6.3 Field-level vs request-level errors
Use JSON Pointer-style paths for fields; concise subsystem names for request-level concerns.

## 6.4 Error `code`
Upper snake case business codes; keep consistent across services.

## 6.5 HTTP status mapping
Clear matrix for common scenarios (auth, conflict, outages, etc.).

## 6.6 Takeaways
`code` + `status` + `X-Request-Id` = fast debugging.
