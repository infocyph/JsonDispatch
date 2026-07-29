9. Compatibility and evolution
==============================

9.1 Specification versions
--------------------------

JsonDispatch follows semantic versioning:

- A **major** release may change a normative schema, remove or change a
  requirement, or alter envelope semantics.
- A **minor** release may add conformance fixtures, non-breaking normative
  clarification, or optional guidance that remains valid under the existing
  schemas.
- A **patch** release corrects editorial defects without changing conforming
  behavior.

An implementation MUST pin a complete specification version. It MUST rerun all
positive and negative fixtures before changing that pin.

The media type major changes only for a JsonDispatch major release. JsonDispatch
3.x uses ``jd.v3+json``.

9.2 Application API evolution
-----------------------------

Application API versioning is independent from JsonDispatch versioning. Within
one application API major, a producer:

- MUST NOT remove a documented field;
- MUST NOT change a documented field's JSON type or meaning;
- MAY add documented optional fields;
- MAY deprecate a field while continuing to emit it; and
- SHOULD provide a migration URI through the relevant property descriptor.

Clients of a compatible application API minor MUST ignore unknown members
inside application-owned ``data`` and ``meta`` objects. This rule does not
permit unknown JsonDispatch envelope or issue members.

A producer that removes a field, changes its type, or changes its meaning MUST
select a new application API major.

9.3 Deprecation and retirement
------------------------------

A deprecated application API SHOULD include a standard ``Deprecation`` response
field. A scheduled retirement SHOULD also include ``Sunset``.

After an advertised version is retired, a request for that version MUST receive
``410 Gone`` with ``status`` equal to ``fail`` and issue code
``API_VERSION_RETIRED`` when a JsonDispatch response can be negotiated.

The response SHOULD link to supported versions or migration documentation.
JsonDispatch does not prescribe a support-window duration.

9.4 Schema compatibility
------------------------

The schema at a published version is immutable. Corrections that change which
instances validate require a new specification version and a new artifact
path.

Producers MUST NOT replace a published schema or fixture in place. Documentation
may correct prose without a new schema path only when the correction does not
change conforming behavior.
