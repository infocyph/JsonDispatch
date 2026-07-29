2. Media types and versioning
=============================

2.1 JsonDispatch media type
---------------------------

A JsonDispatch v3 representation uses:

::

   application/vnd.<vendor>.jd.v3+json

``<vendor>`` is a lowercase registered or organization-controlled token. For
example:

::

   application/vnd.infocyph.jd.v3+json
   application/vnd.acme.jd.v3+json

The ``v3`` component identifies the JsonDispatch major version. It does not
identify the application API version.

2.2 Request negotiation
-----------------------

A request for a JsonDispatch representation:

- MUST include an ``Accept`` field containing at least one compatible
  JsonDispatch media type;
- MUST include ``X-Api-Version`` with a full stable semantic version in
  ``MAJOR.MINOR.PATCH`` form; and
- MAY include other acceptable representations.

Example:

.. code-block:: http

   GET /articles HTTP/1.1
   Accept: application/vnd.infocyph.jd.v3+json
   X-Api-Version: 1.4.0

The server MUST apply HTTP media-range precedence and quality values. It MUST
NOT select a representation solely because it appears first when another
compatible representation has a higher quality value.

The selected application API version MUST have the same major version as the
requested ``X-Api-Version``. A server MAY select a later compatible minor or
patch version. It MUST NOT silently select a different application API major.

2.3 Response representation
---------------------------

A conforming response with an envelope MUST include:

.. code-block:: http

   HTTP/1.1 200 OK
   Content-Type: application/vnd.infocyph.jd.v3+json; charset=utf-8
   X-Api-Version-Selected: 1.4.2
   X-Request-Id: 019fb440-4e83-7b1b-9ef9-44a80771f181
   Vary: Accept, X-Api-Version

The ``Content-Type`` vendor token MUST match the selected request
representation. ``X-Api-Version-Selected`` MUST contain the exact application
API version used to produce the response.

The representation MUST be valid JSON encoded as UTF-8. Producers MUST send a
JsonDispatch vendor media type, not plain ``application/json``, for a response
claimed to conform to this specification.

``Vary`` MUST identify both ``Accept`` and ``X-Api-Version``. It MAY contain
additional fields and field order is not significant.

The restricted-transport profile defined in Section 4.3 additionally uses
``X-JD-Status-Code`` and ``Cache-Control``. It does not alter media-type
or application-version negotiation.

2.4 Negotiation failures
------------------------

Protocol failures use a conforming ``fail`` envelope when the server can emit a
JsonDispatch error representation:

.. list-table::
   :header-rows: 1
   :widths: 44 12 44

   * - Condition
     - HTTP status
     - Required issue code
   * - ``X-Api-Version`` is missing or malformed
     - ``400``
     - ``API_VERSION_INVALID``
   * - No acceptable JsonDispatch media type is supported
     - ``406``
     - ``REPRESENTATION_NOT_ACCEPTABLE``
   * - The application API version is valid but unsupported
     - ``406``
     - ``API_VERSION_UNSUPPORTED``
   * - The requested application API version is retired
     - ``410``
     - ``API_VERSION_RETIRED``

A ``406`` response MAY use the server's default supported JsonDispatch media
type because no requested representation was selectable. Its issue metadata
SHOULD identify supported media types or versions without exposing internal
configuration.

Request-body ``Content-Type`` validation is owned by the application protocol,
not JsonDispatch.

2.5 Responses outside JsonDispatch
----------------------------------

Binary files, CSV, HTML, images, event streams, and other non-JSON
representations use their native media types and do not carry a JsonDispatch
envelope.

HTTP responses that cannot contain a representation, including ``204``,
``205``, and ``304``, are not JsonDispatch responses. Redirects are also
outside the envelope contract.
