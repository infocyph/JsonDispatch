# 11. Appendix

## 11.1 Reserved headers (response only)
Canonical list including `Content-Type`, `X-Api-Version`, `X-Request-Id`, `X-Correlation-Id`, rate-limit fields, `Retry-After`, RFC 8594 `Deprecation`/`Sunset`, W3C trace headers.

## 11.2 Reserved top-level keys
`status`, `message`, `data`, `code`, `_references`, `_properties`, `_links`.

## 11.3 Middleware & utilities
Typical responsibilities and helper builders: `success`, `fail`, `error`.

## 11.4 Minimal JSON Schema (envelope)
A Draft 2020-12 schema to validate envelopes.

## 11.5 Example cURL requests
Versioned and correlation-aware requests and responses.

## 11.6 Developer notes
Servers own the headers; clients never send `X-Request-Id`. Always include `X-Api-Version`.
