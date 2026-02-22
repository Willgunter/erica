# Agent 03 — Personalized Learning Engine (Codecademy-Inspired)

**Agent description**
Owns the core lesson generation flow that turns user preferences and content into a structured, interactive learning path. Produces visual lessons using Manim and auditory lessons using the NotebookLM API, with checkpoints embedded.

**Goals**
- Generate personalized lesson modules from profile + chunks.
- Match teaching style and pacing to user preferences.
- Insert knowledge checks at natural breakpoints.

**Scope**
- Lesson planning and module generation.
- Manim pipeline for visual learners.
- NotebookLM-based audio generation for auditory learners.
- Orchestration of media assets and metadata.

**Inputs**
- `profile` object from Agent 01.
- `content_chunks` from Agent 02.

**Outputs**
- `lesson` object: `modules`, `media_assets`, `checkpoints`, `estimated_duration`.
- Rendered media files stored in object storage.

**Key interfaces**
- `POST /api/lesson/generate` start lesson generation.
- `GET /api/lesson/:id` fetch lesson plan and assets.

**Dependencies**
- Manim runtime on worker nodes.
- NotebookLM API access for audio generation.
- Object storage for media outputs.
- Worker queue for long-running renders.

**Acceptance criteria**
- Lesson modules follow a stepwise, Codecademy-like format.
- Visual learner path produces a Manim-rendered sequence per module.
- Auditory learner path produces a podcast-style audio segment per module.
- Knowledge check markers are present in every module.

**Deliverables**
- Lesson planner and generator services.
- Worker tasks for Manim and NotebookLM generation.
- Lesson JSON schema and asset manifest.
