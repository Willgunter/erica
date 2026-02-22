# Agent 04 — Knowledge Checks, Testing & Feedback

**Agent description**
Builds the AI sparring partner and assessment experience. Ensures knowledge checks are guiding, not revealing, and that the final test provides feedback only at the end.

**Goals**
- Provide 2–3 guided questions per knowledge check.
- Generate a final test that covers the full lesson.
- Score and return feedback only after completion.

**Scope**
- Checkpoint question generation and dialogue flow.
- Final test creation, submission, and scoring.
- Response storage for analytics and summaries.

**Inputs**
- Lesson modules and checkpoint markers from Agent 03.
- User responses during checkpoints and test.

**Outputs**
- Checkpoint transcripts with Q&A pairs.
- Final test results and scores.

**Key interfaces**
- `POST /api/checkpoint` generate and record checkpoint questions.
- `POST /api/test/start` create test.
- `POST /api/test/submit` score and return feedback.

**Dependencies**
- LLM provider for sparring partner prompts.
- `lesson` objects from Agent 03.
- Results consumed by Agent 05 for summaries.

**Acceptance criteria**
- Each knowledge check asks exactly 2–3 questions.
- Sparring partner guidance avoids direct answers.
- Test feedback is returned only after full submission.
- Test covers all lesson modules and core topics.

**Deliverables**
- Checkpoint generation logic and prompt templates.
- Test generation and scoring service.
- Data schema for checkpoint and test responses.
