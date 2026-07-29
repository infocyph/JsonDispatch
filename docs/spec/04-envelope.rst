4. Response envelope
====================

4.1 Top-level object
--------------------

A JsonDispatch body MUST be a JSON object. It MAY contain only these top-level
members:

.. list-table::
   :header-rows: 1
   :widths: 22 20 18 40

   * - Member
     - Type
     - Required
     - Purpose
   * - ``status``
     - string
     - Always
     - ``success``, ``fail``, or ``error``
   * - ``status_code``
     - integer
     - Status tunneling
     - Semantic HTTP status when the transport cannot carry it
   * - ``message``
     - string
     - No
     - Human-readable summary
   * - ``data``
     - any JSON value
     - For fail/error
     - Success payload or issue array
   * - ``_properties``
     - object
     - No
     - Resource and pagination metadata
   * - ``_references``
     - object
     - No
     - Bounded identifier-to-label mappings
   * - ``_links``
     - object
     - No
     - Typed or simple link relations

Unknown top-level members are invalid. Applications place extension data
inside their ``data`` payload or inside an explicitly permitted ``meta`` member
of an issue or link object.

If present, ``message`` MUST be non-empty. Clients MUST NOT use ``message`` for
program control or localization keys.

4.2 Native HTTP status
----------------------

Native HTTP status is the default profile. ``status`` MUST agree with the HTTP
response status:

.. list-table::
   :header-rows: 1
   :widths: 20 24 56

   * - Envelope status
     - HTTP range
     - Meaning
   * - ``success``
     - ``2xx`` with a body
     - The requested operation completed successfully.
   * - ``fail``
     - ``4xx``
     - The request cannot succeed without a client-side change.
   * - ``error``
     - ``5xx``
     - The producer or a dependency could not complete a valid request.

One response has one status. A producer MUST NOT place a ``fail`` envelope on a
``5xx`` response or an ``error`` envelope on a ``4xx`` response.

``status_code`` MAY be present in the native profile. When present, it MUST
equal the actual HTTP response status. Producers SHOULD omit it because the
transport already carries the value.

``1xx`` and ``3xx`` responses do not use a JsonDispatch envelope. ``204``,
``205``, and ``304`` do not carry a JsonDispatch body.

4.3 Restricted-transport status tunneling
-----------------------------------------

Some controlled gateways, hosting platforms, or intermediary policies prevent
an application from returning ``4xx`` or ``5xx`` responses. A producer MAY use
status tunneling only when such a transport restriction has been explicitly
configured. It MUST NOT select this profile merely to avoid correct HTTP error
handling.

A tunneled response:

- MUST use an actual HTTP status of ``200``;
- MUST have an envelope status of ``fail`` or ``error``;
- MUST include ``status_code`` with the intended ``4xx`` or ``5xx`` semantic
  status;
- MUST include ``X-JD-Status-Code`` with the same decimal status;
- MUST include a ``Cache-Control`` field containing ``no-store``; and
- MUST satisfy every ordinary rule for its semantic status class.

The envelope ``status``, ``status_code``, and ``X-JD-Status-Code`` MUST
agree exactly. A producer MUST NOT tunnel ``success``. The
``X-JD-Status-Code`` field MUST NOT appear in the native profile.

Example:

.. code-block:: http

   HTTP/1.1 200 OK
   Content-Type: application/vnd.infocyph.jd.v3+json; charset=utf-8
   X-Api-Version-Selected: 1.4.2
   X-Request-Id: 019fb440-4e83-7b1b-9ef9-44a80771f184
   Vary: Accept, X-Api-Version
   X-JD-Status-Code: 503
   Cache-Control: no-store

.. code-block:: json

   {
     "status": "error",
     "status_code": 503,
     "message": "The service is temporarily unavailable",
     "data": [
       {
         "code": "DEPENDENCY_UNAVAILABLE",
         "title": "A required dependency did not respond"
       }
     ]
   }

A tunnel-aware client MUST compare the header and body values and reject a
mismatch as a protocol error. A client that has not explicitly enabled this
profile will see the outer ``200`` as success, so producers and consumers MUST
agree on its use before deployment. Access logs, metrics, alerts, tracing, and
retry policy MUST use the semantic status rather than counting the outer
``200`` as a successful operation.

An undeclared error envelope on ``200``, or a ``200`` error without all
tunneling signals, is nonconforming.

4.4 Data
--------

For ``success``, ``data`` MAY be any JSON value and MAY be omitted when the
successful operation has no representation-specific payload.

For ``fail`` and ``error``, ``data`` is REQUIRED and MUST be a non-empty array
of issue objects defined in Chapter 6. An empty issue array is invalid.

The shape of successful ``data`` is an application API contract. JsonDispatch
does not impose resource wrappers, ORM conventions, attribute bags, or
identifier types.

4.5 Companion members
---------------------

``_properties``, ``_references``, and ``_links`` describe the selected
representation. They MUST NOT contain authorization decisions, credentials,
internal service topology, or executable implementation instructions.

Their complete shapes are defined in Chapters 7 and 8 and in the v3 schemas.
Producers SHOULD omit any companion member that would otherwise be empty.

4.6 Minimal examples
--------------------

Success:

.. code-block:: json

   {
     "status": "success",
     "data": {
       "id": "article-42",
       "title": "A predictable envelope"
     }
   }

Failure:

.. code-block:: json

   {
     "status": "fail",
     "message": "Validation failed",
     "data": [
       {
         "code": "EMAIL_INVALID",
         "title": "Invalid email",
         "source": {
           "pointer": "/email"
         }
       }
     ]
   }
