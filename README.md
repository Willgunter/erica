# Erica Agent 02: Content Ingestion & Context Pipeline

Implementation of `agents/agent-02.md`:
- Upload UI for files and free-text topics.
- `POST /api/ingest` and `GET /api/ingest/:id` interfaces.
- Async parsing/chunking pipeline with Redis + RQ worker.
- `lesson_sources` + `content_chunks` schema and storage.
- Retry path via `POST /api/ingest/:id/retry`.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run API in sync mode (no Redis required):

```bash
export INGEST_SYNC=true
python -m flask --app run.py run --host 0.0.0.0 --port 8000
```

Run async mode with Redis + RQ:

```bash
export REDIS_URL=redis://localhost:6379/0
export INGEST_SYNC=false
python -m flask --app run.py run --host 0.0.0.0 --port 8000
python worker.py
```

Open UI:
- `http://localhost:8000/ingest`

## API

### `POST /api/ingest`
- Multipart file upload: `file=@lesson.pdf`
- JSON text ingestion: `{ "text": "outline/topic notes" }`

Returns `202` and source ID:

```json
{
  "id": "<source-id>",
  "status": "queued",
  "filename": "lesson.pdf",
  "type": "pdf"
}
```

### `GET /api/ingest/<id>`
Returns ingestion status and chunk summary:

```json
{
  "id": "<source-id>",
  "status": "completed",
  "chunk_count": 12,
  "metadata": {
    "pages": [1,2],
    "chunk_count": 12
  }
}
```

### `POST /api/ingest/<id>/retry`
Retries failed (or completed) ingestion.

## Storage providers

Set `STORAGE_PROVIDER`:
- `local` (default): writes files under `UPLOADS_DIR`.
- `spaces`: DigitalOcean Spaces (S3-compatible).
- `supabase`: Supabase Storage fallback.

Environment configuration is in `app/config.py`.
