10. Best Practices
==================

JsonDispatch provides structure — but your team’s discipline keeps it reliable.
These best practices ensure consistency, observability and developer happiness.


10.1 Always log ``X-Request-Id``
--------------------------------

- The **server generates** a unique ``X-Request-Id`` for each response.
- Include it in all logs, traces and monitoring dashboards.
- When an issue occurs, that single ID traces the request end-to-end.

.. tip::
   Treat ``X-Request-Id`` as your **primary debugging handle**.


10.2 Deprecation Lifecycle (Field or Endpoint Evolution)
--------------------------------------------------------

Deprecation in JsonDispatch isn’t just about marking things as “old.”
It’s about **communicating intent clearly** — to humans and machines — so clients can migrate smoothly without breaking.

Below is the **recommended lifecycle** for any field, structure or endpoint change.

.. list-table::
   :header-rows: 1
   :widths: 18 32 20 30 40

   * - Phase
     - Description
     - Duration / Expectation
     - Implementation Pattern
     - Example
   * - **1. Active (Default)**
     - Field is stable and supported.
     - Ongoing
     - Regular use; documented and visible.
     - ``"title": "Hello World"``
   * - **2. Announce Deprecation**
     - You’ve introduced a replacement field or version.
     - 1 release cycle minimum before enforcement
     - Mark in ``_properties.deprecation`` with URL + replacement reference.
     - ``"legacyTitle": {"deprecation": "https://api.example.com/docs/v2/articles#title"}``
   * - **3. Dual Support Phase**
     - Both old and new fields coexist; clients update gradually.
     - 1–2 release cycles
     - Continue returning both values; prefer new one in docs and examples.
     - Old → ``legacyTitle``, New → ``title``
   * - **4. Soft Removal (Warn Only)**
     - Old field still exists but returns a notice or ``null``.
     - 1 cycle max
     - Include ``_properties.legacyTitle.deprecation`` + log warnings in responses.
     - ``"legacyTitle": null`` + metadata link
   * - **5. Hard Removal**
     - Field is no longer returned; major version bump required.
     - Next major release
     - Remove from payload; update JSON Schema and docs.
     - Removed in ``v2``

**Example — Deprecation Metadata in Action**

.. code-block:: json

   {
     "status": "success",
     "message": "Article listed with deprecated field notice",
     "data": {
       "id": 42,
       "legacyTitle": "Hello JD (legacy)",
       "title": "Hello JsonDispatch"
     },
     "_properties": {
       "legacyTitle": {
         "type": "string",
         "deprecation": "https://api.example.com/docs/v2/articles#title"
       },
       "title": {
         "type": "string",
         "name": "title"
       }
     }
   }

**Quick Rules of Thumb**

.. list-table::
   :header-rows: 1
   :widths: 42 58

   * - Rule
     - Why
   * - Never remove without prior deprecation notice
     - Prevents client crashes
   * - Always provide documentation link
     - Enables auto-migration and transparency
   * - Keep dual support phase predictable
     - Lets clients plan migration windows
   * - Announce removals in release notes
     - Keeps API consumers informed
   * - Bundle hard removals with major version bumps
     - Aligns with Semantic Versioning


10.3 Response Media Types & Fallbacks
-------------------------------------

Clients are not required to send vendor-specific ``Accept`` headers.
Your server defines the media type in responses:

.. list-table::
   :header-rows: 1
   :widths: 24 40 36

   * - Header
     - Example
     - Description
   * - **Content-Type**
     - ``application/vnd.infocyph.jd.v1+json``
     - Defines the JsonDispatch version in use
   * - **X-Api-Version**
     - ``1.3.2``
     - Full semantic version of implementation

If a client requests plain JSON (``Accept: application/json``), return the **default stable major version** — but still
include the correct headers for transparency.

**Example**

.. code-block:: http

   HTTP/1.1 200 OK
   Content-Type: application/vnd.infocyph.jd.v1+json
   X-Api-Version: 1.3.2
   X-Request-Id: b3e9e7c4-9b7b-44c3-a8f3-8c39e612d882


10.4 Security Headers & CORS Policy Recommendations
---------------------------------------------------

Even the most elegant API format is useless if it leaks data or opens up attack surfaces.
JsonDispatch defines **how** you format responses — but your platform must enforce **how** they’re delivered securely.

Below are recommended **security headers**, **CORS patterns** and **exposure rules** that align with JsonDispatch’s design.

10.4.1 Required Security Headers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 28 40 32

   * - Header
     - Example
     - Purpose
   * - ``Content-Security-Policy``
     - ``default-src 'none'; frame-ancestors 'none';``
     - Prevents browsers from embedding or executing API responses in iframes or cross-site contexts.
   * - ``Strict-Transport-Security``
     - ``max-age=31536000; includeSubDomains; preload``
     - Enforces HTTPS and prevents downgrade attacks.
   * - ``X-Content-Type-Options``
     - ``nosniff``
     - Blocks MIME-type sniffing, ensuring ``application/json`` stays JSON.
   * - ``X-Frame-Options``
     - ``DENY``
     - Prevents clickjacking or UI redress attacks.
   * - ``Referrer-Policy``
     - ``no-referrer``
     - Avoids leaking private API URLs in browser referrers.
   * - ``Cache-Control``
     - ``no-store, no-cache, must-revalidate``
     - Prevents sensitive responses from being cached.
   * - ``Permissions-Policy``
     - ``geolocation=(), microphone=(), camera=()``
     - Locks down API-origin capabilities in browsers.

