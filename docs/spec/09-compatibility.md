# 9. Compatibility & Evolution

> Evolve forward, never break back.

## 9.1 Core rules
- Never remove or change types; only add.
- Deprecate with `_properties.deprecation` first.

## 9.2 Breaking changes
- Bump major in request `Content-Type`.
- Operate old and new in parallel during migration.

## 9.3 Evolution workflow
Add → Deprecate → Announce → Introduce vN → Sunset old.
