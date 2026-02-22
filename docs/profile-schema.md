# Profile schema contract

This schema is the normalized output expected by downstream personalization consumers.

## API

- `POST /api/profile`: creates or updates `profiles` and `learning_preferences` for the authenticated user.
- `GET /api/profile`: fetches normalized profile for the authenticated user.

## Normalized profile object

```json
{
  "user_id": "uuid",
  "subject": "string",
  "goals": ["string"],
  "study_time": "15_min | 30_min | 45_min | 60_min_plus",
  "pacing": "light | steady | accelerated",
  "accessibility": {
    "captions": "boolean",
    "highContrast": "boolean",
    "reduceMotion": "boolean",
    "dyslexiaFriendlyFont": "boolean",
    "screenReaderOptimized": "boolean"
  },
  "learning_preferences": {
    "teaching_style": "visual | socratic | project_based | mixed | null",
    "content_formats": ["text | video | interactive | audio | flashcards"],
    "review_preferences": ["spaced_repetition | practice_quiz | reflection | teach_back"],
    "uncertainty_flags": {
      "teaching_style": "boolean"
    }
  }
}
```

## Defaults and normalization

- `subject`: defaults to `General learning` when empty.
- `goals`: defaults to `["Build confidence"]` when empty.
- `study_time`: defaults to `30_min`.
- `pacing`: defaults to `steady`.
- `accessibility.*`: defaults to `false` for all flags.
- `teaching_style`: `null` when omitted or set to `not_sure`.
- `learning_preferences.uncertainty_flags.teaching_style`: `true` when teaching style is unknown.
- `content_formats`: defaults to `["text", "interactive"]` when empty.
- `review_preferences`: defaults to `["practice_quiz"]` when empty.

## Auth expectations

- Endpoints use Supabase user auth.
- `Authorization: Bearer <access_token>` is expected in production.
- For local development only, `x-dev-user-id` can be used to bypass token validation.
