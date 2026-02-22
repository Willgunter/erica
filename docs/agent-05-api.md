# Agent 05 API + Replay UI

Implementation target: `app/main.py`

## Endpoints

### `POST /api/summary`
Creates a stored lesson summary from lesson metadata + test/checkpoint outputs.

Accepted request fields:
- `user_id` or `userId` (required)
- `lesson` (required)
- `test_result` / `testResult`, or `test_id` / `testId`
- `checkpoint_sessions` / `checkpointSessions`, or `checkpoint_session_ids` / `checkpointSessionIds`

Response: `201`

```json
{
  "summary": {
    "id": "uuid",
    "user_id": "demo-user",
    "lesson_id": "lesson-analytics-1",
    "lesson_title": "Linear Modeling",
    "accuracy": 60.0,
    "correct_count": 3,
    "incorrect_count": 2,
    "topics": [
      {
        "name": "Applications",
        "correct": 0,
        "incorrect": 2,
        "attempts": 2,
        "accuracy": 0.0,
        "checkpoint_questions": 1
      }
    ],
    "focus_areas": ["Applications"],
    "recommendations": ["Prioritize targeted review for: Applications."],
    "replay": {
      "lesson_id": "lesson-analytics-1",
      "title": "Linear Modeling",
      "modules": [],
      "media_assets": []
    }
  }
}
```

### `GET /api/summaries?user_id=:userId`
Returns account history list for a user.

### `GET /api/summary/:id?user_id=:userId`
Returns full summary details.

### `GET /api/summary/:id/replay`
Returns replay payload only.

## UI Routes

- `GET /history`: account history + analytics dashboard.
- `GET /replay/:id`: full lesson replay view.

## In-memory Storage

`app/store.py` now tracks:
- `summaries`: summary detail records by ID.
- `user_summaries`: per-user history list.
