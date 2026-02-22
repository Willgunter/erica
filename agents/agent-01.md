# Agent 01 — Onboarding & Profile Modeling

**Agent description**
Owns the onboarding experience and student profile schema that drives personalization. Focus is a fast, low-friction questionnaire that captures goals, preferences, and accessibility needs with “Not sure” options.

**Goals**
- Deliver a 3–5 screen onboarding flow that feels simple and fast.
- Normalize responses into a stable, queryable profile model.
- Provide a clean API surface for downstream personalization.

**Scope**
- Next.js onboarding UI and UX flow.
- Flask endpoints or Supabase RPC for profile create/update.
- Supabase tables and types for profile and learning preferences.

**Inputs**
- User responses: subject, goals, study time, content and review preferences, teaching style or “Not sure”, pacing, accessibility settings.

**Outputs**
- `profile` object with normalized fields ready for lesson generation.

**Key interfaces**
- `POST /api/profile` create/update profile.
- `GET /api/profile` fetch profile.

**Data model**
- `profiles` table: `user_id`, `subject`, `goals`, `study_time`, `pacing`, `accessibility`.
- `learning_preferences` table: `user_id`, `teaching_style`, `content_formats`, `review_preferences`, `uncertainty_flags`.

**Dependencies**
- Auth from Supabase.
- Downstream consumers: Agent 03 (learning engine), Agent 04 (tests), Agent 05 (summary).

**Acceptance criteria**
- New user can complete onboarding in under 2 minutes.
- “Not sure” is available for teaching style and does not block progress.
- Profile can be created and fetched in a single round-trip each.
- All profile fields are validated and defaulted where optional.

**Deliverables**
- UI flow with form state, validation, and submit.
- API handler(s) and database migrations.
- Example profile JSON and schema docs for other agents.
