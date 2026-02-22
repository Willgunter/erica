# Agent 05 — Analytics, Summaries & Account History

**Agent description**
Owns the post-lesson summary, analytics, and historical replay experience. Ensures learners can review performance, identify weak areas, and replay complete lessons.

**Goals**
- Produce a clear, actionable summary after each lesson.
- Persist summaries and display them in the user account.
- Enable replay of any completed lesson.

**Scope**
- Summary generation and storage.
- Analytics metrics and dashboard UI.
- Replay and history endpoints.

**Inputs**
- Test results and checkpoint data from Agent 04.
- Lesson metadata from Agent 03.

**Outputs**
- `summary` object with topics, accuracy, and recommendations.
- History list for the user.

**Key interfaces**
- `POST /api/summary` create summary.
- `GET /api/summaries` list summaries.
- `GET /api/summary/:id` fetch summary details.

**Dependencies**
- Results data from Agent 04.
- Lesson metadata from Agent 03.
- Supabase storage for history records.

**Acceptance criteria**
- Summary includes topics covered, correct/incorrect, and suggested focus areas.
- All summaries are visible in account history.
- User can replay a full lesson from summary view.

**Deliverables**
- Summary generator and schema.
- Account history UI.
- Replay hook to lesson assets.
