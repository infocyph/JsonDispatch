5. Examples
===========

.. note::

   This chapter is non-normative. The schemas and normative chapters determine
   conformance.

5.1 Success
-----------

.. code-block:: http

   HTTP/1.1 200 OK
   Content-Type: application/vnd.infocyph.jd.v3+json; charset=utf-8
   X-Api-Version-Selected: 1.4.2
   X-Request-Id: 019fb440-4e83-7b1b-9ef9-44a80771f181
   Vary: Accept, X-Api-Version

.. code-block:: json

   {
     "status": "success",
     "data": {
       "id": "article-42",
       "title": "JsonDispatch 3"
     },
     "_links": {
       "self": "https://api.example.com/articles/article-42"
     }
   }

5.2 Validation failure
----------------------

.. code-block:: http

   HTTP/1.1 422 Unprocessable Content
   Content-Type: application/vnd.infocyph.jd.v3+json; charset=utf-8
   X-Api-Version-Selected: 1.4.2
   X-Request-Id: 019fb440-4e83-7b1b-9ef9-44a80771f182
   Vary: Accept, X-Api-Version

.. code-block:: json

   {
     "status": "fail",
     "message": "Validation failed",
     "data": [
       {
         "code": "TITLE_TOO_SHORT",
         "title": "Title is too short",
         "detail": "Provide at least five characters.",
         "source": {
           "pointer": "/title"
         }
       },
       {
         "code": "CATEGORY_INVALID",
         "title": "Category is invalid",
         "source": {
           "pointer": "/category"
         },
         "meta": {
           "allowed": ["news", "tutorial", "opinion"]
         }
       }
     ]
   }

5.3 Dependency error
--------------------

.. code-block:: http

   HTTP/1.1 503 Service Unavailable
   Content-Type: application/vnd.infocyph.jd.v3+json; charset=utf-8
   X-Api-Version-Selected: 1.4.2
   X-Request-Id: 019fb440-4e83-7b1b-9ef9-44a80771f183
   Vary: Accept, X-Api-Version
   Retry-After: 30

.. code-block:: json

   {
     "status": "error",
     "message": "The service is temporarily unavailable",
     "data": [
       {
         "code": "DEPENDENCY_UNAVAILABLE",
         "title": "A required dependency did not respond",
         "source": {
           "resource": "article-store"
         }
       }
     ]
   }

5.4 Restricted-transport error
------------------------------

This form is used only when the deployment cannot carry a native ``5xx``
status and both producer and consumer have enabled status tunneling.

.. code-block:: http

   HTTP/1.1 200 OK
   Content-Type: application/vnd.infocyph.jd.v3+json; charset=utf-8
   X-Api-Version-Selected: 1.4.2
   X-Request-Id: 019fb440-4e83-7b1b-9ef9-44a80771f184
   Vary: Accept, X-Api-Version
   X-JD-Status-Code: 503
   Cache-Control: no-store

.. code-block:: json

   {
     "status": "error",
     "status_code": 503,
     "message": "The service is temporarily unavailable",
     "data": [
       {
         "code": "DEPENDENCY_UNAVAILABLE",
         "title": "A required dependency did not respond"
       }
     ]
   }

5.5 Offset pagination
---------------------

.. code-block:: json

   {
     "status": "success",
     "data": [
       {"id": "article-21"},
       {"id": "article-22"}
     ],
     "_properties": {
       "/data": {
         "type": "array",
         "name": "articles",
         "pagination": {
           "mode": "offset",
           "offset": 20,
           "limit": 2,
           "count": 2,
           "total": 48
         }
       }
     },
     "_links": {
       "self": "https://api.example.com/articles?offset=20&limit=2",
       "next": "https://api.example.com/articles?offset=22&limit=2",
       "prev": "https://api.example.com/articles?offset=18&limit=2",
       "first": "https://api.example.com/articles?offset=0&limit=2",
       "last": "https://api.example.com/articles?offset=46&limit=2"
     }
   }

5.6 Cursor pagination
---------------------

.. code-block:: json

   {
     "status": "success",
     "data": [
       {"id": "article-101"},
       {"id": "article-102"}
     ],
     "_properties": {
       "/data": {
         "type": "array",
         "name": "articles",
         "pagination": {
           "mode": "cursor",
           "limit": 2,
           "count": 2,
           "has_more": true,
           "next_cursor": "eyJpZCI6MTAyfQ"
         }
       }
     },
     "_links": {
       "self": "https://api.example.com/articles?limit=2",
       "next": "https://api.example.com/articles?limit=2&cursor=eyJpZCI6MTAyfQ"
     }
   }

5.7 References
--------------

.. code-block:: json

   {
     "status": "success",
     "data": [
       {"id": "article-42", "category": 2}
     ],
     "_references": {
       "/data/*/category": {
         "1": "News",
         "2": "Tutorial",
         "3": "Opinion"
       }
     }
   }
