3. Response identification
===========================

3.1 Request identifier
----------------------

Every conforming HTTP response MUST include ``X-Request-Id``.

The producer MUST generate a new request identifier once for each inbound
request. It MUST NOT trust or echo an inbound ``X-Request-Id`` as the generated
identifier. The value:

- MUST be a non-empty ASCII string;
- MUST contain no whitespace or control characters;
- MUST be no longer than 128 characters; and
- MUST be sufficiently unique within the producer's operational lifetime.

UUID and ULID values satisfy the syntax when generated with an appropriate
uniqueness source. JsonDispatch does not mandate an identifier algorithm.

The same generated value MUST be used for every attempted JsonDispatch
response associated with that request.

3.2 Correlation identifier
--------------------------

``X-Correlation-Id`` is optional and identifies a logical operation spanning
multiple requests.

If a producer accepts an inbound correlation identifier, it MUST validate the
value before use. An accepted value MUST follow the same length and character
limits as ``X-Request-Id``. The response MUST echo the accepted value exactly.

A producer MAY generate a correlation identifier when none was supplied. If
it does, it MUST return that value in ``X-Correlation-Id``.

How an implementation propagates correlation context to logs, messages, or
downstream services is outside this specification.

3.3 Distributed tracing
-----------------------

W3C ``traceparent`` and ``tracestate`` fields are independent from
JsonDispatch identifiers. Implementations MAY support them according to the
W3C Trace Context specification. JsonDispatch neither changes nor duplicates
their semantics.

3.4 Identification summary
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 28 22 34 16

   * - Field
     - Direction
     - Meaning
     - Required
   * - ``X-Request-Id``
     - Response
     - Producer-generated request identity
     - Yes
   * - ``X-Correlation-Id``
     - Request and response
     - Logical operation identity
     - No
   * - ``X-Api-Version``
     - Request
     - Requested application API version
     - Yes
   * - ``X-Api-Version-Selected``
     - Response
     - Served application API version
     - Yes
