# JsonDispatch

[![Specification checks](https://github.com/infocyph/JsonDispatch/actions/workflows/specification.yml/badge.svg)](https://github.com/infocyph/JsonDispatch/actions/workflows/specification.yml)
[![Specification](https://img.shields.io/badge/specification-3.0.0-3154a5.svg)](specification.json)

JsonDispatch is a language-neutral specification for predictable JSON HTTP
responses. It standardizes outcome semantics, errors, representation
negotiation, request identification, links, references, and offset or cursor
pagination without prescribing an application framework or programming
language.

**[Read the published specification](https://docs.infocyph.com/projects/json-dispatch/)**

## Response contract

Every JsonDispatch response uses one of three outcomes:

| Status | HTTP class | Meaning |
| --- | --- | --- |
| `success` | `2xx` | The operation completed successfully. |
| `fail` | `4xx` | The request requires a client-side change. |
| `error` | `5xx` | The producer or a dependency could not complete a valid request. |

```http
HTTP/1.1 200 OK
Content-Type: application/vnd.infocyph.jd.v3+json; charset=utf-8
X-Api-Version-Selected: 1.4.2
X-Request-Id: 019fb440-4e83-7b1b-9ef9-44a80771f181
Vary: Accept, X-Api-Version
```

```json
{
  "status": "success",
  "data": {
    "id": "article-42",
    "title": "A predictable response contract"
  },
  "_links": {
    "self": "https://api.example.com/articles/article-42"
  }
}
```

The complete envelope, failure, metadata, and pagination rules are defined by
the normative specification and its versioned schemas.

## Versioning

JsonDispatch versioning and application API versioning are separate contracts:

| Signal | Purpose |
| --- | --- |
| `application/vnd.<vendor>.jd.v3+json` | Selects JsonDispatch major version 3. |
| `X-Api-Version` | Requests an application API version. |
| `X-Api-Version-Selected` | Reports the exact application API version served. |
| `specification.json` | Pins the complete JsonDispatch specification release. |

Implementations should pin the complete specification version rather than
depending only on the media-type major.

## Conformance artifacts

Conformance is defined jointly by the normative prose and machine-readable
artifacts:

| Artifact | Purpose |
| --- | --- |
| [Specification source](docs/spec) | Normative requirements, examples, and implementation recommendations |
| [Version manifest](specification.json) | Current specification and artifact locations |
| [JSON Schemas](schemas/v3) | Envelope, HTTP response, issue, link, property, reference, and pagination validation |
| [Positive fixtures](fixtures/v3/positive) | Canonical conforming responses |
| [Negative fixtures](fixtures/v3/negative) | Responses that implementations must reject |
| [Fixture manifest](fixtures/v3/manifest.json) | Expected result and violated rule for every fixture |

Current published development artifacts:

- [Envelope schema](https://docs.infocyph.com/projects/json-dispatch/en/latest/schemas/v3/envelope.schema.json)
- [HTTP-response schema](https://docs.infocyph.com/projects/json-dispatch/en/latest/schemas/v3/http-response.schema.json)
- [Fixture manifest](https://docs.infocyph.com/projects/json-dispatch/en/latest/fixtures/v3/manifest.json)
- [Specification manifest](https://docs.infocyph.com/projects/json-dispatch/en/latest/specification.json)

Rules that cannot be expressed completely by JSON Schema—such as HTTP
field-name case insensitivity, media-range selection, identifier uniqueness,
pagination arithmetic, and sensitive-data redaction—remain normative and
require implementation-level tests.

## Validate locally

Requires Python 3.11 or later.

```bash
python3 -m pip install -r docs/requirements.txt
python3 tools/check_conformance.py
python3 -m sphinx -W --keep-going -b html docs docs/_build/html
```

The conformance check verifies all schemas, the specification and fixture
manifests, every positive fixture, and every negative fixture. The same checks
run in GitHub Actions and before Read the Docs publishes a build.

## Project scope

This repository owns the JsonDispatch specification and its conformance
artifacts. It intentionally contains no runtime implementation, Composer
package, framework adapter, middleware, authentication system, or storage
integration.

Language and framework implementations remain independent projects and prove
compatibility against a pinned JsonDispatch release.

## Normative changes

A change to normative behavior must:

1. use the standards language defined by the specification;
2. update every affected chapter and schema consistently;
3. add positive or negative fixtures for machine-testable behavior;
4. preserve published artifacts unchanged; and
5. follow semantic versioning when conformance behavior changes.
