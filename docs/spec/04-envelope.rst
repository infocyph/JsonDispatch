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

4.2 Status and HTTP mapping
---------------------------

``status`` MUST agree with the HTTP response status:

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

``1xx`` and ``3xx`` responses do not use a JsonDispatch envelope. ``204``,
``205``, and ``304`` do not carry a JsonDispatch body.

4.3 Data
--------

For ``success``, ``data`` MAY be any JSON value and MAY be omitted when the
successful operation has no representation-specific payload.

For ``fail`` and ``error``, ``data`` is REQUIRED and MUST be a non-empty array
of issue objects defined in Chapter 6. An empty issue array is invalid.

The shape of successful ``data`` is an application API contract. JsonDispatch
does not impose resource wrappers, ORM conventions, attribute bags, or
identifier types.

4.4 Companion members
---------------------

``_properties``, ``_references``, and ``_links`` describe the selected
representation. They MUST NOT contain authorization decisions, credentials,
internal service topology, or executable implementation instructions.

Their complete shapes are defined in Chapters 7 and 8 and in the v3 schemas.
Producers SHOULD omit any companion member that would otherwise be empty.

4.5 Minimal examples
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
