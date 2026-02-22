from __future__ import annotations

import os
import uuid

from app.web import Flask, jsonify, redirect, render_template, request

from .config import ALLOWED_FILE_TYPES, Config
from .db import Database
from .queueing import QueueManager
from .storage import StorageError, build_storage


def _extension(filename: str) -> str:
    return filename.rsplit(".", 1)[-1].lower() if "." in filename else ""


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates")
    config = Config()
    db = Database(config)
    db.init()
    queue = QueueManager(config)

    @app.get("/")
    def index():
        return redirect("/ingest")

    @app.get("/healthz")
    def healthz():
        return jsonify({"ok": True})

    @app.get("/ingest")
    def ingest_ui():
        return render_template("ingest.html")

    @app.post("/api/ingest")
    def ingest():
        user_id = request.headers.get("x-user-id")

        if "file" in request.files:
            file = request.files["file"]
            if not file.filename:
                return jsonify({"error": "Missing filename"}), 400

            source_type = _extension(file.filename)
            if source_type not in ALLOWED_FILE_TYPES:
                return (
                    jsonify(
                        {
                            "error": f"Unsupported file type '{source_type}'. Allowed: {sorted(ALLOWED_FILE_TYPES)}"
                        }
                    ),
                    400,
                )

            source_id = str(uuid.uuid4())
            payload = file.read()
            try:
                storage = build_storage(config)
                storage_url = storage.upload_bytes(payload, file.filename, source_id)
            except StorageError as exc:
                return jsonify({"error": f"Storage configuration error: {exc}"}), 500

            db.create_source(
                source_id=source_id,
                user_id=user_id,
                filename=file.filename,
                source_type=source_type,
                storage_url=storage_url,
                input_mode="file",
                source_metadata={"filesize": len(payload)},
            )

            queue_info = queue.enqueue_ingestion(source_id)
            return (
                jsonify(
                    {
                        "id": source_id,
                        "status": "queued",
                        "filename": file.filename,
                        "type": source_type,
                        "queue": queue_info,
                    }
                ),
                202,
            )

        payload = request.get_json(silent=True) or {}
        topic_text = payload.get("text") or payload.get("topic")
        if not topic_text:
            return (
                jsonify(
                    {
                        "error": "Provide either a multipart file ('file') or JSON field 'text'/'topic'."
                    }
                ),
                400,
            )

        source_id = str(uuid.uuid4())
        db.create_source(
            source_id=source_id,
            user_id=user_id,
            filename=payload.get("title", "topic.txt"),
            source_type="topic",
            storage_url=None,
            input_mode="text",
            source_metadata={"raw_text": topic_text, "length": len(topic_text)},
        )
        queue_info = queue.enqueue_ingestion(source_id)
        return (
            jsonify(
                {
                    "id": source_id,
                    "status": "queued",
                    "filename": payload.get("title", "topic.txt"),
                    "type": "topic",
                    "queue": queue_info,
                }
            ),
            202,
        )

    @app.get("/api/ingest/<source_id>")
    def ingest_status(source_id: str):
        source = db.get_source(source_id)
        if source is None:
            return jsonify({"error": "Source not found"}), 404

        stats = db.chunk_stats(source_id)
        response = {
            "id": source["id"],
            "user_id": source["user_id"],
            "filename": source["filename"],
            "type": source["type"],
            "status": source["status"],
            "storage_url": source["storage_url"],
            "error_message": source["error_message"],
            "created_at": source["created_at"],
            "updated_at": source["updated_at"],
            "metadata": source["source_metadata"],
            **stats,
        }
        if source["status"] == "failed":
            response["retry_url"] = f"/api/ingest/{source_id}/retry"
        return jsonify(response)

    @app.post("/api/ingest/<source_id>/retry")
    def retry_ingest(source_id: str):
        source = db.get_source(source_id)
        if source is None:
            return jsonify({"error": "Source not found"}), 404

        if source["status"] not in {"failed", "completed"}:
            return (
                jsonify({"error": f"Cannot retry source in status '{source['status']}'"}),
                409,
            )

        db.update_source_status(source_id, "queued", error_message=None)
        queue_info = queue.enqueue_ingestion(source_id)
        return jsonify(
            {"id": source_id, "status": "queued", "message": "Retry started", "queue": queue_info}
        )

    return app


if __name__ == "__main__":
    app = create_app()
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(host=host, port=port, debug=debug)
