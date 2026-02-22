# Agent 02 Schema Docs

## `lesson_sources`
Purpose: Tracks each uploaded file or free-text topic through ingestion lifecycle.

```sql
CREATE TABLE lesson_sources (
  id TEXT PRIMARY KEY,
  user_id TEXT,
  filename TEXT NOT NULL,
  type TEXT NOT NULL,
  storage_url TEXT,
  status TEXT NOT NULL,
  error_message TEXT,
  input_mode TEXT NOT NULL,
  source_metadata TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
```

Field notes:
- `id`: stable source ID (UUID).
- `type`: one of `pdf`, `ppt`, `pptx`, `docx`, `txt`, `topic`.
- `status`: `queued`, `processing`, `completed`, or `failed`.
- `storage_url`: object path; `local://...`, `s3://...`, or `supabase://...`.
- `source_metadata`: JSON map with extraction summary and provenance details.

## `content_chunks`
Purpose: Stores chunked text for downstream lesson generation and retrieval.

```sql
CREATE TABLE content_chunks (
  id TEXT PRIMARY KEY,
  source_id TEXT NOT NULL,
  chunk_index INTEGER NOT NULL,
  text TEXT NOT NULL,
  metadata TEXT,
  created_at TEXT NOT NULL,
  FOREIGN KEY (source_id) REFERENCES lesson_sources(id)
);

CREATE INDEX idx_content_chunks_source_id
  ON content_chunks(source_id);

CREATE UNIQUE INDEX idx_content_chunks_source_index
  ON content_chunks(source_id, chunk_index);
```

Field notes:
- `id`: stable chunk ID (UUID).
- `chunk_index`: deterministic order within source.
- `metadata`: JSON map with page/slide and character offsets.
