1. Scope and conformance
========================

JsonDispatch 3.0.0 is a language-neutral specification for JSON HTTP response
envelopes. It gives clients one deterministic place to inspect an outcome,
payload, machine-readable issues, resource metadata, references, and links.

1.1 Normative language
----------------------

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHOULD**, **SHOULD NOT**,
and **MAY** are to be interpreted as described by BCP 14 (RFC 2119 and RFC
8174) when, and only when, they appear in uppercase.

Text labelled "Non-normative" does not define conformance. Examples illustrate
valid shapes but do not add requirements beyond the normative chapters.

1.2 Scope
---------

This specification defines:

- the JsonDispatch vendor media type and version negotiation;
- response identification headers;
- the JSON envelope and its status semantics;
- machine-readable issue objects;
- resource properties, references, and links;
- offset and cursor pagination metadata; and
- compatibility and conformance rules.

JsonDispatch does not define request-body schemas, routing, authentication,
authorization, sessions, middleware, logging, storage, serialization APIs,
framework adapters, or programming-language helpers.

1.3 Version identity
--------------------

The JsonDispatch specification version and an application's API version are
independent:

- ``3.0.0`` is the version of this specification.
- ``v3`` in the media type selects this specification's envelope major.
- ``X-Api-Version`` and ``X-Api-Version-Selected`` identify the application
  API contract, not the JsonDispatch specification release.

An implementation pins the complete JsonDispatch specification version in its
own release metadata. It MUST NOT report that value through
``X-Api-Version-Selected``.

1.4 Conformance targets
-----------------------

A **conforming envelope** satisfies the v3 envelope schema and every applicable
normative rule in Chapters 4, 6, 7, and 8.

A **conforming HTTP response** has a conforming envelope, satisfies the
applicable status and header rules in Chapters 2 and 3, and uses an HTTP status
consistent with the envelope status.

A **conforming implementation** emits only conforming HTTP responses when it
selects a JsonDispatch representation. It MAY expose endpoints that return
other representations; those responses are outside JsonDispatch conformance.

The versioned schemas and fixtures described in Chapter 11 are normative
artifacts. Prose controls when a behavior cannot be expressed by JSON Schema.

1.5 Design constraints
----------------------

- Clients MUST be able to parse the envelope without framework knowledge.
- A response MUST NOT expose secrets, credentials, stack traces, SQL, internal
  paths, or other private implementation detail.
- Optional members MUST be omitted when they have no value; placeholder empty
  metadata SHOULD NOT be emitted.
- Producers SHOULD avoid computing optional properties, references, or links
  that the selected representation does not require.
