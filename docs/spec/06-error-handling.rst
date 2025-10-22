6. Error Handling
=================

Errors are where consistency matters most. If every service formats errors differently, debugging turns into chaos.
JsonDispatch enforces a clean, uniform structure for **client-side issues** (``fail``) and **server-side issues** (``error``) — so you always know where the problem came from.


6.1 ``fail`` vs ``error`` — Know the Difference
-----------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 16 32 18 18 16

   * - Type
     - Cause
     - Who Fixes It
     - Typical HTTP Status
     - Example
   * - **``fail``**
     - The client sent something invalid
     - The **client**
     - 400–422
     - Missing required fields, invalid format
   * - **``error``**
     - The server or an external dependency failed
     - The **server**
     - 500–504
     - Timeout, DB crash, network outage

Think of it like this:

- 🧑‍💻 **fail** → *“Fix your request and try again.”*
- 🧩 **error** → *“It’s not you, it’s us.”*

This split helps:

- **Clients** decide whether to retry or correct their data.
- **Developers** log and alert on real outages separately from validation noise.


6.2 Error Object Structure
--------------------------

Both ``fail`` and ``error`` responses contain an **array of objects** under ``data``. Each describes one issue in a standard format:

.. list-table::
   :header-rows: 1
   :widths: 16 14 70

   * - Field
     - Type
     - Description
   * - ``status``
     - integer
     - HTTP status code for this error.
   * - ``source``
     - string
     - Where the problem occurred — field path or subsystem name.
   * - ``title``
     - string
     - Short summary of the problem.
   * - ``detail``
     - string
     - Human-readable explanation for logs or UI.

**Example – Client Validation (``fail``)**

.. code-block:: http

   HTTP/1.1 422 Unprocessable Entity
   Content-Type: application/json
   X-Api-Version: 1.3.1
   X-Request-Id: 9d2e7f6a-2f3b-45b0-9ff2-dc3d99991234

.. code-block:: json

   {
     "status": "fail",
     "message": "Validation failed",
     "data": [
       {
         "status": 422,
         "source": "/data/attributes/email",
         "title": "Invalid email",
         "detail": "Email must be a valid address."
       },
       {
         "status": 422,
         "source": "/data/attributes/password",
         "title": "Password too short",
         "detail": "Password must be at least 8 characters."
       }
     ]
   }

**Example – Server Outage (``error``)**

.. code-block:: http

   HTTP/1.1 503 Service Unavailable
   Content-Type: application/json
   X-Api-Version: 1.3.1
   X-Request-Id: e13a97b3-5a2d-46db-a3b2-f401239b0cba

.. code-block:: json

   {
     "status": "error",
     "message": "Database unavailable",
     "code": "DB_CONN_TIMEOUT",
     "data": [
       {
         "status": 503,
         "source": "db-service",
         "title": "Timeout",
         "detail": "No response from database after 30s."
       }
     ]
   }


6.3 Field-level vs request-level errors
---------------------------------------

JsonDispatch lets you express **where** an issue occurred so clients can react precisely.

**Two scopes**

- **Field-level** — a specific input is invalid. Use a **JSON Pointer–style path** in ``source`` (e.g., ``/data/attributes/email``).
- **Request-level** — the whole request failed for a non-field reason (rate limit, auth, dependency outage). Use a **concise string** naming the subsystem or concern (e.g., ``auth``, ``rate-limit``, ``payments-gateway``).

**Rules**

- Prefer the most **specific** ``source`` you can provide.
- You **may mix** field-level and request-level items in the same ``data`` array.
- Keep ``title`` short; put human-friendly detail in ``detail``.
- Don’t leak internals; subsystem names should be stable, public-safe identifiers.

**Examples**

Field-level (``fail``)
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: json

   {
     "status": "fail",
     "message": "Validation failed",
     "data": [
       {
         "status": 422,
         "source": "/data/attributes/email",
         "title": "Invalid email",
         "detail": "Email must be a valid address."
       },
       {
         "status": 422,
         "source": "/data/attributes/age",
         "title": "Out of range",
         "detail": "Age must be between 13 and 120."
       }
     ]
   }

Request-level (``error``)
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: json

   {
     "status": "error",
     "message": "Upstream dependency unavailable",
     "code": "PAYMENTS_GATEWAY_DOWN",
     "data": [
       {
         "status": 503,
         "source": "payments-gateway",
         "title": "Service unavailable",
         "detail": "No response from provider within 30s."
       }
     ]
   }

Mixed (some fields invalid, plus a request constraint)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: json

   {
     "status": "fail",
     "message": "Request cannot be processed",
     "data": [
       {
         "status": 422,
         "source": "/data/attributes/items/0/sku",
         "title": "Unknown SKU",
         "detail": "SKU ABC-123 was not found."
       },
       {
         "status": 429,
         "source": "rate-limit",
         "title": "Too many requests",
         "detail": "Burst limit exceeded; retry after 15 seconds."
       }
     ]
   }

**Client guidance**

- **Highlight fields** with pointer paths; show inline messages near inputs.
- **Banner or dialog** for request-level issues (``auth``, ``rate-limit``, ``maintenance``).
- Consider ``status`` code for **retry/backoff** behavior (see the next subsections).


6.4 Error Codes (``code``) — Symbolic and Actionable
----------------------------------------------------

The optional top-level ``code`` field adds a **business-level meaning** beyond the HTTP status. It’s ideal for client logic, dashboards, and automation.

**Guidelines**

- Use uppercase ``UPPER_SNAKE_CASE``.
- Keep them short and descriptive.
- Document them in your internal or public API guide.
- Stay consistent across microservices.

**Examples**

.. list-table::
   :header-rows: 1
   :widths: 36 64

   * - Code
     - Meaning
   * - ``USER_NOT_FOUND``
     - The requested user doesn’t exist.
   * - ``DB_CONN_TIMEOUT``
     - Database connection timeout.
   * - ``PAYMENT_GATEWAY_DOWN``
     - Payment provider not reachable.
   * - ``ARTICLE_TITLE_TOO_SHORT``
     - Validation failure on title.


6.5 Recommended HTTP Status Mapping
-----------------------------------

.. list-table::
   :header-rows: 1
   :widths: 54 14 32

   * - Scenario
     - ``status``
     - HTTP Status
   * - Read / List / Create / Update Success
     - success
     - 200 / 201 / 204
   * - Validation error / bad input
     - fail
     - 400 / 422
   * - Authentication required or failed
     - fail
     - 401
   * - Forbidden (no permission)
     - fail
     - 403
   * - Not found
     - fail
     - 404
   * - Conflict (duplicate / version mismatch)
     - fail
     - 409
   * - Server exception / crash
     - error
     - 500
   * - Bad gateway (upstream failure)
     - error
     - 502
   * - Service unavailable / maintenance
     - error
     - 503
   * - Upstream timeout
     - error
     - 504


6.6 Key Takeaways
-----------------

- Clients never send ``X-Request-Id`` — the server generates it for traceability.
- All error and fail responses share the same envelope shape.
- Each issue in ``data[]`` must be explicit and readable.
- ``code`` + ``status`` + ``X-Request-Id`` = everything you need for quick debugging.
