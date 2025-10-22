7. Properties & References
==========================

JsonDispatch goes beyond just returning ``status`` and ``data``. It introduces two companion sections —
``_properties`` and ``_references`` — to make responses **self-descriptive** and **context-aware** without extra API calls.


7.1 ``_properties`` — Describe Your Data, Not Just Send It
-----------------------------------------------------------

The ``_properties`` object carries **metadata about the ``data`` field**. It helps clients understand the payload’s
structure, count, pagination, and even its lifecycle (like deprecation or schema changes).

.. list-table::
   :header-rows: 1
   :widths: 22 18 60

   * - Field
     - Type
     - Purpose
   * - ``type``
     - string
     - Type of data (``array``, ``object``, ``string``, ``number``, ``boolean``).
   * - ``name``
     - string
     - Logical name for this data block.
   * - ``template``
     - string (URL)
     - Optional link to a JSON Schema or template definition.
   * - ``deprecation``
     - string (URL)
     - Optional link marking this resource as deprecated.
   * - ``count``
     - integer
     - Total number of items if the data is an array.
   * - ``range``
     - string
     - Range of records in paginated results (e.g., ``"21-40"``).
   * - ``page``
     - integer
     - Current page number, if paginated.

**Example**

.. code-block:: json

   "_properties": {
     "data": {
       "type": "array",
       "name": "articles",
       "count": 20,
       "page": 2,
       "range": "21-40",
       "deprecation": "https://api.example.com/docs/v2/articles"
     }
   }

This tells the client:

- The ``data`` is an array named ``articles``.
- It contains 20 items, displaying page 2 (items 21–40).
- The endpoint is deprecated in favor of the linked v2 spec.

**Best practice:** Always include at least ``type`` and ``name``. This enables automated clients (CLI tools, SDKs, data grids) to interpret results correctly.


7.2 ``_references`` — Replace IDs with Meaning
-----------------------------------------------

The ``_references`` object defines **lookup tables** that map internal IDs or codes to human-readable labels.
It eliminates the need for extra “dictionary” or “enum” endpoints.

**Example**

.. code-block:: json

   "_references": {
     "category": {
       "1": "News",
       "2": "Tutorial",
       "3": "Opinion"
     },
     "status": {
       "A": "Active",
       "I": "Inactive",
       "S": "Suspended"
     }
   }

When a record includes ``"category": 2``, the client can instantly render **“Tutorial”** using the mapping.

**Best practice:** Keep keys short and meaningful (e.g., ``category``, ``status``, ``role``) that directly correspond to the field names inside ``data``.


7.3 Choosing Between Them
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 56 22 22

   * - Use Case
     - Use ``_properties``
     - Use ``_references``
   * - Describe structure, pagination, or schema
     - ✅
     - 
   * - Translate IDs or codes to labels
     - 
     - ✅
   * - Mark field as deprecated or link to template
     - ✅
     - 
   * - Enumerate possible options or states
     - 
     - ✅


7.4 Example — Combined in One Response
--------------------------------------

.. code-block:: json

   {
     "status": "success",
     "message": "Articles listed successfully",
     "data": [
       {
         "id": 1,
         "title": "Intro to JsonDispatch",
         "category": 1
       },
       {
         "id": 2,
         "title": "Error Handling Patterns",
         "category": 3
       }
     ],
     "_properties": {
       "data": {
         "type": "array",
         "name": "articles",
         "count": 2,
         "page": 1,
         "range": "1-2"
       }
     },
     "_references": {
       "category": {
         "1": "News",
         "2": "Tutorial",
         "3": "Opinion"
       }
     }
   }

Clients can now:

- Display labels directly using ``_references``.
- Understand that ``data`` is paginated and typed via ``_properties``.
- Do all this **without extra round-trips** or hard-coded logic.


7.5 Nested ``_references`` Example
----------------------------------

Complex datasets often include **hierarchical or multi-level relationships** — e.g., categories, subcategories, or status groups.
JsonDispatch supports **nested ``_references``** so you can express those relationships cleanly while keeping the payload compact.

This allows clients to resolve **multi-level identifiers** without multiple API calls.

**Example — Category → Subcategory → Label Mapping**

.. code-block:: json

   {
     "status": "success",
     "message": "Product list with hierarchical references",
     "data": [
       { "id": 1, "name": "iPhone 15", "category": 10, "subcategory": 101 },
       { "id": 2, "name": "Galaxy S24", "category": 10, "subcategory": 102 },
       { "id": 3, "name": "MacBook Air", "category": 20, "subcategory": 201 }
     ],
     "_references": {
       "category": {
         "10": {
           "label": "Mobile",
           "children": {
             "101": "Apple",
             "102": "Samsung"
           }
         },
         "20": {
           "label": "Laptop",
           "children": {
             "201": "Apple",
             "202": "Windows"
           }
         }
       }
     },
     "_properties": {
       "data": {
         "type": "array",
         "name": "products",
         "count": 3
       }
     }
   }

**Explanation**

.. list-table::
   :header-rows: 1
   :widths: 22 78

   * - Field
     - Purpose
   * - ``category``
     - Maps high-level IDs (``10``, ``20``) to parent labels.
   * - ``children``
     - Maps subcategory IDs to their names under each parent.
   * - ``label``
     - A friendly label for the parent category.
   * - ``_references``
     - Keeps the hierarchy readable and cacheable on the client.

**Why it matters**

- **Fewer round-trips** — clients can render category and subcategory labels directly.
- **Extensible** — future nesting levels (e.g., regions → countries → cities) follow the same pattern.
- **Localized references** — ``_references`` can hold language-specific labels if needed.

**Client behavior**

When parsing, clients should:

#. Resolve ``subcategory`` first within its parent ``category``.
#. Fallback to top-level label if no match is found.
#. Cache ``_references`` by version to avoid redundant lookups.

**Best practice:** Use nested ``_references`` only when relationships are **stable and bounded**. For dynamic trees, prefer dedicated endpoints (``/categories``, ``/locations``).
