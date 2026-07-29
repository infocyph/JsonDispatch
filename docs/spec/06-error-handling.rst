6. Failures and errors
======================

6.1 Outcome classification
--------------------------

``fail`` means a client-side change is required before the request can
succeed. It is used with ``4xx`` HTTP statuses.

``error`` means the producer or one of its dependencies could not complete an
otherwise valid request. It is used with ``5xx`` HTTP statuses.

Retryability is not implied by ``status`` alone. Applications use HTTP
semantics such as ``Retry-After`` and documented issue codes to communicate
retry behavior.

6.2 Issue object
----------------

Every entry in a ``fail`` or ``error`` ``data`` array MUST be an issue object
with this shape:

.. list-table::
   :header-rows: 1
   :widths: 20 20 16 44

   * - Member
     - Type
     - Required
     - Meaning
   * - ``code``
     - string
     - Yes
     - Stable machine-readable identifier
   * - ``title``
     - string
     - Yes
     - Short public-safe summary
   * - ``detail``
     - string
     - No
     - Public-safe explanation
   * - ``source``
     - object
     - No
     - One location for the issue
   * - ``meta``
     - object
     - No
     - Application-defined structured detail

Unknown issue members are invalid.

``code`` MUST match ``^[A-Z][A-Z0-9_]*$`` and remain stable within an
application API major. ``title`` and ``detail`` MUST be non-empty when present.
Clients SHOULD branch on ``code``, not human-readable text.

An issue does not repeat the HTTP status. All issues in one response belong to
the single outcome represented by the response status and envelope status.

6.3 Source object
-----------------

``source`` MUST contain exactly one of:

.. list-table::
   :header-rows: 1
   :widths: 22 78

   * - Member
     - Meaning
   * - ``pointer``
     - RFC 6901 JSON Pointer into the application request document
   * - ``parameter``
     - Request query or form parameter name
   * - ``header``
     - HTTP request field name
   * - ``resource``
     - Stable public resource or dependency identifier

Source values MUST be non-empty strings. A pointer MUST begin with ``/`` and
MUST use RFC 6901 escaping. A producer MUST NOT use ``source`` to expose a
filesystem path, SQL identifier, internal hostname, class name, or stack frame.

Example:

.. code-block:: json

   {
     "code": "EMAIL_INVALID",
     "title": "Email is invalid",
     "source": {
       "pointer": "/profile/email"
     }
   }

6.4 Multiple issues
-------------------

A producer MAY return multiple issues when they share the same HTTP outcome.
Their order MUST be deterministic for the same selected API version and input.

A producer MUST NOT combine issues that require different HTTP outcome
classes. For example, a validation ``fail`` and a dependency ``error`` cannot
share one envelope.

6.5 Status guidance
-------------------

The application selects the most specific applicable HTTP status. Common
mappings include:

.. list-table::
   :header-rows: 1
   :widths: 58 14 28

   * - Condition
     - Envelope
     - Typical HTTP status
   * - Malformed request or negotiation field
     - ``fail``
     - ``400``
   * - Representation not acceptable
     - ``fail``
     - ``406``
   * - Semantic validation failed
     - ``fail``
     - ``422``
   * - Rate limit exceeded
     - ``fail``
     - ``429``
   * - Unexpected producer failure
     - ``error``
     - ``500``
   * - Upstream service failure
     - ``error``
     - ``502`` or ``503``
   * - Upstream timeout
     - ``error``
     - ``504``

JsonDispatch classifies the resulting response; it does not define
authentication policy or application-specific status selection.