.. tip::
   You can centralize these headers at the reverse proxy (Nginx, Caddy, API Gateway) — they don’t need to live inside application code.

10.4.2 CORS (Cross-Origin Resource Sharing)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If your API is accessed from browsers, define **explicit and minimal** CORS policies.

**Recommended Example**

.. code-block:: http

   Access-Control-Allow-Origin: https://app.example.com
   Access-Control-Allow-Methods: GET, POST, PUT, PATCH, DELETE, OPTIONS
   Access-Control-Allow-Headers: Content-Type, X-Request-Id, X-Correlation-Id, Authorization
   Access-Control-Expose-Headers: X-Request-Id, X-Api-Version, X-Correlation-Id
   Access-Control-Max-Age: 600

Key points:

- Always **whitelist origins**, never use ``*`` for authenticated APIs.
- **Expose** ``X-Request-Id``, ``X-Api-Version`` and ``X-Correlation-Id`` so browser-based clients can log and correlate them.
- Cache preflight (``OPTIONS``) responses to reduce latency.

10.4.3 Authentication & Error Safety
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Never echo back **raw credentials**, tokens or stack traces in ``error`` responses. Use safe ``code`` and ``message`` fields.
- Return **consistent HTTP status codes** (``401``, ``403``) for unauthorized access — don’t over-share.
- When using JWT or HMAC signatures, ensure timestamps and expirations are validated server-side.
- **Log ``X-Request-Id`` with auth context**, but never include sensitive tokens in the same line.

**Example Safe Error Response (Auth Context)**

.. code-block:: json

   {
     "status": "fail",
     "message": "Authentication required",
     "data": [
       {
         "status": 401,
         "source": "auth-service",
         "title": "Invalid or missing token",
         "detail": "Please provide a valid Authorization header."
       }
     ]
   }

10.4.5 Summary: Security Sanity Checklist
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - ✅ Task
     - Why it matters
   * - HTTPS enforced (``Strict-Transport-Security``)
     - Prevents MITM attacks
   * - No open ``Access-Control-Allow-Origin: *``
     - Blocks cross-site token leakage
   * - ``nosniff`` and ``DENY`` headers applied
     - Stops MIME confusion & framing
   * - Only expose safe headers (``X-*``)
     - Prevents internal header leakage
   * - Minimal, consistent error structure
     - Avoids sensitive info exposure


10.5 Use ``_properties`` and ``_references`` Generously
-------------------------------------------------------

They’re not fluff — they make your responses **self-describing**.

- ``_properties`` → guides clients about structure and pagination.
- ``_references`` → eliminates enum lookups or duplicate API calls.

**Example**

.. code-block:: json

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


10.6 Operational Logging, Correlation, Monitoring & Security
------------------------------------------------------------

JsonDispatch isn’t just a response format — it’s the foundation of your API **observability contract**.
When used consistently, it becomes the single source of truth for **debugging, monitoring, auditing and compliance**.

10.6.1 Unified Structured Logging
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Every service should emit structured logs with consistent keys — machine-parseable and human-readable.

.. list-table::
   :header-rows: 1
   :widths: 28 12 60

   * - Field
     - Source
     - Purpose
   * - ``timestamp``
     - system
     - When the event occurred
   * - ``level``
     - system
     - Severity (``INFO``, ``WARN``, ``ERROR``)
   * - ``service``
     - config
     - Service name (``checkout-api``, ``risk-worker``)
   * - ``route``
     - request
     - HTTP method + path
   * - ``status``
     - response
     - HTTP status code
   * - ``duration_ms``
     - response
     - Request duration
   * - ``x_request_id``
     - header
     - Per-request trace ID
   * - ``x_correlation_id``
     - header
     - Workflow-level trace ID
   * - ``user_id``
     - context
     - Acting user or system ID
   * - ``remote_ip``
     - request
     - Client IP (sanitized if needed)

**Example log line**

.. code-block:: text

   [2025-10-06T10:22:51Z] INFO  service=checkout-api
     route=POST /checkout duration=284ms status=201
     request_id=019fb440-4e83-4b1b-bef9-44a80771f181
     correlation_id=order-2025-10-05-777 user_id=U9912

.. tip::
   Always start each log entry with ``request_id`` for fast filtering in log pipelines.

10.6.2 Cross-Service Correlation Flow
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Each inbound call generates a unique **``X-Request-Id``**, while **``X-Correlation-Id``** persists across the entire workflow.

