from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    db_path: str = os.getenv("DB_PATH", "./erica.db")
    uploads_dir: str = os.getenv("UPLOADS_DIR", "./uploads")

    # Queue settings
    redis_url: str | None = os.getenv("REDIS_URL")
    ingest_sync: bool = os.getenv("INGEST_SYNC", "false").lower() == "true"

    # Storage selection: local | spaces | supabase
    storage_provider: str = os.getenv("STORAGE_PROVIDER", "local").lower()

    # Spaces (S3-compatible) settings
    spaces_key: str | None = os.getenv("SPACES_KEY")
    spaces_secret: str | None = os.getenv("SPACES_SECRET")
    spaces_region: str | None = os.getenv("SPACES_REGION", "nyc3")
    spaces_bucket: str | None = os.getenv("SPACES_BUCKET")
    spaces_endpoint: str | None = os.getenv("SPACES_ENDPOINT")

    # Supabase Storage settings
    supabase_url: str | None = os.getenv("SUPABASE_URL")
    supabase_service_key: str | None = os.getenv("SUPABASE_SERVICE_KEY")
    supabase_bucket: str | None = os.getenv("SUPABASE_BUCKET", "lesson-sources")


ALLOWED_FILE_TYPES = {"pdf", "ppt", "pptx", "docx", "txt"}
