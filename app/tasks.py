from __future__ import annotations

from .chunker import build_chunks
from .config import Config
from .db import Database
from .parsers import ParseError, parse_source
from .storage import build_storage


def process_ingestion(source_id: str) -> None:
    config = Config()
    db = Database(config)
    db.init()

    source = db.get_source(source_id)
    if source is None:
        return

    db.update_source_status(source_id, "processing", error_message=None)

    try:
        source_type = source["type"].lower()
        if source["input_mode"] == "text":
            text = source["source_metadata"].get("raw_text", "")
            payload = text.encode("utf-8")
        else:
            storage = build_storage(config)
            payload = storage.read_bytes(source["storage_url"])

        units = parse_source(payload, source_type)
        chunks = build_chunks(units)
        if not chunks:
            raise ParseError("Extraction succeeded but no chunks were produced")

        db.replace_chunks(source_id, chunks)

        pages = sorted({u["metadata"].get("page") for u in units if "page" in u["metadata"]})
        slides = sorted({u["metadata"].get("slide") for u in units if "slide" in u["metadata"]})

        db.update_source_status(
            source_id,
            "completed",
            error_message=None,
            source_metadata_patch={
                "unit_count": len(units),
                "chunk_count": len(chunks),
                "pages": pages,
                "slides": slides,
            },
        )
    except Exception as exc:  # noqa: BLE001 - show ingestion errors in API/UI status.
        db.update_source_status(source_id, "failed", error_message=str(exc))
        raise
