Fixture reference
=================

The fixture manifest declares whether every example must pass or fail and names
the normative rule exercised by that fixture.

:download:`Download manifest.json <../../fixtures/v3/manifest.json>`

.. literalinclude:: ../../fixtures/v3/manifest.json
   :language: json
   :linenos:

Representative positive fixtures
--------------------------------

Minimal success
^^^^^^^^^^^^^^^

:download:`Download minimal-success.json <../../fixtures/v3/positive/minimal-success.json>`

.. literalinclude:: ../../fixtures/v3/positive/minimal-success.json
   :language: json
   :linenos:

Cursor pagination
^^^^^^^^^^^^^^^^^

:download:`Download cursor-pagination.json <../../fixtures/v3/positive/cursor-pagination.json>`

.. literalinclude:: ../../fixtures/v3/positive/cursor-pagination.json
   :language: json
   :linenos:

Validation failure
^^^^^^^^^^^^^^^^^^

:download:`Download validation-fail.json <../../fixtures/v3/positive/validation-fail.json>`

.. literalinclude:: ../../fixtures/v3/positive/validation-fail.json
   :language: json
   :linenos:

Restricted-transport error
^^^^^^^^^^^^^^^^^^^^^^^^^^

:download:`Download tunneled-dependency-error.json <../../fixtures/v3/positive/tunneled-dependency-error.json>`

.. literalinclude:: ../../fixtures/v3/positive/tunneled-dependency-error.json
   :language: json
   :linenos:

Representative negative fixture
-------------------------------

The following response is intentionally invalid because its HTTP status and
envelope status disagree.

:download:`Download http-envelope-status-mismatch.json <../../fixtures/v3/negative/http-envelope-status-mismatch.json>`

.. literalinclude:: ../../fixtures/v3/negative/http-envelope-status-mismatch.json
   :language: json
   :linenos:

The complete positive and negative collections are declared by the fixture
manifest and remain available from the versioned raw artifact tree.
