Conformance artifacts
=====================

JsonDispatch publishes each conformance artifact in two forms:

- themed documentation pages for people, with syntax highlighting and context;
- unchanged JSON files for validators, generators, and automated tests.

The rendered pages are part of the normal Sphinx documentation. Raw files keep
stable relative paths inside every Read the Docs version.

.. toctree::
   :maxdepth: 1

   schemas
   fixtures

Machine-readable manifest
-------------------------

:download:`Download specification.json <../../specification.json>`

Read the Docs creates a versioned artifact URL only after that version is
activated and built. Use the ``latest`` build while developing and the
corresponding immutable version after release.
