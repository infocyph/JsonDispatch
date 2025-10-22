# 10. Best Practices

## 10.1 Always log `X-Request-Id`
Primary debugging handle.

## 10.2 Deprecation lifecycle
Announce, dual-run, soft remove, hard remove with major bump.

## 10.3 Response media types & fallbacks
Prefer vendor media type for requests; always emit `X-Api-Version`.

## 10.4 Security headers & CORS
Harden with CSP, HSTS, nosniff, frame-deny, minimal CORS.

## 10.5 Use `_properties` & `_references` generously
Make responses self-describing.

## 10.6 Operational logging, correlation, monitoring & security
Structured logs, correlation flows, APM spans, health/metrics endpoints, audit hooks, governance checklist.
