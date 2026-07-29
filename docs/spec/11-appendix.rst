11. Conformance artifacts
=========================

11.1 Canonical publication
--------------------------

The Read the Docs project origin is:

``https://docs.infocyph.com/projects/json-dispatch/``

Read the Docs serves versioned builds at
``/projects/json-dispatch/<language>/<version>/``. The immutable 3.0.0
documentation root is:

``https://docs.infocyph.com/projects/json-dispatch/en/3.0.0/``

Published v3 schemas for that build are rooted at:

``https://docs.infocyph.com/projects/json-dispatch/en/3.0.0/schemas/v3/``

The repository copies ``schemas`` and ``fixtures`` into the documentation
artifact without transforming them. Development builds expose the same paths
under their Read the Docs version slug, such as ``en/latest``.

11.2 Version manifest
---------------------

``specification.json`` identifies the current specification version, media type
major, schemas, and fixture manifest. Consumers SHOULD use a released tag or an
immutable commit when pinning the specification.

JsonDispatch 3.0.0 provides:

- ``schemas/v3/envelope.schema.json`` for response bodies;
- ``schemas/v3/http-response.schema.json`` for canonical HTTP fixture records;
- supporting issue, link, property, pagination, and reference schemas; and
- ``fixtures/v3/manifest.json`` listing positive and negative fixtures.

11.3 Fixture record format
--------------------------

HTTP conformance fixtures are JSON records with:

.. code-block:: json

   {
     "http_status": 200,
     "headers": {
       "Content-Type": "application/vnd.infocyph.jd.v3+json; charset=utf-8",
       "X-Api-Version-Selected": "1.4.2",
       "X-Request-Id": "019fb440-4e83-7b1b-9ef9-44a80771f181",
       "Vary": "Accept, X-Api-Version"
     },
     "body": {
       "status": "success"
     }
   }

The record is a test representation, not a network serialization. Header names
use canonical casing in fixtures so ordinary JSON Schema can validate them.
Actual HTTP field names are case-insensitive, and ``Vary`` field order is not
significant.

11.4 Positive and negative fixtures
-----------------------------------

Every positive fixture MUST validate against the declared schema. Every
negative fixture MUST fail validation. A negative fixture's manifest entry
states the normative rule it violates.

Adding a normative rule requires at least one positive fixture when the rule
adds a valid shape and at least one negative fixture when JSON Schema can
express the invalid shape.

11.5 Local validation
---------------------

From the repository root:

.. code-block:: bash

   python -m pip install -r docs/requirements.txt
   python tools/check_conformance.py
   sphinx-build -W --keep-going -b html docs docs/_build/html

The conformance checker validates schemas themselves, verifies the specification
manifest and fixture inventory, accepts all positive fixtures, and rejects all
negative fixtures.

11.6 Prose-only rules
---------------------

Some HTTP rules cannot be completely represented by the fixture schemas,
including:

- case-insensitive HTTP field names;
- media-range quality and precedence;
- semantic-version compatibility selection;
- uniqueness of request identifiers;
- complete RFC 6901 escaping for source pointers and pointer patterns;
- arithmetic relationships such as ``count <= limit``;
- preservation of filter and sort query semantics in pagination links; and
- redaction of private implementation detail.

Conforming implementations MUST cover applicable prose-only rules with their
own integration tests.
