8. Links
========

APIs aren’t just about data — they’re about **navigating between resources**.
JsonDispatch provides a ``_links`` object that helps clients discover where to go next without guessing or relying on
hard-coded routes.

The goal is simple:
➡️ **Make your API self-navigable** — so clients can move through it like a website, not a maze.


8.1 ``_links`` for Pagination
-----------------------------

Whenever your response includes a collection or list, include pagination links to guide the client.

.. list-table::
   :header-rows: 1
   :widths: 18 82

   * - Key
     - Purpose
   * - ``self``
     - URL of the current page
   * - ``next``
     - Next page (if available)
   * - ``prev``
     - Previous page (if available)
   * - ``first``
     - First page in the dataset
   * - ``last``
     - Last page in the dataset

**Example**

.. code-block:: json

   "_links": {
     "self":  "https://api.example.com/articles?page=2&limit=10",
     "next":  "https://api.example.com/articles?page=3&limit=10",
     "prev":  "https://api.example.com/articles?page=1&limit=10",
     "first": "https://api.example.com/articles?page=1&limit=10",
     "last":  "https://api.example.com/articles?page=50&limit=10"
   }

This lets clients paginate seamlessly — no manual query-building or separate pagination logic required.

**Tip:** Include ``self`` in every response. It makes your payload self-documenting when viewed in isolation.


8.2 ``_links`` for Related Resources
------------------------------------

Beyond pagination, ``_links`` can expose **relationships** or **related resources**. These hints tell the client where
additional or contextual information lives.

**Example**

.. code-block:: json

   "_links": {
     "self":     "https://api.example.com/articles/42",
     "author":   "https://api.example.com/users/99",
     "comments": "https://api.example.com/articles/42/comments",
     "related":  "https://api.example.com/tutorials/jsondispatch"
   }

Now, clients can:

- Navigate to the author or comments without extra documentation.
- Preload related data efficiently.
- Treat your API like a graph of connected resources.


8.3 ``_links`` with Metadata (Enriched Links)
---------------------------------------------

Sometimes you need to describe **how** a link should be used — not just where it points. In such cases, ``_links``
entries can be full objects containing an ``href`` and a ``meta`` section.

**Example**

.. code-block:: json

   "_links": {
     "self": {
       "href": "https://api.example.com/articles/42",
       "meta": {
         "method": "GET",
         "auth": "required"
       }
     },
     "edit": {
       "href": "https://api.example.com/articles/42",
       "meta": {
         "method": "PUT",
         "auth": "editor-role"
       }
     },
     "delete": {
       "href": "https://api.example.com/articles/42",
       "meta": {
         "method": "DELETE",
         "auth": "admin-role"
       }
     }
   }

This pattern makes ``_links`` expressive and safe for **HATEOAS-style** APIs. It tells clients both *where* to go and
*how* to interact, without needing extra documentation.


8.4 Best Practices for ``_links``
---------------------------------

- Always include ``self``. It’s essential for debugging and introspection.
- Keep URLs **absolute** (never relative).
- Use **consistent naming** (``next``, ``prev``, ``author``, ``related``, ``edit``, ``delete``, etc.).
- Avoid embedding authentication tokens directly in URLs.
- When possible, pair ``_links`` with ``_properties`` to describe pagination metadata (``page``, ``count``, etc.).


8.5 ``_links`` for Files and Downloads
--------------------------------------

APIs frequently serve or reference **files** — such as reports, invoices, exports or media. JsonDispatch supports this
cleanly through ``_links``, using either **direct URLs** or **expirable signed URLs** under a dedicated ``file`` or
``download`` key.

This keeps your responses self-descriptive, avoids embedding raw file data and enables clients to access assets securely.

**Example — Direct File Link (Public Resource)**

.. code-block:: json

   {
     "status": "success",
     "message": "Activity report generated successfully",
     "data": {
       "report_id": "RPT-2025-10-06",
       "type": "activity",
       "period": "2025-09",
       "size": "2.4 MB"
     },
     "_links": {
       "self": "https://api.example.com/reports/RPT-2025-10-06",
       "file": "https://cdn.example.com/reports/RPT-2025-10-06.pdf"
     },
     "_properties": {
       "data": { "type": "object", "name": "report" }
     }
   }

**Use this when** files are **public or long-lived** (e.g., CDN-hosted assets or documentation).

**Example — Signed File Link (Secure or Temporary Access)**

.. code-block:: json

   {
     "status": "success",
     "message": "Report ready for download",
     "data": {
       "report_id": "RPT-2025-10-06",
       "type": "activity",
       "expires_in": 900
     },
     "_links": {
       "self": "https://api.example.com/reports/RPT-2025-10-06",
       "download": {
         "href": "https://api.example.com/reports/RPT-2025-10-06/download?token=eyJhbGciOiJIUzI1...",
         "meta": {
           "method": "GET",
           "auth": "required",
           "expires": "2025-10-06T12:30:00Z"
         }
       }
     }
   }

