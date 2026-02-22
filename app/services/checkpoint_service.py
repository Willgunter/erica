from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from app.store import store
from app.templates.prompts import CHECKPOINT_SYSTEM_PROMPT


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _normalize_topics(module: dict) -> list[str]:
    topics = module.get("core_topics") or []
    normalized = [str(topic).strip() for topic in topics if str(topic).strip()]
    if normalized:
        return normalized

    title = str(module.get("title", "")).strip()
    if title:
        return [title]
    return ["this module"]


def _question_count_for_topics(topic_count: int) -> int:
    if topic_count >= 3:
        return 3
    return 2


def _build_guided_question(topic: str, index: int) -> str:
    templates = [
        "In your own words, how would you explain {topic}?",
        "What clue helps you decide when to apply {topic}?",
        "Where do you still feel uncertain about {topic}?",
    ]
    return templates[index].format(topic=topic)


def create_checkpoint_session(
    lesson: dict, module: dict, checkpoint_id: str | None = None
) -> dict:
    topics = _normalize_topics(module)
    question_count = _question_count_for_topics(len(topics))
    seed_topics = topics[:question_count]
    while len(seed_topics) < question_count:
        seed_topics.append(topics[-1])

    questions = [
        {"id": str(uuid4()), "text": _build_guided_question(topic, idx)}
        for idx, topic in enumerate(seed_topics)
    ]

    session = {
        "session_id": str(uuid4()),
        "lesson_id": str(lesson.get("id", "")),
        "module_id": str(module.get("id", "")),
        "checkpoint_id": checkpoint_id or f"{module.get('id', 'module')}-checkpoint",
        "prompt_template": CHECKPOINT_SYSTEM_PROMPT,
        "questions": questions,
        "qa_pairs": [],
        "completed": False,
        "created_at": _now_iso(),
        "updated_at": _now_iso(),
    }

    with store.lock:
        store.checkpoint_sessions[session["session_id"]] = session
    return session


def record_checkpoint_answers(session: dict, answers: list[dict]) -> dict:
    questions_by_id = {question["id"]: question for question in session["questions"]}
    existing_question_ids = {pair["question_id"] for pair in session["qa_pairs"]}

    for answer in answers:
        question_id = answer.get("question_id")
        learner_answer = str(answer.get("answer", "")).strip()
        if question_id not in questions_by_id:
            continue
        if not learner_answer:
            continue
        if question_id in existing_question_ids:
            continue
        session["qa_pairs"].append(
            {
                "question_id": question_id,
                "question": questions_by_id[question_id]["text"],
                "answer": learner_answer,
            }
        )
        existing_question_ids.add(question_id)

    session["completed"] = len(session["qa_pairs"]) >= len(session["questions"])
    session["updated_at"] = _now_iso()

    with store.lock:
        store.checkpoint_sessions[session["session_id"]] = session
    return session


def remaining_question_ids(session: dict) -> list[str]:
    answered = {pair["question_id"] for pair in session["qa_pairs"]}
    return [q["id"] for q in session["questions"] if q["id"] not in answered]
