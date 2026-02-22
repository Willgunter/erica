from __future__ import annotations

import io
from pathlib import Path

from .config import Config


class StorageError(RuntimeError):
    pass


class BaseStorage:
    def upload_bytes(self, data: bytes, filename: str, source_id: str) -> str:
        raise NotImplementedError

    def read_bytes(self, storage_url: str) -> bytes:
        raise NotImplementedError


class LocalStorage(BaseStorage):
    def __init__(self, root_dir: str):
        self.root = Path(root_dir)
        self.root.mkdir(parents=True, exist_ok=True)

    def upload_bytes(self, data: bytes, filename: str, source_id: str) -> str:
        safe_name = filename.replace("/", "_")
        target = self.root / f"{source_id}_{safe_name}"
        target.write_bytes(data)
        return f"local://{target.resolve()}"

    def read_bytes(self, storage_url: str) -> bytes:
        if not storage_url.startswith("local://"):
            raise StorageError(f"Invalid local storage URL: {storage_url}")
        path = Path(storage_url.replace("local://", "", 1))
        return path.read_bytes()


class SpacesStorage(BaseStorage):
    def __init__(self, config: Config):
        try:
            import boto3
        except ImportError as exc:
            raise StorageError("boto3 is required for SpacesStorage") from exc

        if not all([config.spaces_key, config.spaces_secret, config.spaces_bucket, config.spaces_endpoint]):
            raise StorageError("Missing Spaces configuration")

        self.bucket = config.spaces_bucket
        self.client = boto3.client(
            "s3",
            region_name=config.spaces_region,
            endpoint_url=config.spaces_endpoint,
            aws_access_key_id=config.spaces_key,
            aws_secret_access_key=config.spaces_secret,
        )

    def upload_bytes(self, data: bytes, filename: str, source_id: str) -> str:
        key = f"lesson-sources/{source_id}/{filename}"
        self.client.upload_fileobj(io.BytesIO(data), self.bucket, key)
        return f"s3://{self.bucket}/{key}"

    def read_bytes(self, storage_url: str) -> bytes:
        if not storage_url.startswith("s3://"):
            raise StorageError(f"Invalid Spaces URL: {storage_url}")
        without_scheme = storage_url.replace("s3://", "", 1)
        bucket, key = without_scheme.split("/", 1)
        if bucket != self.bucket:
            raise StorageError("Bucket mismatch for Spaces read")

        stream = io.BytesIO()
        self.client.download_fileobj(bucket, key, stream)
        return stream.getvalue()


class SupabaseStorage(BaseStorage):
    def __init__(self, config: Config):
        try:
            from supabase import create_client
        except ImportError as exc:
            raise StorageError("supabase is required for SupabaseStorage") from exc

        if not all([config.supabase_url, config.supabase_service_key, config.supabase_bucket]):
            raise StorageError("Missing Supabase storage configuration")

        self.bucket = config.supabase_bucket
        self.client = create_client(config.supabase_url, config.supabase_service_key)

    def upload_bytes(self, data: bytes, filename: str, source_id: str) -> str:
        path = f"lesson-sources/{source_id}/{filename}"
        self.client.storage.from_(self.bucket).upload(path, data, {"upsert": "true"})
        return f"supabase://{self.bucket}/{path}"

    def read_bytes(self, storage_url: str) -> bytes:
        if not storage_url.startswith("supabase://"):
            raise StorageError(f"Invalid Supabase URL: {storage_url}")
        without_scheme = storage_url.replace("supabase://", "", 1)
        bucket, path = without_scheme.split("/", 1)
        if bucket != self.bucket:
            raise StorageError("Bucket mismatch for Supabase read")
        return self.client.storage.from_(bucket).download(path)


def build_storage(config: Config) -> BaseStorage:
    provider = config.storage_provider
    if provider == "spaces":
        return SpacesStorage(config)
    if provider == "supabase":
        return SupabaseStorage(config)
    if provider != "local":
        raise StorageError(
            f"Unknown STORAGE_PROVIDER='{provider}'. Use local, spaces, or supabase."
        )

    return LocalStorage(config.uploads_dir)
