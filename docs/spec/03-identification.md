# 3. Request & Response Identification

JsonDispatch enforces **consistent tracing identifiers** on every response for log correlation and distributed tracing.

## 3.1 `X-Request-Id` – server-generated trace ID
Rules:
* Generate per inbound request (UUID v4/ULID).
* Include in **all** responses and logs.
* Clients never send it.

## 3.2 `X-Correlation-Id` – linking related operations
* Optional; may be client-supplied or generated at workflow entry.
* Echo in responses; propagate downstream.

## 3.3 Distributed tracing (`traceparent`, `tracestate`)
Fully compatible with W3C Trace Context / OpenTelemetry, Jaeger, Zipkin.

## 3.4 Rate limiting
Standard `X-RateLimit-*` and IETF `RateLimit-*` headers supported. Includes 429 fail example and strategy guidance (per-user, per-key, per-endpoint).
