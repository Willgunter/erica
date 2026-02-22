from __future__ import annotations

from app.main import create_app


def _lesson_payload() -> dict:
    return {
        "id": "lesson-analytics-1",
        "title": "Linear Modeling",
        "estimated_duration": 30,
        "modules": [
            {"id": "m-1", "title": "Slope", "core_topics": ["Slope"]},
            {"id": "m-2", "title": "Intercepts", "core_topics": ["Intercepts"]},
            {"id": "m-3", "title": "Applications", "core_topics": ["Applications"]},
        ],
        "media_assets": [
            {"type": "video", "label": "Slope Visual", "url": "https://example.com/slope-video"},
            {
                "type": "audio",
                "label": "Applications Recap",
                "url": "https://example.com/applications-audio",
            },
        ],
    }


def _test_result_payload() -> dict:
    return {
        "completed": True,
        "feedback": {
            "strong_topics": ["Slope", "Intercepts", "Slope"],
            "focus_topics": ["Applications", "Applications"],
        },
    }


def test_create_summary_returns_topics_accuracy_and_recommendations() -> None:
    app = create_app()
    client = app.test_client()

    response = client.post(
        "/api/summary",
        json={
            "user_id": "agent05-user",
            "lesson": _lesson_payload(),
            "test_result": _test_result_payload(),
            "checkpoint_sessions": [
                {
                    "module_id": "m-1",
                    "qa_pairs": [{"question": "Explain slope", "answer": "Rate of change"}],
                }
            ],
        },
    )
    assert response.status_code == 201
    body = response.get_json()
    summary = body["summary"]

    assert summary["accuracy"] == 60.0
    assert summary["correct_count"] == 3
    assert summary["incorrect_count"] == 2
    assert len(summary["topics"]) >= 3
    assert "recommendations" in summary and len(summary["recommendations"]) >= 1
    assert "Applications" in summary["focus_areas"]


def test_summaries_are_visible_in_account_history() -> None:
    app = create_app()
    client = app.test_client()

    create = client.post(
        "/api/summary",
        json={
            "userId": "agent05-history-user",
            "lesson": _lesson_payload(),
            "testResult": _test_result_payload(),
            "checkpointSessions": [],
        },
    )
    assert create.status_code == 201

    list_response = client.get("/api/summaries?userId=agent05-history-user")
    assert list_response.status_code == 200
    payload = list_response.get_json()
    assert len(payload["summaries"]) >= 1
    first = payload["summaries"][0]
    assert first["lesson_title"] == "Linear Modeling"
    assert "topics_covered" in first


def test_summary_detail_supports_full_replay_payload() -> None:
    app = create_app()
    client = app.test_client()

    create = client.post(
        "/api/summary",
        json={
            "user_id": "agent05-replay-user",
            "lesson": _lesson_payload(),
            "test_result": _test_result_payload(),
            "checkpoint_sessions": [],
        },
    )
    summary = create.get_json()["summary"]
    summary_id = summary["id"]

    detail = client.get(f"/api/summary/{summary_id}?user_id=agent05-replay-user")
    assert detail.status_code == 200
    detail_payload = detail.get_json()["summary"]
    assert detail_payload["lesson_id"] == "lesson-analytics-1"
    assert len(detail_payload["replay"]["modules"]) == 3

    replay = client.get(f"/api/summary/{summary_id}/replay")
    assert replay.status_code == 200
    replay_payload = replay.get_json()["replay"]
    assert replay_payload["title"] == "Linear Modeling"
    assert len(replay_payload["media_assets"]) == 2


def test_create_summary_can_resolve_test_and_checkpoint_dependencies_by_id() -> None:
    app = create_app()
    client = app.test_client()
    lesson = _lesson_payload()

    checkpoint_start = client.post(
        "/api/checkpoint",
        json={"lesson": lesson, "module_id": "m-1"},
    ).get_json()
    checkpoint_submit = client.post(
        "/api/checkpoint",
        json={
            "lesson": lesson,
            "module_id": "m-1",
            "session_id": checkpoint_start["session_id"],
            "answers": [
                {"question_id": question["id"], "answer": "Reasoning"}
                for question in checkpoint_start["questions"]
            ],
        },
    )
    assert checkpoint_submit.status_code == 200

    test_start = client.post("/api/test/start", json={"lesson": lesson}).get_json()
    questions = test_start["questions"]
    test_submit = client.post(
        "/api/test/submit",
        json={
            "test_id": test_start["test_id"],
            "answers": [{"question_id": q["id"], "choice_index": 0} for q in questions],
        },
    )
    assert test_submit.status_code == 200

    summary_response = client.post(
        "/api/summary",
        json={
            "user_id": "agent05-dependency-user",
            "lesson": lesson,
            "test_id": test_start["test_id"],
            "checkpoint_session_ids": [checkpoint_start["session_id"]],
        },
    )
    assert summary_response.status_code == 201
    summary = summary_response.get_json()["summary"]
    assert summary["inputs"]["test_result"]["completed"] is True
    assert len(summary["inputs"]["checkpoint_sessions"]) == 1