**Use this when:**

- Files are **user-specific** or **sensitive** (exports, invoices, personal data).
- Links must **expire** or require **authentication**.
- You want to guide clients explicitly on how to fetch the file (via ``meta``).

**Example — Multiple File Formats**

.. code-block:: json

   {
     "_links": {
       "pdf":  "https://cdn.example.com/reports/RPT-2025-10-06.pdf",
       "csv":  "https://cdn.example.com/reports/RPT-2025-10-06.csv",
       "json": "https://api.example.com/reports/RPT-2025-10-06.json"
     }
   }

Clients can choose their preferred format programmatically — ideal for exports or analytics dashboards.

**Best Practices**

.. list-table::
   :header-rows: 1
   :widths: 52 48

   * - Guideline
     - Why
   * - Always use HTTPS links
     - Prevents man-in-the-middle interception.
   * - Include ``meta`` when authentication or expiry applies
     - Clients can display expiry timers or handle refresh logic.
   * - Avoid embedding file data inline
     - Reduces payload size and memory footprint.
   * - Prefer ``download`` over generic link names
     - Keeps semantics consistent across endpoints.

**Summary**

File links under ``_links`` make your API:

- **Predictable** → consistent structure for downloads
- **Secure** → signed URLs and metadata guidance
- **Portable** → clients can consume them without custom conventions


8.6 ``_links`` for Inline Media (Thumbnails, Avatars, Previews)
----------------------------------------------------------------

Not every file link is a downloadable document — many APIs include **media previews** such as user avatars, product
thumbnails or video stills. JsonDispatch keeps this consistent by defining them under ``_links.media`` or
``_links.image``, so clients can handle them predictably.

**Example — Simple Inline Media Links**

.. code-block:: json

   {
     "status": "success",
     "message": "User profile fetched successfully",
     "data": {
       "id": 99,
       "name": "A. B. M. Mahmudul Hasan",
       "role": "admin"
     },
     "_links": {
       "self": "https://api.example.com/users/99",
       "avatar": "https://cdn.example.com/avatars/99-thumb.jpg"
     },
     "_properties": {
       "data": { "type": "object", "name": "user" }
     }
   }

Ideal for lightweight references such as **user photos**, **brand icons**, or **thumbnail images**.

**Example — Media with Multiple Resolutions or Types**

.. code-block:: json

   {
     "_links": {
       "self": "https://api.example.com/products/2001",
       "image": {
         "small":  "https://cdn.example.com/products/2001/small.jpg",
         "medium": "https://cdn.example.com/products/2001/medium.jpg",
         "large":  "https://cdn.example.com/products/2001/large.jpg"
       }
     }
   }

Clients can choose which variant to use — perfect for responsive frontends or apps that cache different image sizes.

**Example — Rich Media Metadata**

When returning multiple images, videos, or icons, each media entry can include metadata for display and accessibility:

.. code-block:: json

   {
     "_links": {
       "thumbnail": {
         "href": "https://cdn.example.com/products/2001/thumb.webp",
         "meta": {
           "width": 120,
           "height": 120,
           "type": "image/webp",
           "alt": "Product preview image"
         }
       },
       "video_preview": {
         "href": "https://cdn.example.com/products/2001/preview.mp4",
         "meta": {
           "duration": 12,
           "type": "video/mp4",
           "poster": "https://cdn.example.com/products/2001/thumb.jpg"
         }
       }
     }
   }

This allows advanced clients (e.g., web dashboards, mobile apps) to render previews, use proper MIME types and preload efficiently.

**Best Practices**

.. list-table::
   :header-rows: 1
   :widths: 62 38

   * - Guideline
     - Reason
   * - Use separate keys for image vs. video (e.g., ``avatar``, ``thumbnail``, ``video_preview``)
     - Keeps structure clear and predictable.
   * - Include ``meta.type`` for MIME hints (``image/png``, ``video/mp4``)
     - Helps browsers and SDKs preload correctly.
   * - Prefer WebP or AVIF for image efficiency
     - Saves bandwidth for clients.
   * - Use ``_links`` — not ``_references`` — for any URL-based assets
     - Keeps semantics clean (navigation vs. lookup).

**Summary**

Inline media links under ``_links`` let APIs describe:

- **Where** assets are located (``href``)
- **What** they are (``meta.type``, ``meta.alt``)
- **How** to use them (variants, resolutions, roles)

They make your API **visual-friendly**, **cache-efficient** and **self-documenting** — no guesswork or extra endpoints needed.
