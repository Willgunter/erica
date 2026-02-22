from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


def now_iso() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


@dataclass
class Profile:
    user_id: str
    subject: str
    goals: list[str]
    study_time_minutes: int
    pacing: str
    teaching_style: str
    content_formats: list[str]
    review_preferences: list[str]
    accessibility: dict[str, Any]
    uncertainty_flags: list[str]

    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> "Profile":
        if not isinstance(payload, dict):
            raise ValueError("profile must be an object")

        user_id = str(payload.get("user_id") or "anonymous")
        subject = str(payload.get("subject") or "General Studies")

        goals_raw = payload.get("goals") or []
        goals = [str(goal).strip() for goal in goals_raw if str(goal).strip()]
        if not goals:
            goals = [f"Build practical understanding of {subject}"]

        study_time = payload.get("study_time_minutes", payload.get("study_time", 30))
        try:
            study_time_minutes = int(study_time)
        except (TypeError, ValueError) as exc:
            raise ValueError("study_time_minutes must be numeric") from exc
        study_time_minutes = max(10, min(study_time_minutes, 180))

        pacing = str(payload.get("pacing") or "medium").lower()
        if pacing not in {"slow", "medium", "fast"}:
            pacing = "medium"

        teaching_style = str(payload.get("teaching_style") or "not_sure").lower()

        content_formats_raw = payload.get("content_formats") or ["text"]
        content_formats = [str(item).lower() for item in content_formats_raw]
        normalized_formats: list[str] = []
        for fmt in content_formats:
            if fmt in {"visual", "video"} and "visual" not in normalized_formats:
                normalized_formats.append("visual")
            elif fmt in {"auditory", "audio", "podcast"} and "auditory" not in normalized_formats:
                normalized_formats.append("auditory")
            elif fmt in {"text", "interactive"} and "text" not in normalized_formats:
                normalized_formats.append("text")
        if not normalized_formats:
            normalized_formats = ["text"]

        review_raw = payload.get("review_preferences") or []
        review_preferences = [str(item).strip() for item in review_raw if str(item).strip()]

        accessibility = payload.get("accessibility") or {}
        if not isinstance(accessibility, dict):
            accessibility = {}

        uncertainty_raw = payload.get("uncertainty_flags") or []
        uncertainty_flags = [str(item) for item in uncertainty_raw]

        return cls(
            user_id=user_id,
            subject=subject,
            goals=goals,
            study_time_minutes=study_time_minutes,
            pacing=pacing,
            teaching_style=teaching_style,
            content_formats=normalized_formats,
            review_preferences=review_preferences,
            accessibility=accessibility,
            uncertainty_flags=uncertainty_flags,
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "user_id": self.user_id,
            "subject": self.subject,
            "goals": self.goals,
            "study_time_minutes": self.study_time_minutes,
            "pacing": self.pacing,
            "teaching_style": self.teaching_style,
            "content_formats": self.content_formats,
            "review_preferences": self.review_preferences,
            "accessibility": self.accessibility,
            "uncertainty_flags": self.uncertainty_flags,
        }


@dataclass
class ContentChunk:
    id: str
    source_id: str
    chunk_index: int
    text: str
    metadata: dict[str, Any]

    @classmethod
    def from_payload(cls, payload: dict[str, Any], idx: int) -> "ContentChunk":
        if not isinstance(payload, dict):
            raise ValueError("content_chunks items must be objects")

        chunk_id = str(payload.get("id") or f"chunk-{idx}")
        source_id = str(payload.get("source_id") or "unknown-source")
        chunk_index = int(payload.get("chunk_index", idx))
        text = str(payload.get("text") or "").strip()
        if not text:
            raise ValueError(f"content chunk {chunk_id} has empty text")
        metadata = payload.get("metadata") or {}
        if not isinstance(metadata, dict):
            metadata = {}
        return cls(
            id=chunk_id,
            source_id=source_id,
            chunk_index=chunk_index,
            text=text,
            metadata=metadata,
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "source_id": self.source_id,
            "chunk_index": self.chunk_index,
            "text": self.text,
            "metadata": self.metadata,
        }


@dataclass
class Lesson:
    id: str
    user_id: str
    status: str
    modules: list[dict[str, Any]]
    media_assets: list[dict[str, Any]]
    checkpoints: list[dict[str, Any]]
    estimated_duration: int
    profile: dict[str, Any]
    created_at: str = field(default_factory=now_iso)
    updated_at: str = field(default_factory=now_iso)

    @classmethod
    def new(
        cls,
        profile: Profile,
        modules: list[dict[str, Any]],
        checkpoints: list[dict[str, Any]],
        estimated_duration: int,
    ) -> "Lesson":
        lesson_id = f"lesson-{uuid4().hex[:12]}"
        return cls(
            id=lesson_id,
            user_id=profile.user_id,
            status="generating",
            modules=modules,
            media_assets=[],
            checkpoints=checkpoints,
            estimated_duration=estimated_duration,
            profile=profile.as_dict(),
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "status": self.status,
            "modules": self.modules,
            "media_assets": self.media_assets,
            "checkpoints": self.checkpoints,
            "estimated_duration": self.estimated_duration,
            "profile": self.profile,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
