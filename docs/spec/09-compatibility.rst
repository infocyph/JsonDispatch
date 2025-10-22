9. Compatibility & Evolution
============================

JsonDispatch is designed for **long-lived APIs** that evolve gracefully without breaking existing clients.

.. important::

   ⚙️ **Evolve forward, never break back.**


9.1 Core Compatibility Rules
----------------------------

When making changes to your API responses:

- **Never remove a field.** Old clients may still depend on it.
- **Never change the type** of an existing field. A string should never become an object and an object should never
  become an array.
- **Only add new fields** (preferably optional ones with sensible defaults).
- **Deprecate before removing.** Mark old fields with ``_properties.deprecation`` and provide documentation for migration.

**Example**

.. code-block:: json

   {
     "_properties": {
       "legacyTitle": {
         "type": "string",
         "name": "legacy-title",
         "deprecation": "https://api.example.com/docs/v2/articles#title"
       }
     }
   }

This approach ensures:

- Older clients keep working as expected.
- Newer clients can progressively adopt new structures.


9.2 How to Introduce Breaking Changes
-------------------------------------

When a breaking change becomes necessary:

1. Increment the **major version** in the response’s ``Content-Type``.

   .. code-block:: http

      Content-Type: application/vnd.infocyph.jd.v2+json
      X-Api-Version: 2.0.0

2. Maintain the old major version (v1) in production for a transition period. Deprecate it gradually using
   communication and version headers.
3. Publish updated documentation for each major version side-by-side.
4. Avoid “soft breaks” (changing existing semantics without version bumps). Always be explicit.


9.3 Recommended Evolution Workflow
----------------------------------

.. list-table::
   :header-rows: 1
   :widths: 10 30 60

   * - Step
     - Action
     - Example
   * - 1
     - Add field
     - Add ``_properties.template``
   * - 2
     - Mark old field deprecated
     - ``_properties.oldField.deprecation``
   * - 3
     - Announce upcoming version
     - Changelog + docs
   * - 4
     - Introduce new major version
     - ``v2`` media type
   * - 5
     - Sunset old version
     - Remove after clients migrate
