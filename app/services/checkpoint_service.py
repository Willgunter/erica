from __future__ import annotations

import re
from datetime import datetime, timezone
from difflib import SequenceMatcher
from typing import Any
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


def _normalize_text(value: Any) -> str:
    text = str(value or "").strip().lower()
    text = re.sub(r"[^a-z0-9\s']", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _extract_hint(question: dict) -> str:
    hints = question.get("hints") or []
    normalized_hints = [str(hint).strip() for hint in hints if str(hint).strip()]
    if normalized_hints:
        return normalized_hints[0]

    answer = _normalize_text(question.get("answer", ""))
    if not answer:
        return "Focus on the key ideas from the material and explain your reasoning."

    answer_parts = answer.split()
    clue_words = ", ".join(answer_parts[:6])
    return f"Try mentioning: {clue_words}"


def _is_answer_correct(question: dict, student_answer: str) -> tuple[bool, str]:
    expected = _normalize_text(question.get("answer", ""))
    if not expected:
        # No canonical answer available, so keep the flow open-ended for this checkpoint question.
        return True, ""

    normalized_student = _normalize_text(student_answer)
    if not normalized_student:
        return False, _extract_hint(question)

    if normalized_student in expected or expected in normalized_student:
        return True, ""

    expected_tokens = {token for token in expected.split() if len(token) > 2}
    student_tokens = {token for token in normalized_student.split() if len(token) > 2}
    if not expected_tokens:
        return False, _extract_hint(question)

    matched_tokens = expected_tokens.intersection(student_tokens)
    min_matches = max(1, int(len(expected_tokens) * 0.6))
    if len(matched_tokens) >= min_matches:
        return True, ""

    similarity = SequenceMatcher(None, expected, normalized_student).ratio()
    if similarity >= 0.72:
        return True, ""

    return False, _extract_hint(question)


def create_checkpoint_session(
    lesson: dict, module: dict, checkpoint_id: str | None = None
) -> dict:
    exam_questions = module.get("exam_questions") or []
    if exam_questions:
        questions = [
            {
                "id": str(uuid4()),
                "text": q["question"],
                "answer": q.get("answer", ""),
                "hints": q.get("hints", []),
            }
            for q in exam_questions[:3]
        ]
    else:
        topics = _normalize_topics(module)
        question_count = _question_count_for_topics(len(topics))
        seed_topics = topics[:question_count]
        while len(seed_topics) < question_count:
            seed_topics.append(topics[-1])
        questions = [
            {"id": str(uuid4()), "text": _build_guided_question(topic, idx), "answer": "", "hints": []}
            for idx, topic in enumerate(seed_topics)
        ]

    module_id = str(module.get("module_id") or module.get("id") or "module")

    session = {
        "session_id": str(uuid4()),
        "lesson_id": str(lesson.get("id", "")),
        "module_id": module_id,
        "checkpoint_id": checkpoint_id or f"{module_id}-checkpoint",
        "prompt_template": CHECKPOINT_SYSTEM_PROMPT,
        "module_context": {
            "title": module.get("title", ""),
            "objective": module.get("objective", ""),
            "concept_explanation": module.get("concept_explanation", ""),
            "key_insight": module.get("key_insight", ""),
        },
        "questions": questions,
        "qa_pairs": [],
        "completed": False,
        "created_at": _now_iso(),
        "updated_at": _now_iso(),
    }

    with store.lock:
        store.checkpoint_sessions[session["session_id"]] = session
    return session


def record_checkpoint_answers(session: dict, answers: list[dict]) -> tuple[dict, list[dict[str, Any]]]:
    questions_by_id = {question["id"]: question for question in session["questions"]}
    qa_pairs_by_id: dict[str, int] = {
        pair["question_id"]: index for index, pair in enumerate(session["qa_pairs"])
    }

    answer_results: list[dict[str, Any]] = []
    for answer in answers:
        question_id = answer.get("question_id")
        learner_answer = str(answer.get("answer", "")).strip()
        if question_id not in questions_by_id:
            continue
        if not learner_answer:
            continue

        existing_index = qa_pairs_by_id.get(question_id)
        question = questions_by_id[question_id]
        is_correct, hint = _is_answer_correct(question, learner_answer)
        if existing_index is not None:
            existing_pair = session["qa_pairs"][existing_index]
            if existing_pair.get("is_correct"):
                continue
            existing_pair.update(
                {
                    "question": question["text"],
                    "answer": learner_answer,
                    "is_correct": is_correct,
                    "hint": hint,
                    "attempts": existing_pair.get("attempts", 0) + 1,
                    "attempted_at": _now_iso(),
                }
            )
        else:
            qa_pairs_by_id[question_id] = len(session["qa_pairs"])
            session["qa_pairs"].append(
                {
                    "question_id": question_id,
                    "question": question["text"],
                    "answer": learner_answer,
                    "is_correct": is_correct,
                    "hint": hint,
                    "attempts": 1,
                    "attempted_at": _now_iso(),
                }
            )

        answer_results.append(
            {
                "question_id": question_id,
                "is_correct": is_correct,
                "hint": hint,
                "answer": learner_answer,
                "direct_answer": str(question.get("answer", "")).strip(),
            }
        )

    completed = all(
        any(
            pair.get("question_id") == question["id"] and pair.get("is_correct")
            for pair in session["qa_pairs"]
        )
        for question in session["questions"]
    )
    session["completed"] = completed
    session["updated_at"] = _now_iso()

    with store.lock:
        store.checkpoint_sessions[session["session_id"]] = session
    return session, answer_results


def remaining_question_ids(session: dict) -> list[str]:
    answered = {
        pair["question_id"]
        for pair in session["qa_pairs"]
        if pair.get("is_correct")
    }
    return [q["id"] for q in session["questions"] if q["id"] not in answered]
