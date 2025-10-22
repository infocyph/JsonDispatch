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