10. Implementation recommendations
==================================

.. note::

   This chapter is non-normative. It does not add conformance requirements.

10.1 Construct only selected data
---------------------------------

Build optional fields, references, properties, and links only when the selected
application representation requires them. Avoid loading relations or computing
counts merely to decorate an envelope.

For large collections, stream or incrementally encode when the host runtime can
preserve valid JSON and bounded memory. Native NDJSON and file streams are
outside JsonDispatch and may be better for exports.

10.2 Prefer cursor pagination at scale
--------------------------------------

Offset pagination is convenient for small or randomly accessible collections.
Cursor pagination generally gives more stable traversal and avoids increasingly
expensive deep offsets. Keep cursors opaque, signed or otherwise integrity
protected when clients must not alter their contents.

Do not calculate an exact total unless clients need it and the underlying store
can provide it within the endpoint's performance budget.

10.3 Observability
------------------

Include the generated request identifier in structured logs and telemetry.
Keep correlation and trace identifiers separate so operators can distinguish
one HTTP request from a wider workflow.

Never log entire envelopes indiscriminately. Payloads and issue metadata may
contain personal or confidential application data.

10.4 Caching
------------

Account for ``Accept`` and ``X-Api-Version`` in shared-cache keys. Preserve the
required ``Vary`` fields through reverse proxies and CDNs.

Choose application-appropriate cache controls. JsonDispatch does not require
all responses to be private or non-cacheable.

10.5 Links and metadata
-----------------------

Prefer a stable ``self`` relation for resource and collection responses. Treat
all received links as untrusted URI-references and apply the client's normal
origin, scheme, and navigation policy.

Keep reference maps and link metadata bounded. Large dictionaries, resource
trees, and file catalogs are usually better represented as normal resources.

10.6 Safe failures
------------------

Use stable issue codes and public-safe titles. Put only information a caller is
authorized to see in ``detail`` and ``meta``. Capture private diagnostics in
server-side telemetry associated with ``X-Request-Id``.

Return multiple validation issues in deterministic order when doing so is
useful. A fail-fast endpoint may return one issue and still conform.

10.7 Conformance in delivery pipelines
--------------------------------------

Validate representative real responses, not only hand-written fixtures. Run
the published positive and negative fixtures whenever the pinned JsonDispatch
version changes.

Schema validation proves document structure. Separate integration tests should
also verify HTTP status, media negotiation, header generation, pagination link
semantics, and failure redaction.
