# JsonDispatch

JsonDispatch is a language-neutral specification for JSON HTTP response
envelopes. It defines response status semantics, representation negotiation,
identification headers, error details, links, references, and offset/cursor
pagination metadata.

**Published documentation:**

https://docs.infocyph.com/projects/json-dispatch/

The documentation is hosted by Read the Docs as a subproject. Versioned builds
use
``https://docs.infocyph.com/projects/json-dispatch/<language>/<version>/``;
for example, the current development build is available under
[/en/latest/](https://docs.infocyph.com/projects/json-dispatch/en/latest/).

The current normative specification is **JsonDispatch 3.0.0**. An
application's API version is independent from the JsonDispatch specification
version:

- `application/vnd.<vendor>.jd.v3+json` selects JsonDispatch major version 3.
- `X-Api-Version` requests an application API version.
- `X-Api-Version-Selected` reports the application API version served.

## Normative specification

The canonical rendered specification is published at the documentation URL
above. Its source is maintained in [docs/spec](docs/spec). Start with:

- [Conformance and terminology](docs/spec/01-introduction.rst)
- [Media types and versioning](docs/spec/02-media-types-versioning.rst)
- [Response envelope](docs/spec/04-envelope.rst)
- [Errors](docs/spec/06-error-handling.rst)
- [Conformance artifacts](docs/spec/11-appendix.rst)

Versioned machine-readable artifacts are in [schemas/v3](schemas/v3).
Positive and negative examples are in [fixtures/v3](fixtures/v3).
Read the Docs publishes these unchanged at:

- https://docs.infocyph.com/projects/json-dispatch/en/3.0.0/schemas/v3/
- https://docs.infocyph.com/projects/json-dispatch/en/3.0.0/fixtures/v3/

## Validate

```bash
python3 -m pip install -r docs/requirements.txt
python3 tools/check_conformance.py
sphinx-build -W --keep-going -b html docs docs/_build/html
```

JsonDispatch contains no PHP implementation, Composer package, framework
adapter, authentication system, middleware, or runtime dependency.
