2. Media types & versioning
===========================

As your API evolves, clients need a stable way to understand **which shape they’re getting** and how to **migrate** when it changes. JsonDispatch solves this by versioning **request media types** and signaling the **exact server version** in a response header.


2.1 Media type explained (with examples)
----------------------------------------

For requests with a body, set a JsonDispatch vendor media type in ``Content-Type``::

  Content-Type: application/vnd.infocyph.jd.v1+json


Media type breakdown
^^^^^^^^^^^^^^^^^^^^

- **``application``** — application payload (static)
- **``vnd.infocyph``** — your vendor namespace (configurable)
- **``jd``** — JsonDispatch spec identifier (static for this spec)
- **``v1``** — **major** version of the request format (configurable)
- **``+json``** — JSON syntax suffix (static)

.. note::

   Responses can simply use ``Content-Type: application/json`` while still following the JsonDispatch envelope.

Examples
^^^^^^^^

- **Project “Acme”**: ``application/vnd.acme.jd.v1+json``
- **Personal/OSS** (not recommended for org APIs): ``application/prs.yourname.jd.v1+json``


2.2 Versioning strategy (major/minor/patch)
-------------------------------------------

JsonDispatch follows `Semantic Versioning <https://semver.org/>`_:

- **Major** (``v1 → v2``): breaking changes to the **envelope or field types**
- **Minor** (``v1.1 → v1.2``): backward-compatible additions
- **Patch** (``v1.0.0 → v1.0.1``): backward-compatible bug fixes

.. tip::

   The **request media type** carries the **major** version (e.g., ``…jd.v1+json``).
   The server’s full version is returned in ``X-Api-Version`` (e.g., ``1.3.0``).

- **Do not** use ``Accept`` for version negotiation; keep it ``application/json`` if you send it at all.


2.3 Required & recommended headers
----------------------------------

Requests (with body)
^^^^^^^^^^^^^^^^^^^^

- **MUST** send::

    Content-Type: application/vnd.<vendor>.jd.v<MAJOR>+json

  Example::

    Content-Type: application/vnd.infocyph.jd.v1+json

- **SHOULD NOT** use ``Accept`` for versioning. If present, keep it::

    Accept: application/json

Responses
^^^^^^^^^

- **MUST** send::

    X-Api-Version: <MAJOR.MINOR.PATCH>

  Example::

    X-Api-Version: 1.4.0

- **MAY** send::

    Content-Type: application/json

.. note::

   Servers *can* set a vendor media type on responses if needed, but
   ``application/json`` is sufficient and preferred.

``X-Request-Id``, ``X-Correlation-Id`` and other tracing headers are covered in **Section 3**.


2.4 Version selection & migration
---------------------------------

- The **server controls** the response envelope version. Clients do **not** negotiate via ``Accept``.
- When you introduce a **breaking change**, bump the **request** major (e.g., ``v1 → v2``) and keep returning
  ``application/json`` with an updated ``X-Api-Version``.

Create (client → server)::

  POST /articles
  Content-Type: application/vnd.infocyph.jd.v1+json

  { "title": "Hello JD" }

Response (server → client)
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: http

   HTTP/1.1 201 Created
   Content-Type: application/json
   X-Api-Version: 1.4.0
   X-Request-Id: 1f1f6a2e-0c8f-4f7f-9b4b-5d2d0a3f5b99

.. code-block:: json

   {
     "status": "success",
     "data": { ... }
   }

After a breaking change (client updates request major)::

  POST /articles
  Content-Type: application/vnd.infocyph.jd.v2+json

  { "title": "Hello JD v2" }

Server response
~~~~~~~~~~~~~~~

.. code-block:: http

   HTTP/1.1 201 Created
   Content-Type: application/json
   X-Api-Version: 2.0.0
   X-Request-Id: 6c2a3d7e-9d5a-4b61-9b05-d1d8f6a8f4a1

.. code-block:: json

   {
     "status": "success",
     "data": { ... }
   }

