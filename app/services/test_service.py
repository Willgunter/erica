from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from app.store import store
from app.templates.prompts import TEST_GENERATION_SYSTEM_PROMPT


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _rotate_choices(topic: str, correct_index: int) -> list[str]:
    correct = f"{topic}: core idea used in this lesson"
    distractors = [
        f"{topic}: unrelated implementation detail",
        f"{topic}: tool setup only",
        f"{topic}: historical trivia",
    ]
    choices = distractors[:]
    choices.insert(correct_index, correct)
    return choices


def _iter_module_topics(lesson: dict) -> list[tuple[dict, str]]:
    pairs: list[tuple[dict, str]] = []
    for module in lesson.get("modules", []):
        topics = module.get("core_topics") or []
        normalized = [str(topic).strip() for topic in topics if str(topic).strip()]
        if not normalized:
            title = str(module.get("title", "")).strip() or "module concept"
            normalized = [title]
        for topic in normalized:
            pairs.append((module, topic))
    return pairs


def create_test_session(lesson: dict) -> dict:
    module_topics = _iter_module_topics(lesson)
    questions: list[dict] = []
    answer_key: dict[str, int] = {}

    for idx, (module, topic) in enumerate(module_topics):
        question_id = str(uuid4())
        correct_index = idx % 4
        choices = _rotate_choices(topic, correct_index)
        questions.append(
            {
                "id": question_id,
                "module_id": str(module.get("id", "")),
                "module_title": str(module.get("title", "")),
                "topic": topic,
                "prompt": f"Which option best captures the core idea of {topic}?",
                "choices": choices,
            }
        )
        answer_key[question_id] = correct_index

    session = {
        "test_id": str(uuid4()),
        "lesson_id": str(lesson.get("id", "")),
        "prompt_template": TEST_GENERATION_SYSTEM_PROMPT,
        "questions": questions,
        "answer_key": answer_key,
        "created_at": _now_iso(),
        "updated_at": _now_iso(),
    }
    with store.lock:
        store.test_sessions[session["test_id"]] = session
    return session


def submit_test_answers(session: dict, answers: list[dict]) -> dict:
    answers_by_id = {
        str(item.get("question_id")): int(item.get("choice_index"))
        for item in answers
        if item.get("question_id") in session["answer_key"] and "choice_index" in item
    }

    expected_ids = list(session["answer_key"].keys())
    missing_ids = [question_id for question_id in expected_ids if question_id not in answers_by_id]

    if missing_ids:
        return {
            "test_id": session["test_id"],
            "completed": False,
            "missing_question_ids": missing_ids,
            "message": "Submission incomplete. Feedback is available only after full completion.",
        }

    correct = 0
    incorrect_topics: list[str] = []
    correct_topics: list[str] = []
    question_by_id = {question["id"]: question for question in session["questions"]}
    for question_id, expected_choice_index in session["answer_key"].items():
        topic = question_by_id[question_id]["topic"]
        if answers_by_id[question_id] == expected_choice_index:
            correct += 1
            correct_topics.append(topic)
        else:
            incorrect_topics.append(topic)

    total = len(session["questions"])
    score_pct = round((correct / total) * 100, 2) if total else 0.0
    result = {
        "test_id": session["test_id"],
        "completed": True,
        "score": {
            "correct": correct,
            "total": total,
            "percentage": score_pct,
        },
        "feedback": {
            "summary": f"You answered {correct} out of {total} correctly.",
            "strong_topics": correct_topics,
            "focus_topics": incorrect_topics,
        },
        "submitted_at": _now_iso(),
    }

    with store.lock:
        store.test_results[session["test_id"]] = result
        session["updated_at"] = _now_iso()
        store.test_sessions[session["test_id"]] = session
    return result
