8. Links
========

8.1 Link map
------------

``_links`` is a non-empty object mapping link-relation names to link values.
A relation name MUST be a registered relation token, an application-defined
lowercase token, or an absolute URI.

A link value is either:

- a non-empty URI-reference string; or
- an object with REQUIRED ``href`` and optional ``type``, ``title``,
  ``hreflang``, and ``meta`` members.

Example:

.. code-block:: json

   "_links": {
     "self": "https://api.example.com/articles/article-42",
     "alternate": {
       "href": "https://api.example.com/articles/article-42.html",
       "type": "text/html",
       "hreflang": "en",
       "title": "HTML representation"
     }
   }

``href`` MUST be a non-empty URI-reference. ``type``, when present, MUST be a
media type. ``hreflang``, when present, MUST be a language tag. ``meta`` MAY
contain application-defined JSON members.

Unknown members in a link object are invalid.

8.2 Resolution and safety
-------------------------

Relative URI-references are resolved against the effective request URI unless
the application API documents another base.

Clients MUST treat link values as untrusted input. A link does not grant
authorization and does not require a client to follow it. JsonDispatch does
not place credentials, roles, authentication schemes, or executable actions in
link objects.

8.3 Pagination relations
------------------------

Pagination uses these relations:

.. list-table::
   :header-rows: 1
   :widths: 18 82

   * - Relation
     - Meaning
   * - ``self``
     - Current collection representation
   * - ``next``
     - Next collection window
   * - ``prev``
     - Previous collection window
   * - ``first``
     - First offset window
   * - ``last``
     - Last offset window when the total is known

The presence rules in Chapter 7 are normative. A producer MUST preserve all
non-pagination query semantics, including sparse fieldsets, filters, and sort
order, when constructing pagination links.

For cursor pagination, links SHOULD carry the opaque cursor so a client does
not need to construct a URI. The corresponding cursor remains in
``_properties`` for clients that use a separately documented transport.

8.4 Related resources and files
-------------------------------

Application-defined relations MAY identify related resources, documentation,
or files. Native file bytes are returned using their own media type and are
outside the JsonDispatch envelope.

Temporary links MAY expose expiry information in ``meta``. Sensitive tokens in
URI query strings SHOULD be short-lived and scoped by the application. These
recommendations do not define an authentication mechanism.