.. list-table::
   :header-rows: 1
   :widths: 28 36 20 16

   * - Service
     - ``X-Correlation-Id``
     - ``X-Request-Id``
     - Role
   * - ``checkout-api``
     - ``order-2025-10-05-777``
     - ``019f…``
     - Entry point
   * - ``payment-api``
     - Propagated
     - ``020a…``
     - Downstream call
   * - ``shipping-worker``
     - Propagated
     - ``021b…``
     - Background task

.. code-block:: text

   order-2025-10-05-777
   ├── [checkout-api] 019f…
   ├── [payment-api]  020a…
   └── [shipping-job] 021b…

Search by ``correlation_id`` to see the entire transaction chain.

10.6.3 Integration with APM & Trace Systems
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Attach JsonDispatch IDs to your tracing spans for full observability.

**Example span attributes**

.. code-block:: json

   {
     "trace_id": "00f067aa0ba902b7",
     "request_id": "019fb440-4e83-4b1b-bef9-44a80771f181",
     "correlation_id": "order-2025-10-05-777",
     "service.name": "checkout-api",
     "http.status_code": 201,
     "duration_ms": 284
   }

.. tip::
   Mirror these IDs in logs, traces and metrics — enabling one-click navigation from error to trace to log line.

10.6.4 Health & Readiness Endpoints
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Expose ``/health`` and ``/ready`` endpoints using the JsonDispatch envelope.

**Example**

.. code-block:: http

   GET /health
   Accept: application/json

.. code-block:: http

   HTTP/1.1 200 OK
   Content-Type: application/json
   X-Api-Version: 1.4.0
   X-Request-Id: 44f0d7e2-c9b2-4a61-9b2a-1cf41b922021

.. code-block:: json

   {
     "status": "success",
     "message": "Service healthy",
     "data": {
       "uptime": "4d 06h 22m",
       "load": 0.21,
       "dependencies": {
         "database": "ok",
         "redis": "ok",
         "queue": "delayed(1)"
       }
     },
     "_properties": {
       "data": { "type": "object", "name": "health" }
     }
   }

*Return ``status:error`` with ``503`` if any dependency fails.*

10.6.5 Metrics & Monitoring Snapshots
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Expose lightweight ``/metrics`` or ``/stats`` endpoints for quantitative insights.

.. code-block:: json

   {
     "status": "success",
     "message": "Metrics snapshot",
     "data": {
       "requests_per_minute": 1240,
       "average_latency_ms": 182,
       "active_users": 341,
       "error_rate_percent": 0.6
     },
     "_properties": {
       "data": {
         "type": "object",
         "name": "metrics",
         "template": "https://spec.infocyph.com/jsondispatch/metrics.schema.json"
       }
     }
   }

This allows Grafana, Prometheus exporters or custom dashboards to consume metrics in the same JSON format as all other responses.

10.6.6 Security & Audit Hooks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

JsonDispatch headers and IDs also power **audit trails** and **forensic analysis**.

**Audit Log Entry Example**

.. code-block:: json

   {
     "timestamp": "2025-10-06T11:44:10Z",
     "action": "USER_DELETE",
     "actor_id": "admin-42",
     "target_id": "user-983",
     "result": "success",
     "request_id": "bafc98e0-33a1-41e9-90e4-0234cf19a311",
     "correlation_id": "session-2384",
     "ip": "203.0.113.12"
   }

**Security Best Practices**

- 🔒 **Mask sensitive fields** (PII, credentials, tokens) before logging.
- 🧩 **Validate ``_links`` URLs** to prevent malicious injection.
- 🧮 **Use UUIDs or hashes** instead of numeric IDs in responses.
- 🕵️ **Correlate admin actions** via ``X-Request-Id`` in audit reports.
- 🧱 **Rotate and retain logs** per compliance policy (GDPR, PCI-DSS, ISO 27001).
- 📈 **Trigger alerts** when error rates exceed thresholds, grouped by ``service`` and ``correlation_id``.

10.6.7 Operational Governance Checklist
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 20 60 20

   * - Category
     - Key Practice
     - Why It Matters
   * - **Tracing**
     - Generate ``X-Request-Id`` for every response
     - Root-cause visibility
   * - **Correlation**
     - Reuse ``X-Correlation-Id`` across related calls
     - End-to-end transaction tracing
   * - **Logging**
     - Emit structured JSON logs
     - Machine-readable monitoring
   * - **Security**
     - Mask sensitive info before logging
     - Data protection & compliance
   * - **Monitoring**
     - Return JsonDispatch envelopes for ``/health`` & ``/metrics``
     - Uniform automation
   * - **Audit**
     - Store IDs with every admin or financial action
     - Forensic traceability
   * - **Alerts**
     - Integrate with APM / log aggregator
     - Real-time anomaly detection

.. important::
   **Key Takeaway**

   JsonDispatch is not just a response contract — it’s the **observability spine** of your platform.
   When tracing, metrics, logs and audits all share the same IDs and envelope style, your API ecosystem becomes
   **self-diagnosing, self-auditing and self-healing**.
