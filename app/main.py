from __future__ import annotations

import logging
import os
from typing import Any

from app.web import Flask, jsonify, render_template, request

from app.lesson_engine.media import MediaGenerator
from app.lesson_engine.planner import LessonPlanner
from app.lesson_engine.repository import InMemoryLessonRepository
from app.lesson_engine.service import LessonGenerationService
from app.lesson_engine.storage import LocalObjectStorage
from app.lesson_engine.worker_queue import InProcessWorkerQueue
from app.services.ai_sparring_service import AISparringPartner
from app.services.checkpoint_service import (
    create_checkpoint_session,
    record_checkpoint_answers,
    remaining_question_ids,
)
from app.services.summary_service import (
    build_summary_record,
    get_summary,
    list_summaries,
    store_summary,
)
from app.services.test_service import create_test_session, submit_test_answers
from app.store import store


def _create_service() -> LessonGenerationService:
    level = os.getenv("APP_LOG_LEVEL", "INFO").upper()
    logging.basicConfig(level=getattr(logging, level, logging.INFO))
    storage_root = os.environ.get("OBJECT_STORAGE_ROOT", "app/object_storage")
    storage = LocalObjectStorage(root_dir=storage_root)
    repository = InMemoryLessonRepository()
    planner = LessonPlanner()
    worker_queue = InProcessWorkerQueue(max_workers=4)
    media_generator = MediaGenerator(storage=storage)
    return LessonGenerationService(
        repository=repository,
        planner=planner,
        media_generator=media_generator,
        worker_queue=worker_queue,
    )


