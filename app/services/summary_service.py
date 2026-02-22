from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from app.store import store


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _normalize_topic(topic: Any) -> str:
    if topic is None:
        return "General"
    value = str(topic).strip()
    return value or "General"


def _module_topics(lesson: dict[str, Any]) -> list[str]:
    topics: list[str] = []
    for module in lesson.get("modules", []):
        module_topics = module.get("core_topics") or []
        normalized = [_normalize_topic(topic) for topic in module_topics if str(topic).strip()]
        if normalized:
            topics.extend(normalized)
        else:
            topics.append(_normalize_topic(module.get("title")))
    return topics


def _collect_test_topic_outcomes(test_result: dict[str, Any]) -> tuple[list[str], list[str]]:
    feedback = test_result.get("feedback") or {}
    strong_topics = [_normalize_topic(topic) for topic in feedback.get("strong_topics", [])]
    focus_topics = [_normalize_topic(topic) for topic in feedback.get("focus_topics", [])]
    return strong_topics, focus_topics


def _collect_checkpoint_topic_counts(checkpoint_sessions: list[dict[str, Any]]) -> dict[str, int]:
    topic_counts: dict[str, int] = defaultdict(int)
    for session in checkpoint_sessions:
        module_title = _normalize_topic(session.get("module_id") or session.get("checkpoint_id"))
        for qa_pair in session.get("qa_pairs", []):
            question = str(qa_pair.get("question", "")).strip()
            if question:
                topic_counts[module_title] += 1
    return topic_counts


def _build_topic_metrics(
    lesson_topics: list[str],
    strong_topics: list[str],
    focus_topics: list[str],
    checkpoint_counts: dict[str, int],
) -> list[dict[str, Any]]:
    metrics: dict[str, dict[str, Any]] = {}

    def ensure(topic: str) -> dict[str, Any]:
        if topic not in metrics:
            metrics[topic] = {"name": topic, "correct": 0, "incorrect": 0, "checkpoint_questions": 0}
        return metrics[topic]

    for topic in lesson_topics:
        ensure(topic)

    for topic in strong_topics:
        ensure(topic)["correct"] += 1

    for topic in focus_topics:
        ensure(topic)["incorrect"] += 1

    for topic, count in checkpoint_counts.items():
        ensure(topic)["checkpoint_questions"] += count

    rows: list[dict[str, Any]] = []
    for topic, values in metrics.items():
        attempts = values["correct"] + values["incorrect"]
        accuracy = round((values["correct"] / attempts) * 100, 2) if attempts else 0.0
        rows.append(
            {
                "name": topic,
                "correct": values["correct"],
                "incorrect": values["incorrect"],
                "attempts": attempts,
                "accuracy": accuracy,
                "checkpoint_questions": values["checkpoint_questions"],
            }
        )

    rows.sort(key=lambda item: (item["accuracy"], item["name"]))
    return rows


def _build_recommendations(focus_areas: list[str], accuracy: float) -> list[str]:
    recommendations: list[str] = []
    if focus_areas:
        focus_text = ", ".join(focus_areas[:3])
        recommendations.append(f"Prioritize targeted review for: {focus_text}.")
        recommendations.append(
            "Replay low-accuracy modules and pause after each checkpoint to summarize concepts aloud."
        )

    if accuracy < 60:
        recommendations.append(
            "Before a retest, run one guided practice cycle per focus topic with worked examples."
        )
    elif accuracy < 85:
        recommendations.append(
            "Schedule a mixed-topic checkpoint within 24 hours to reinforce weak concepts."
        )
    else:
        recommendations.append("Maintain momentum with spaced review later this week.")

    return recommendations


def build_summary_record(
    *,
    user_id: str,
    lesson: dict[str, Any],
    test_result: dict[str, Any],
    checkpoint_sessions: list[dict[str, Any]],
) -> dict[str, Any]:
    lesson_id = str(lesson.get("id") or uuid4())
    lesson_title = str(lesson.get("title") or lesson_id)

    lesson_topics = _module_topics(lesson)
    strong_topics, focus_topics = _collect_test_topic_outcomes(test_result)
    checkpoint_counts = _collect_checkpoint_topic_counts(checkpoint_sessions)

    topics = _build_topic_metrics(
        lesson_topics=lesson_topics,
        strong_topics=strong_topics,
        focus_topics=focus_topics,
        checkpoint_counts=checkpoint_counts,
    )

    correct_count = sum(topic["correct"] for topic in topics)
    incorrect_count = sum(topic["incorrect"] for topic in topics)
    total = correct_count + incorrect_count
    accuracy = round((correct_count / total) * 100, 2) if total else 0.0

    focus_areas = [topic["name"] for topic in topics if topic["incorrect"] > topic["correct"]]
    recommendations = _build_recommendations(focus_areas, accuracy)

    return {
        "id": str(uuid4()),
        "user_id": user_id,
        "lesson_id": lesson_id,
        "lesson_title": lesson_title,
        "created_at": _now_iso(),
        "accuracy": accuracy,
        "correct_count": correct_count,
        "incorrect_count": incorrect_count,
        "topics": topics,
        "focus_areas": focus_areas,
        "recommendations": recommendations,
        "replay": {
            "lesson_id": lesson_id,
            "title": lesson_title,
            "estimated_duration": lesson.get("estimated_duration"),
            "modules": lesson.get("modules", []),
            "media_assets": lesson.get("media_assets")
            or lesson.get("mediaAssets")
            or [],
        },
        "inputs": {
            "test_result": test_result,
            "checkpoint_sessions": checkpoint_sessions,
        },
    }


def store_summary(summary: dict[str, Any]) -> dict[str, Any]:
    with store.lock:
        store.summaries[summary["id"]] = summary
        store.user_summaries.setdefault(summary["user_id"], []).append(summary["id"])
    return summary


def get_summary(summary_id: str) -> dict[str, Any] | None:
    with store.lock:
        return store.summaries.get(summary_id)


def list_summaries(user_id: str) -> list[dict[str, Any]]:
    with store.lock:
        summary_ids = list(store.user_summaries.get(user_id, []))
        summaries = [store.summaries[summary_id] for summary_id in summary_ids if summary_id in store.summaries]
    return sorted(summaries, key=lambda item: item["created_at"], reverse=True)