Clients signal **request major** via ``Content-Type`` (when they send a body) and servers announce the **exact
implementation** via ``X-Api-Version`` in the **response**. No ``Accept`` gymnastics, and responses stay plain
``application/json``.


2.5 Non-JSON responses (reports & exports)
------------------------------------------

JsonDispatch defines the **response envelope for JSON**. For binary or tabular deliverables (CSV, PDF, ZIP, images), **return the native media type directly** and keep JsonDispatch for **orchestration endpoints** (job creation, metadata, links).

2.5.1 Direct file delivery
^^^^^^^^^^^^^^^^^^^^^^^^^^

When the endpoint returns a file stream:

Request::

  GET /reports/activity/download?from=2025-09-01&to=2025-09-30
  Accept: text/csv

Response
~~~~~~~~

.. code-block:: http

   HTTP/1.1 200 OK
   Content-Type: text/csv
   Content-Disposition: attachment; filename="activity-report-2025-09.csv"
   X-Api-Version: 1.4.0
   X-Request-Id: 7bfae01e-771c-41d4-b1cf-0ad52d8bce19

.. note::

   Use the correct ``Content-Type`` (e.g., ``text/csv``, ``application/pdf``, ``application/zip``) and add
   ``Content-Disposition`` for downloads.

2.5.2 Orchestration via JsonDispatch (recommended)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create the report **asynchronously** and return a JsonDispatch envelope with status and links.

Request::

  POST /reports/activity
  Content-Type: application/vnd.infocyph.jd.v1+json

  { "from": "2025-09-01", "to": "2025-09-30", "format": "csv" }

Response
~~~~~~~~

.. code-block:: http

   HTTP/1.1 202 Accepted
   Content-Type: application/json
   X-Api-Version: 1.4.0
   X-Request-Id: 3b2c7a5a-0b2e-4b69-b1a2-1a2c3d4e5f6a

Body
~~~~

.. code-block:: json

   {
     "status": "success",
     "message": "Report job accepted",
     "data": {
       "report_id": "rep_9KfGH2",
       "state": "queued",
       "format": "csv",
       "expires_at": "2025-10-31T23:59:59Z"
     },
     "_links": {
       "self": "https://api.example.com/reports/activity/rep_9KfGH2",
       "download": {
         "href": "https://cdn.example.com/reports/rep_9KfGH2.csv",
         "meta": { "method": "GET", "expires": "2025-10-31T23:59:59Z" }
       }
     },
     "_properties": {
       "data": { "type": "object", "name": "report" }
     }
   }

2.5.3 Streaming & large datasets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For very large exports, consider **streaming** formats:

- **CSV/TSV stream:** ``text/csv``
- **NDJSON stream:** ``application/x-ndjson``
- **Gzip:** add ``Content-Encoding: gzip`` when appropriate

Pair streaming/download endpoints with a **JsonDispatch status endpoint** so clients can poll readiness and discover ``_links.download``.

Status polling::

  GET /reports/activity/rep_9KfGH2
  Accept: application/json

Response (ready)
~~~~~~~~~~~~~~~~

.. code-block:: http

   HTTP/1.1 200 OK
   Content-Type: application/json
   X-Api-Version: 1.4.0
   X-Request-Id: d1c9b15f-9c1e-42d5-9a9e-8b8e5a2b1c0a

Body
~~~~

.. code-block:: json

   {
     "status": "success",
     "data": {
       "report_id": "rep_9KfGH2",
       "state": "ready",
       "size_bytes": 9421331
     },
     "_links": {
       "download": "https://cdn.example.com/reports/rep_9KfGH2.csv",
       "retry": "https://api.example.com/reports/activity/rep_9KfGH2/retry"
     }
   }

.. tip::

   **Rule of thumb:** use JsonDispatch for **control, status, and discovery**; use native media types for the **actual file bytes**.


2.6 Authentication & authorization
----------------------------------

JsonDispatch APIs typically require authentication. This section defines where authentication credentials should be placed and how authentication failures map to the response envelope.

2.6.1 Authentication token placement
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Recommended:** use the ``Authorization`` header with a bearer token for API authentication.

.. code-block:: http

   GET /api/v1/users/me
   Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   Accept: application/json

