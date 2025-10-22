# 4. Response Envelope (The Outer Wrapper)

Every JsonDispatch **response** is wrapped in a predictable envelope:

| Key           | Type   | Required | Purpose                                          |
|---------------|--------|----------|--------------------------------------------------|
| `status`      | string | ✅        | `success`, `fail`, or `error`                    |
| `message`     | string | ⚪        | Human-friendly short description                 |
| `data`        | mixed  | ⚪        | Main payload                                     |
| `_references` | object | ⚪        | ID→label maps                                    |
| `_properties` | object | ⚪        | Metadata (type, pagination, deprecation, etc.)   |
| `_links`      | object | ⚪        | Pagination/related resources                     |

Includes detailed guidance for:
- **`status`** semantics
- **`message`** tone
- **`data`** expectations by outcome
- **`_references`** examples
- **`_properties`** patterns
- **`_links`** pagination & relations
