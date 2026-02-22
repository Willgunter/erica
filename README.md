# Erica Agent 02: Content Ingestion & Context Pipeline

This repository contains two parts:

- Backend API + ingestion UI: Flask app at `http://localhost:8000`.
- Frontend app: Next.js app using the `/onboarding` route and shared components.

> The ingestion UI at `/ingest` is rendered by Flask. The Next.js onboarding flow is at `/onboarding` when running `npm run dev`.

## Prerequisites

- Python 3.11+
- Node.js 18+ (Node 20 recommended)
- `npm` or `pnpm`

Optional for async mode:

- Redis server (local or remote)

Optional file parsers/storage providers:

- `pypdf` for PDFs
- `python-pptx` for PPTX
- `python-docx` for DOCX
- `redis` + `rq` for queue worker mode
- `boto3` for Spaces storage
- `supabase` for Supabase storage support

## Quick backend setup

From repo root:

```bash
cd /Users/willgunter/Projects/erica
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Then create your backend env file (optional helper):

```bash
cp .env.example .env.local
```

Run backend in sync mode (no Redis required):

```bash
export INGEST_SYNC=true
export DB_PATH=./erica.db
python -m flask --app run.py run --host 0.0.0.0 --port 8000
```

Run async mode with Redis + RQ:

```bash
export REDIS_URL=redis://localhost:6379/0
export INGEST_SYNC=false
python -m flask --app run.py run --host 0.0.0.0 --port 8000
python worker.py
```

Open ingestion UI:

- `http://localhost:8000/ingest`

## Frontend setup (Next.js)

Install JS dependencies at repo root:

```bash
cd /Users/willgunter/Projects/erica
npm install
```

Run dev server:

```bash
npm run dev
```

Open frontend:

- `http://localhost:3000/onboarding`

Environment variables for frontend:

- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- `SUPABASE_SERVICE_ROLE_KEY` (required for local dev fallback path in `/api/profile`)

Copy from example:

```bash
cp .env.example .env.local
```

Fill values in `.env.local` before running Next:

```bash
NEXT_PUBLIC_SUPABASE_URL=...
NEXT_PUBLIC_SUPABASE_ANON_KEY=...
SUPABASE_SERVICE_ROLE_KEY=...
```

## API endpoints

- `GET /` redirects to `http://localhost:8000/ingest`
- `POST /api/ingest` handles multipart `file` uploads and JSON `{ "text": "..." }`
- `GET /api/ingest/<id>` returns ingestion status
- `POST /api/ingest/<id>/retry` retries failed/completed ingestions

## Storage providers (backend config)

Set `STORAGE_PROVIDER` in env (default: `local`):

- `local` (default): write files under `UPLOADS_DIR` (default `./uploads`)
- `spaces`: DigitalOcean Spaces/S3-compatible
- `supabase`: Supabase Storage

## Required/optional backend env vars

- `DB_PATH` (default `./erica.db`)
- `UPLOADS_DIR` (default `./uploads`)
- `INGEST_SYNC` (`true` or `false`)
- `REDIS_URL` (when async mode is enabled)
- `STORAGE_PROVIDER` (`local`, `spaces`, `supabase`)
- `SPACES_KEY`, `SPACES_SECRET`, `SPACES_REGION`, `SPACES_BUCKET`, `SPACES_ENDPOINT` (Spaces)
- `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, `SUPABASE_BUCKET` (backend Supabase storage path)

## ENOTEMPTY npm install recovery

If npm install fails with:

```
ENOTEMPTY: rename .../node_modules/undici-types -> .../.undici-types-*
```

Run:

```bash
cd /Users/willgunter/Projects/erica
rm -rf node_modules/undici-types node_modules/.undici-types-*
npm cache clean --force
npm install
```

## Notes on parser dependencies

If you upload file formats and see parser errors, install the corresponding package(s):

- PDF: `pip install pypdf`
- PPTX: `pip install python-pptx`
- DOCX: `pip install python-docx`
- Async queue: `pip install redis rq`

## Quick validation checklist

1. Start backend: `python -m flask --app run.py run --host 0.0.0.0 --port 8000`
2. Start frontend: `npm run dev`
3. Visit `http://localhost:8000/ingest` and upload a file/text.
4. Visit `http://localhost:3000/onboarding`.
