# API Endpoints Documentation

Base URL: `http://localhost:8000/api/`

All endpoints return JSON responses.

---

## 1. Create a Note

**Endpoint:** `POST /api/notes/`

**Description:** Create a new note with title, text, and original language.

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
    "title": "My First Note",
    "text": "This is a sample note text that I want to translate later.",
    "original_language": "en"
}
```

**Response (201 Created):**
```json
{
    "id": 1,
    "title": "My First Note",
    "text": "This is a sample note text that I want to translate later.",
    "original_language": "en",
    "translated_text": null,
    "translated_language": null,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/notes/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Note",
    "text": "This is a sample note text that I want to translate later.",
    "original_language": "en"
  }'
```

---

## 2. List All Notes

**Endpoint:** `GET /api/notes/`

**Description:** Retrieve all notes (paginated, 10 per page).

**Response (200 OK):**
```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 2,
            "title": "Second Note",
            "text": "Another note example",
            "original_language": "en",
            "translated_text": null,
            "translated_language": null,
            "created_at": "2024-01-15T10:35:00Z",
            "updated_at": "2024-01-15T10:35:00Z"
        },
        {
            "id": 1,
            "title": "My First Note",
            "text": "This is a sample note text that I want to translate later.",
            "original_language": "en",
            "translated_text": null,
            "translated_language": null,
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T10:30:00Z"
        }
    ]
}
```

**cURL Example:**
```bash
curl -X GET http://localhost:8000/api/notes/
```

**Pagination:**
- Add `?page=2` for next page: `GET /api/notes/?page=2`

---

## 3. Retrieve a Single Note

**Endpoint:** `GET /api/notes/{id}/`

**Description:** Retrieve a specific note by ID.

**Response (200 OK):**
```json
{
    "id": 1,
    "title": "My First Note",
    "text": "This is a sample note text that I want to translate later.",
    "original_language": "en",
    "translated_text": null,
    "translated_language": null,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
}
```

**cURL Example:**
```bash
curl -X GET http://localhost:8000/api/notes/1/
```

---

## 4. Update a Note

**Endpoint:** `PUT /api/notes/{id}/` or `PATCH /api/notes/{id}/`

**Description:** Update an existing note. Use `PUT` for full update, `PATCH` for partial update.

**Request Body (PUT - all fields required):**
```json
{
    "title": "Updated Note Title",
    "text": "Updated note text content",
    "original_language": "en"
}
```

**Request Body (PATCH - only fields to update):**
```json
{
    "title": "Updated Note Title"
}
```

**Response (200 OK):**
```json
{
    "id": 1,
    "title": "Updated Note Title",
    "text": "Updated note text content",
    "original_language": "en",
    "translated_text": null,
    "translated_language": null,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:45:00Z"
}
```

**cURL Example (PUT):**
```bash
curl -X PUT http://localhost:8000/api/notes/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Note Title",
    "text": "Updated note text content",
    "original_language": "en"
  }'
```

**cURL Example (PATCH):**
```bash
curl -X PATCH http://localhost:8000/api/notes/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Note Title"
  }'
```

---

## 5. Delete a Note

**Endpoint:** `DELETE /api/notes/{id}/`

**Description:** Delete a note by ID.

**Response (204 No Content):**
```
(Empty response body)
```

**cURL Example:**
```bash
curl -X DELETE http://localhost:8000/api/notes/1/
```

---

## 6. Translate a Note

**Endpoint:** `POST /api/notes/{id}/translate/`

**Description:** Translate a note to a target language. The translation is saved to the database and cached.

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
    "target_language": "hi"
}
```

**Response (200 OK):**
```json
{
    "id": 1,
    "title": "My First Note",
    "original_text": "This is a sample note text that I want to translate later.",
    "original_language": "en",
    "translated_text": "यह एक नमूना नोट पाठ है जिसे मैं बाद में अनुवाद करना चाहता हूं।",
    "translated_language": "hi",
    "cached": false
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/notes/1/translate/ \
  -H "Content-Type: application/json" \
  -d '{
    "target_language": "hi"
  }'
```

**Supported Language Codes:**
- `en` - English
- `hi` - Hindi
- `es` - Spanish
- `fr` - French
- `de` - German
- `ja` - Japanese
- `zh` - Chinese
- `ar` - Arabic
- And many more (ISO 639-1 language codes)

**Error Responses:**

**400 Bad Request - Same language:**
```json
{
    "error": "Target language cannot be the same as original language"
}
```

**404 Not Found:**
```json
{
    "detail": "Not found."
}
```

**503 Service Unavailable (if translation service unavailable):**
```json
{
    "error": "Translation service is not available. Please install googletrans."
}
```

---

## Complete Testing Workflow Example

### Step 1: Create a note
```bash
curl -X POST http://localhost:8000/api/notes/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Hello World",
    "text": "Hello, this is a test note in English.",
    "original_language": "en"
  }'
```

**Response:**
```json
{
    "id": 1,
    "title": "Hello World",
    "text": "Hello, this is a test note in English.",
    "original_language": "en",
    "translated_text": null,
    "translated_language": null,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
}
```

### Step 2: Translate the note to Hindi
```bash
curl -X POST http://localhost:8000/api/notes/1/translate/ \
  -H "Content-Type: application/json" \
  -d '{
    "target_language": "hi"
  }'
```

**Response:**
```json
{
    "id": 1,
    "title": "Hello World",
    "original_text": "Hello, this is a test note in English.",
    "original_language": "en",
    "translated_text": "नमस्ते, यह अंग्रेजी में एक परीक्षण नोट है।",
    "translated_language": "hi",
    "cached": false
}
```

### Step 3: Retrieve the note (now includes translation)
```bash
curl -X GET http://localhost:8000/api/notes/1/
```

**Response:**
```json
{
    "id": 1,
    "title": "Hello World",
    "text": "Hello, this is a test note in English.",
    "original_language": "en",
    "translated_text": "नमस्ते, यह अंग्रेजी में एक परीक्षण नोट है।",
    "translated_language": "hi",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:35:00Z"
}
```

---

## Notes

1. **Language Codes:** Use ISO 639-1 two-letter language codes (e.g., `en`, `hi`, `es`, `fr`).

2. **Caching:** Translations are cached for 1 hour. Subsequent translation requests for the same note and target language will return cached results.

3. **Pagination:** The list endpoint returns 10 notes per page by default.

4. **Error Handling:** All endpoints return appropriate HTTP status codes:
   - `200` - Success
   - `201` - Created
   - `204` - No Content (Delete)
   - `400` - Bad Request (Validation errors)
   - `404` - Not Found
   - `500` - Internal Server Error
   - `503` - Service Unavailable (Translation service)