**Alternative patterns:**

- **API Keys:** ``X-Api-Key: your-api-key-here``
- **Basic Auth:** ``Authorization: Basic base64(username:password)`` (HTTPS only)
- **Cookie-based:** ``Cookie: session_id=abc123`` (for browser clients)

.. warning::

   Never send credentials in query parameters or URL paths, as they may be logged by proxies, CDNs, or web servers.

2.6.2 Authentication failure responses
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When authentication fails (missing, invalid, or expired token), return **``401 Unauthorized``** with a ``fail`` status.

Example: Missing token
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: http

   HTTP/1.1 401 Unauthorized
   Content-Type: application/json
   X-Api-Version: 1.4.0
   X-Request-Id: f47ac10b-58cc-4372-a567-0e02b2c3d479
   WWW-Authenticate: Bearer realm="API"

.. code-block:: json

   {
     "status": "fail",
     "message": "Authentication required",
     "data": {
       "errors": [
         {
           "field": "Authorization",
           "code": "AUTH_MISSING",
           "message": "No authentication token provided"
         }
       ]
     }
   }

Example: Invalid or expired token
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: http

   HTTP/1.1 401 Unauthorized
   Content-Type: application/json
   X-Api-Version: 1.4.0
   X-Request-Id: 550e8400-e29b-41d4-a716-446655440000
   WWW-Authenticate: Bearer realm="API", error="invalid_token"

.. code-block:: json

   {
     "status": "fail",
     "message": "Invalid or expired authentication token",
     "data": {
       "errors": [
         {
           "field": "Authorization",
           "code": "AUTH_INVALID",
           "message": "Token signature verification failed"
         }
       ]
     },
     "_links": {
       "refresh": "https://api.example.com/auth/refresh",
       "login": "https://api.example.com/auth/login"
     }
   }

2.6.3 Authorization (403 Forbidden)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When a user is **authenticated** but lacks **permission** to access a resource, return **``403 Forbidden``** with a ``fail`` status.

.. code-block:: http

   HTTP/1.1 403 Forbidden
   Content-Type: application/json
   X-Api-Version: 1.4.0
   X-Request-Id: 6ba7b810-9dad-11d1-80b4-00c04fd430c8

.. code-block:: json

   {
     "status": "fail",
     "message": "Access denied",
     "data": {
       "errors": [
         {
           "field": "resource",
           "code": "PERMISSION_DENIED",
           "message": "You do not have permission to delete this resource"
         }
       ]
     }
   }

2.6.4 API key authentication
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For server-to-server communication, API keys can be used:

.. code-block:: http

   GET /api/v1/webhooks
   X-Api-Key: sk_live_51H8rQ2eZvKYlo2C8...
   Accept: application/json

Failed API key authentication
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: http

   HTTP/1.1 401 Unauthorized
   Content-Type: application/json
   X-Api-Version: 1.4.0
   X-Request-Id: 7c9e6679-7425-40de-944b-e07fc1f90ae7

.. code-block:: json

   {
     "status": "fail",
     "message": "Invalid API key",
     "data": {
       "errors": [
         {
           "field": "X-Api-Key",
           "code": "INVALID_API_KEY",
           "message": "The provided API key is invalid or has been revoked"
         }
       ]
     }
   }

2.6.5 OAuth 2.0 & token refresh
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For OAuth 2.0 flows, expired access tokens should return ``401`` with a hint to refresh:

.. code-block:: json

   {
     "status": "fail",
     "message": "Access token expired",
     "data": {
       "errors": [
         {
           "field": "Authorization",
           "code": "TOKEN_EXPIRED",
           "message": "Access token has expired. Use refresh token to obtain a new one"
         }
       ]
     },
     "_links": {
       "refresh": "https://api.example.com/oauth/token"
     },
     "_properties": {
       "token": {
         "expired_at": "2025-10-22T14:30:00Z",
         "type": "Bearer"
       }
     }
   }

.. tip::

   Always include the ``WWW-Authenticate`` header in 401 responses to help clients understand the authentication scheme.
