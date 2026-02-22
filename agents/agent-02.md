# Agent 02 — Content Ingestion & Context Pipeline

**Agent description**
Builds the intake pipeline for lesson context, accepting files and free-text topics and converting them into structured chunks. Ensures uploads are reliable, searchable, and ready for personalization.

**Goals**
- Support common learning materials with clear ingestion status.
- Extract clean text and metadata for downstream generation.
- Provide stable IDs for sources and chunks.

**Scope**
- Upload UI and API endpoints.
- File parsing and text extraction.
- Chunking, metadata tagging, and storage.

**Inputs**
- Files: PDF, PPT/PPTX, DOCX, TXT.
- Free-text topic or outline.

**Outputs**
- `lesson_sources` records and `content_chunks` records.

**Key interfaces**
- `POST /api/ingest` upload and start ingestion.
- `GET /api/ingest/:id` status and summary.

**Data model**
- `lesson_sources` table: `id`, `user_id`, `filename`, `type`, `storage_url`, `status`.
- `content_chunks` table: `id`, `source_id`, `chunk_index`, `text`, `metadata`.

**Dependencies**
- Object storage: DigitalOcean Spaces preferred, Supabase Storage fallback.
- Worker queue: Redis + RQ or Celery for async parsing.
- Downstream consumers: Agent 03 (learning engine).

**Acceptance criteria**
- Ingestion supports at least PDF and PPTX end to end.
- Each source produces chunked text with page or slide metadata.
- UI shows upload progress and final ingestion status.
- Failed ingestions provide an error message and retry path.

**Deliverables**
- Upload UI and API endpoint(s).
- Parsing pipeline and queue worker.
- Schema docs for `lesson_sources` and `content_chunks`.
