# Parse API Error Log

Date: February 22, 2026
Repo: `/Users/willgunter/Projects/erica`

## Reported Symptoms
- Upload screen text: "What are we learning from?"
- Browser console error: `POST http://localhost:3000/api/parse 404 (Not Found)`
- Follow-up API error:
  - `500 Failed to parse file`
  - `Could not reach a parse endpoint at http://localhost:8000 ...`
- Follow-up behavior:
  - `503` errors on uploads (including non-PDF files).

## Confirmed Context
- Next route exists at `app/api/parse/route.ts`.
- Flask parser endpoint exists at `app/main.py` -> `POST /api/parse`.
- Route probing currently checks:
  - `http://localhost:8000/api/parse`
  - `http://127.0.0.1:8000/api/parse`
  - `http://localhost:5000/api/parse`
  - `http://127.0.0.1:5000/api/parse`
  - and matching `/parse` variants.
- If all probes fail at network level, API now returns `503`.

## Changes Applied
1. Structured parse logging
- File: `app/api/parse/route.ts`
- Added JSONL logging to: `scratch/parse-api-errors.jsonl`
- Each entry includes:
  - `request_id`
  - request headers/context (`user_agent`, `origin`, `referer`, `x_forwarded_for`)
  - uploaded file metadata (`name`, `type`, `size`)
  - configured backend URL
  - all target endpoints tried
  - per-target attempt status, duration, backend error, network error
  - final response status + response body

2. Local fallback for text/markdown uploads
- File: `app/api/parse/route.ts`
- If uploaded file is `.txt`/`.md` (or `text/plain`/`text/markdown`), it is chunked locally in Next.js.
- This avoids backend dependency for those file types and prevents `503` when Flask is down.

3. Better client-side error context
- File: `app/upload/page.tsx`
- Upload errors now surface:
  - `details`
  - summarized `network_failures`
  - `hint`
  - `request_id` for direct log correlation.

## How To Correlate a Failure
1. Trigger an upload error in UI.
2. Copy `request_id=...` from the file error row.
3. Find matching entry:
   - `rg "request_id" scratch/parse-api-errors.jsonl`
   - `rg "<the-request-id>" scratch/parse-api-errors.jsonl`

## Remaining Likely Root Cause for 503
- Flask backend not running/reachable from Next process.
- Verify with:
  - `curl -i http://localhost:8000/health`
  - `curl -i -X POST -F "file=@Biology_Fundamentals_Notes.pdf" http://localhost:8000/api/parse`

## Request ID Diagnosis
- Request ID: `0ebff2af-5edb-43f3-8782-49f446e537c9`
- File: `Biology_Fundamentals_Notes.pdf` (`application/pdf`, 2808 bytes)
- Attempt outcomes:
  - `http://localhost:8000/api/parse` -> `404`
  - `http://localhost:8000/parse` -> `404`
  - `http://127.0.0.1:8000/api/parse` -> `404`
  - `http://127.0.0.1:8000/parse` -> `404`
  - `http://localhost:5000/*` and `http://127.0.0.1:5000/*` -> `ECONNREFUSED`
- Interpretation:
  - A service is responding on port `8000`, but it does not expose `/api/parse`.
  - The expected Erica backend route is missing on the active process bound to `8000`.
