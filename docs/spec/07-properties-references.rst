7. Properties, references, and pagination
=========================================

7.1 Property map
----------------

``_properties`` is an object whose keys are JSON Pointer patterns into the
envelope. Each value describes the selected representation at that location.
Keys MUST begin with ``/``. Segments use RFC 6901 escaping, with one
JsonDispatch extension: a complete ``*`` segment describes every item of an
array.

A property descriptor MUST contain ``type`` and MAY contain ``name``,
``template``, ``deprecation``, or ``pagination``:

.. list-table::
   :header-rows: 1
   :widths: 22 22 56

   * - Member
     - Type
     - Meaning
   * - ``type``
     - string
     - JSON type: array, object, string, number, integer, boolean, or null
   * - ``name``
     - string
     - Stable logical name
   * - ``template``
     - URI-reference
     - Machine-readable schema for the value
   * - ``deprecation``
     - URI-reference
     - Migration information for a deprecated value
   * - ``pagination``
     - object
     - Collection pagination state

``pagination`` is permitted only on the ``/data`` descriptor, and that
descriptor's type MUST be ``array``.

Example:

.. code-block:: json

   "_properties": {
     "/data": {
       "type": "array",
       "name": "articles"
     },
     "/data/*/legacy_title": {
       "type": "string",
       "deprecation": "https://docs.example.com/articles/title-migration"
     }
   }

The ``*`` token is metadata syntax, not an RFC 6901 wildcard. Clients MUST NOT
use a pointer pattern containing ``*`` to address the JSON document.

7.2 Offset pagination
---------------------

Offset pagination metadata has:

- ``mode`` equal to ``offset``;
- non-negative integer ``offset``;
- positive integer ``limit``;
- non-negative integer ``count`` for items in the current ``data`` array; and
- optional non-negative integer ``total``.

``count`` MUST equal the number of returned items and MUST NOT exceed
``limit``. If ``total`` is present, it MUST be at least ``offset + count``.
Producers SHOULD omit ``total`` when calculating it would require an
unnecessary count query.

The response MUST include ``_links.self``. It MUST include ``next`` when more
items are known to exist and ``prev`` when a preceding offset exists.
``first`` and ``last`` MAY be included when ``total`` is known.

7.3 Cursor pagination
---------------------

Cursor pagination metadata has:

- ``mode`` equal to ``cursor``;
- positive integer ``limit``;
- non-negative integer ``count``;
- boolean ``has_more``;
- ``next_cursor`` when ``has_more`` is true; and
- optional ``previous_cursor`` when reverse traversal is supported.

``count`` MUST equal the number of returned items and MUST NOT exceed
``limit``. Cursor values MUST be treated as opaque non-empty strings. Clients
MUST NOT decode, construct, or modify them.

The response MUST include ``_links.self``. When ``has_more`` is true, it MUST
include both ``next_cursor`` and ``_links.next``.

7.4 References
--------------

``_references`` is an object whose keys use the same JSON Pointer-pattern
syntax as ``_properties``. A path MAY use a ``*`` segment to describe every
array item.

Each path maps identifiers, represented as JSON object keys, to either:

- a string label; or
- an object containing a string ``label`` and optional ``children`` lookup.

Example:

.. code-block:: json

   "_references": {
     "/data/*/category": {
       "10": {
         "label": "Hardware",
         "children": {
           "101": "Laptop",
           "102": "Phone"
         }
       }
     }
   }

Reference trees MUST be finite and bounded by the producer. References are
display metadata, not authorization rules or canonical resource storage.
Producers SHOULD include only mappings used by the selected ``data`` payload.