def create_app() -> Flask:
    app = Flask(__name__)
    service = _create_service()
    ai_sparring = AISparringPartner()

    @app.get("/health")
    def health() -> Any:
        return jsonify({"ok": True})

    @app.post("/api/parse")
    def parse_file() -> Any:
        from app.parsers import parse_source
        from app.chunker import build_chunks
        
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files["file"]
        if not file or not file.filename:
            return jsonify({"error": "Invalid file"}), 400
        
        filename = file.filename.lower()
        if filename.endswith(".pdf"):
            source_type = "pdf"
        elif filename.endswith(".pptx"):
            source_type = "pptx"
        elif filename.endswith(".docx"):
            source_type = "docx"
        elif filename.endswith((".txt", ".md")):
            source_type = "txt"
        else:
            return jsonify({"error": f"Unsupported file type: {filename}"}), 400
        
        try:
            data = file.read()
            units = parse_source(data, source_type)
            chunks = build_chunks(units)
            return jsonify({"chunks": chunks})
        except Exception as exc:
            return jsonify({"error": str(exc)}), 500

    @app.post("/api/lesson/generate")
    def generate_lesson() -> Any:
        payload = request.get_json(silent=True) or {}
        profile = payload.get("profile")
        chunks = payload.get("content_chunks")

        if profile is None:
            return jsonify({"error": "profile is required"}), 400
        if not isinstance(chunks, list):
            return jsonify({"error": "content_chunks must be an array"}), 400

        try:
            lesson = service.generate_lesson(profile_payload=profile, chunks_payload=chunks)
        except ValueError as exc:
            return jsonify({"error": str(exc)}), 400

        return (
            jsonify(
                {
                    "lesson_id": lesson["id"],
                    "status_url": f"/api/lesson/{lesson['id']}",
                    "lesson": lesson,
                }
            ),
            202,
        )

    @app.get("/api/lesson/<lesson_id>")
    def get_lesson(lesson_id: str) -> Any:
        lesson = service.get_lesson(lesson_id)
        if lesson is None:
            return jsonify({"error": "lesson not found"}), 404
        return jsonify(lesson), 200

    @app.post("/api/checkpoint")
    def checkpoint() -> Any:
        payload = request.get_json(silent=True) or {}
        lesson = payload.get("lesson")
        if not isinstance(lesson, dict):
            return jsonify({"error": "lesson is required"}), 400

        module_id = payload.get("module_id")
        if not module_id:
            return jsonify({"error": "module_id is required"}), 400

        if payload.get("session_id"):
            session_id = str(payload["session_id"])
            with store.lock:
                session = store.checkpoint_sessions.get(session_id)
            if session is None:
                return jsonify({"error": "checkpoint session not found"}), 404

            answers = payload.get("answers") or []
            if not isinstance(answers, list):
                return jsonify({"error": "answers must be an array"}), 400

            updated = record_checkpoint_answers(session=session, answers=answers)
            
            ai_response = None
            if answers and len(answers) > 0:
                last_answer = answers[-1]
                question_id = last_answer.get("question_id")
                student_answer = last_answer.get("answer", "")

                question_obj = next(
                    (q for q in session["questions"] if q["id"] == question_id),
                    None
                )

                if question_obj:
                    module_context = session.get("module_context") or {}
                    conv_history = [
                        {"role": "student", "content": pair["answer"]}
                        for pair in session.get("qa_pairs", [])[-4:]
                    ]
                    ai_response = ai_sparring.generate_guiding_response(
                        question=question_obj["text"],
                        student_answer=student_answer,
                        module_context=module_context,
                        conversation_history=conv_history,
                    )

            return jsonify(
                {
                    "session_id": updated["session_id"],
                    "module_id": updated["module_id"],
                    "completed": updated["completed"],
                    "qa_pairs": updated["qa_pairs"],
                    "remaining_question_ids": remaining_question_ids(updated),
                    "ai_feedback": ai_response,
                }
            )

        lesson_id = lesson.get("id", "")
        full_lesson = service.get_lesson(lesson_id) if lesson_id else None
        if full_lesson is None:
            full_lesson = lesson

        module = _find_module(lesson=full_lesson, module_id=str(module_id))
        if module is None:
            return jsonify({"error": f"module '{module_id}' not found in lesson '{lesson_id}'"}), 404

        session = create_checkpoint_session(lesson=full_lesson, module=module)
        return jsonify(
            {
                "session_id": session["session_id"],
                "module_id": session["module_id"],
                "checkpoint_id": session["checkpoint_id"],
                "questions": session["questions"],
                "completed": session["completed"],
            }
        )

    @app.post("/api/test/start")
    def start_test() -> Any:
        payload = request.get_json(silent=True) or {}
        lesson = payload.get("lesson")
        if not isinstance(lesson, dict):
            return jsonify({"error": "lesson is required"}), 400

        session = create_test_session(lesson=lesson)
        module_ids = sorted(str(module.get("id", "")) for module in lesson.get("modules", []))
        topics = sorted(
            str(topic)
            for module in lesson.get("modules", [])
            for topic in (module.get("core_topics") or [module.get("title", "module concept")])
        )
        return jsonify(
            {
                "test_id": session["test_id"],
                "questions": session["questions"],
                "coverage": {
                    "module_ids": module_ids,
                    "topics": topics,
                },
            }
        )

    @app.post("/api/test/submit")
    def submit_test() -> Any:
        payload = request.get_json(silent=True) or {}
        test_id = payload.get("test_id")
        if not test_id:
            return jsonify({"error": "test_id is required"}), 400

        with store.lock:
            session = store.test_sessions.get(str(test_id))
        if session is None:
            return jsonify({"error": "test not found"}), 404

        answers = payload.get("answers") or []
        if not isinstance(answers, list):
            return jsonify({"error": "answers must be an array"}), 400

        result = submit_test_answers(session=session, answers=answers)
        return jsonify(result)

    @app.post("/api/summary")
    def create_summary() -> Any:
        payload = request.get_json(silent=True) or {}
        user_id = str(payload.get("user_id") or payload.get("userId") or "").strip()
        if not user_id:
            return jsonify({"error": "user_id is required"}), 400

        lesson = payload.get("lesson")
        if not isinstance(lesson, dict):
            return jsonify({"error": "lesson is required"}), 400

        test_result = payload.get("test_result") or payload.get("testResult")
        test_id = payload.get("test_id") or payload.get("testId")
        if test_result is None and test_id:
            with store.lock:
                test_result = store.test_results.get(str(test_id))
        if not isinstance(test_result, dict):
            return jsonify({"error": "test_result is required (or provide test_id)"}), 400

        checkpoint_sessions = (
            payload.get("checkpoint_sessions") or payload.get("checkpointSessions") or []
        )
        checkpoint_session_ids = payload.get("checkpoint_session_ids") or payload.get(
            "checkpointSessionIds"
        ) or []
        if checkpoint_session_ids:
            collected: list[dict[str, Any]] = []
            with store.lock:
                for session_id in checkpoint_session_ids:
                    session = store.checkpoint_sessions.get(str(session_id))
                    if session is not None:
                        collected.append(session)
            checkpoint_sessions = collected
        if not isinstance(checkpoint_sessions, list):
            return jsonify({"error": "checkpoint_sessions must be an array"}), 400

        summary = build_summary_record(
            user_id=user_id,
            lesson=lesson,
            test_result=test_result,
            checkpoint_sessions=checkpoint_sessions,
        )
        saved = store_summary(summary)
        return jsonify({"summary": saved}), 201

    @app.get("/api/summaries")
    def get_summaries() -> Any:
        user_id = str(request.args.get("user_id") or request.args.get("userId") or "").strip()
        if not user_id:
            return jsonify({"error": "user_id is required"}), 400

        summaries = list_summaries(user_id)
        history = [
            {
                "id": summary["id"],
                "user_id": summary["user_id"],
                "lesson_id": summary["lesson_id"],
                "lesson_title": summary["lesson_title"],
                "created_at": summary["created_at"],
                "accuracy": summary["accuracy"],
                "correct_count": summary["correct_count"],
                "incorrect_count": summary["incorrect_count"],
                "focus_areas": summary["focus_areas"],
                "topics_covered": [topic["name"] for topic in summary["topics"]],
            }
            for summary in summaries
        ]
        return jsonify({"summaries": history})

    @app.get("/api/summary/<summary_id>")
    def get_summary_details(summary_id: str) -> Any:
        summary = get_summary(summary_id)
        if summary is None:
            return jsonify({"error": "summary not found"}), 404

        user_id = request.args.get("user_id") or request.args.get("userId")
        if user_id and str(user_id) != str(summary["user_id"]):
            return jsonify({"error": "summary not found"}), 404

        return jsonify({"summary": summary})

    @app.get("/api/summary/<summary_id>/replay")
    def get_summary_replay(summary_id: str) -> Any:
        summary = get_summary(summary_id)
        if summary is None:
            return jsonify({"error": "summary not found"}), 404
        return jsonify({"replay": summary["replay"]})

    @app.get("/history")
    def account_history_page() -> Any:
        return render_template("history.html")

    @app.get("/replay/<summary_id>")
    def replay_page(summary_id: str) -> Any:
        return render_template("replay.html", summary_id=summary_id)

    return app


def _find_module(lesson: dict[str, Any], module_id: str) -> dict[str, Any] | None:
    for module in lesson.get("modules", []):
        if str(module.get("id")) == module_id or str(module.get("module_id")) == module_id:
            return module
    return None


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
