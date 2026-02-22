# Agent 04 Implementation

This implementation provides the knowledge-check and final-test backend described in `agents/agent-04.md`.

## Endpoints

### `POST /api/checkpoint`
Creates (or resumes) a checkpoint session, returns exactly 2-3 guided questions, and records Q&A pairs.

Request:

```json
{
  "lesson": {
    "id": "lesson-1",
    "modules": [
      { "id": "m-1", "title": "Module 1", "core_topics": ["topic-a", "topic-b"] }
    ]
  },
  "module_id": "m-1",
  "checkpoint_id": "m-1-cp-1",
  "session_id": "optional-existing-session-id",
  "answers": [
    { "question_id": "uuid", "answer": "Learner response" }
  ]
}
```

### `POST /api/test/start`
Builds a full-lesson test that covers all modules and core topics.

Request:

```json
{
  "lesson": {
    "id": "lesson-1",
    "modules": [
      { "id": "m-1", "title": "Module 1", "core_topics": ["topic-a", "topic-b"] }
    ]
  }
}
```

### `POST /api/test/submit`
Scores only when all questions are answered. Partial submission returns no score and no feedback.

Request:

```json
{
  "test_id": "uuid",
  "answers": [
    { "question_id": "uuid", "choice_index": 1 }
  ]
}
```

## Prompt Templates

- `app/templates/prompts.py` includes:
  - checkpoint guidance prompt (no direct answers)
  - test generation prompt (feedback only after full completion)

## Storage

In-memory store (`app/store.py`) tracks:
- checkpoint sessions and Q&A transcripts
- test sessions and answer keys
- scored test results

## Validation and Acceptance Coverage

`tests/test_agent_04_api.py` verifies:
- checkpoint asks exactly 2-3 questions
- checkpoint transcripts are stored as Q&A pairs
- final test covers all module topics
- feedback appears only after full test submission
