# 5. Response Examples

This section provides production-ready examples for:

## 5.1 Simple success
Returns a single resource with `_references` mapping.

## 5.2 Fail (validation)
`422 Unprocessable Entity` with field-level pointers.

## 5.3 Error (system failure)
`503 Service Unavailable` with `code` and dependency name.

## 5.4 Paginated collection
Includes `_properties.data` pagination metadata and `_links`.

## 5.5 References in action
How clients resolve enums without extra calls.

## 5.6 Async & long-running operations
Pattern for `202 Accepted` job creation, status polling, webhooks, and failure reporting.

## 5.7 Bulk operations & partial success
Use `207 Multi-Status` for best-effort batches; include `summary` and per-item results.
