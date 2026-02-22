from __future__ import annotations

from app.main import create_app


def _sample_lesson() -> dict:
    return {
        "id": "lesson-1",
        "modules": [
            {
                "id": "m-1",
                "title": "Variables and Data Types",
                "core_topics": ["variables", "types", "casting"],
            },
            {
                "id": "m-2",
                "title": "Control Flow",
                "core_topics": ["conditionals", "loops"],
            },
        ],
    }


def test_checkpoint_generates_2_to_3_guided_questions() -> None:
    app = create_app()
    client = app.test_client()

    response = client.post(
        "/api/checkpoint",
        json={"lesson": _sample_lesson(), "module_id": "m-1"},
    )
    assert response.status_code == 200
    body = response.get_json()
    assert 2 <= len(body["questions"]) <= 3
    assert len(body["questions"]) == 3
    for question in body["questions"]:
        assert "answer" not in question["text"].lower()


def test_checkpoint_records_qa_pairs_and_completion() -> None:
    app = create_app()
    client = app.test_client()

    start = client.post(
        "/api/checkpoint",
        json={"lesson": _sample_lesson(), "module_id": "m-2"},
    ).get_json()
    answers = [{"question_id": q["id"], "answer": "My reasoning"} for q in start["questions"]]

    submit = client.post(
        "/api/checkpoint",
        json={
            "lesson": _sample_lesson(),
            "module_id": "m-2",
            "session_id": start["session_id"],
            "answers": answers,
        },
    )
    assert submit.status_code == 200
    body = submit.get_json()
    assert body["completed"] is True
    assert len(body["qa_pairs"]) == len(start["questions"])


def test_test_start_covers_all_modules_and_topics() -> None:
    app = create_app()
    client = app.test_client()
    lesson = _sample_lesson()

    response = client.post("/api/test/start", json={"lesson": lesson})
    assert response.status_code == 200
    body = response.get_json()

    expected_modules = sorted(module["id"] for module in lesson["modules"])
    expected_topics = sorted(
        topic
        for module in lesson["modules"]
        for topic in module["core_topics"]
    )
    assert body["coverage"]["module_ids"] == expected_modules
    assert body["coverage"]["topics"] == expected_topics


def test_submit_requires_full_completion_before_feedback() -> None:
    app = create_app()
    client = app.test_client()

    test_start = client.post("/api/test/start", json={"lesson": _sample_lesson()}).get_json()
    first_question = test_start["questions"][0]
    partial_answers = [{"question_id": first_question["id"], "choice_index": 0}]

    response = client.post(
        "/api/test/submit",
        json={"test_id": test_start["test_id"], "answers": partial_answers},
    )
    assert response.status_code == 200
    body = response.get_json()
    assert body["completed"] is False
    assert "score" not in body
    assert "feedback" not in body


def test_submit_returns_score_and_feedback_after_full_submission() -> None:
    app = create_app()
    client = app.test_client()

    test_start = client.post("/api/test/start", json={"lesson": _sample_lesson()}).get_json()
    answers = [{"question_id": q["id"], "choice_index": 0} for q in test_start["questions"]]

    response = client.post(
        "/api/test/submit",
        json={"test_id": test_start["test_id"], "answers": answers},
    )
    assert response.status_code == 200
    body = response.get_json()
    assert body["completed"] is True
    assert "score" in body
    assert "feedback" in body
