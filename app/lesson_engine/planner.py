from __future__ import annotations

import math
import re
from typing import Any

from .models import ContentChunk, Profile


class LessonPlanner:
    """Builds stepwise modules and checkpoints from profile + content chunks."""

    _SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")

    def plan(
        self,
        profile: Profile,
        chunks: list[ContentChunk],
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]], int]:
        grouped_chunks = self._group_chunks(profile=profile, chunks=chunks)
        modules: list[dict[str, Any]] = []
        checkpoints: list[dict[str, Any]] = []

        for index, group in enumerate(grouped_chunks, start=1):
            module = self._build_module(index=index, group=group, profile=profile)
            modules.append(module)
            checkpoints.append(module["checkpoint"])

        estimated_duration = sum(module["estimated_minutes"] for module in modules)
        return modules, checkpoints, estimated_duration

    def _group_chunks(self, profile: Profile, chunks: list[ContentChunk]) -> list[list[ContentChunk]]:
        if not chunks:
            fallback = ContentChunk(
                id="chunk-0",
                source_id="generated",
                chunk_index=0,
                text=f"Foundational overview for {profile.subject}.",
                metadata={"generated": True},
            )
            return [[fallback]]

        base_count = max(1, min(8, math.ceil(len(chunks) / 2)))
        if profile.pacing == "slow":
            target_modules = min(base_count + 1, len(chunks))
        elif profile.pacing == "fast":
            target_modules = max(1, base_count - 1)
        else:
            target_modules = base_count

        per_module = math.ceil(len(chunks) / target_modules)
        grouped: list[list[ContentChunk]] = []
        for start in range(0, len(chunks), per_module):
            grouped.append(chunks[start : start + per_module])
        return grouped

    def _build_module(
        self,
        index: int,
        group: list[ContentChunk],
        profile: Profile,
    ) -> dict[str, Any]:
        title = self._title_from_group(index=index, group=group, profile=profile)
        summary = self._summary_from_group(group)
        chunk_ids = [chunk.id for chunk in group]

        pace_multiplier = {"slow": 1.2, "medium": 1.0, "fast": 0.8}[profile.pacing]
        module_minutes = max(8, int((10 + len(group) * 2) * pace_multiplier))

        steps = [
            {
                "step_id": f"module-{index}-step-1",
                "kind": "learn",
                "title": "Concept Walkthrough",
                "instruction": summary,
                "estimated_minutes": max(3, int(4 * pace_multiplier)),
            },
            {
                "step_id": f"module-{index}-step-2",
                "kind": "practice",
                "title": "Guided Practice",
                "instruction": self._practice_prompt(profile=profile, summary=summary),
                "estimated_minutes": max(3, int(3 * pace_multiplier)),
            },
            {
                "step_id": f"module-{index}-step-3",
                "kind": "challenge",
                "title": "Mini Challenge",
                "instruction": self._challenge_prompt(profile=profile, summary=summary),
                "estimated_minutes": max(2, int(3 * pace_multiplier)),
            },
        ]

        checkpoint = {
            "checkpoint_id": f"checkpoint-{index}",
            "module_id": f"module-{index}",
            "marker": "knowledge_check",
            "questions": self._checkpoint_questions(summary=summary, profile=profile),
        }

        return {
            "module_id": f"module-{index}",
            "title": title,
            "objective": f"Apply {title.lower()} to {profile.goals[0].lower()}",
            "teaching_style": profile.teaching_style,
            "pacing": profile.pacing,
            "chunk_ids": chunk_ids,
            "steps": steps,
            "checkpoint": checkpoint,
            "estimated_minutes": module_minutes,
        }

    def _title_from_group(
        self,
        index: int,
        group: list[ContentChunk],
        profile: Profile,
    ) -> str:
        first = group[0]
        explicit_title = first.metadata.get("title") or first.metadata.get("topic")
        if explicit_title:
            return str(explicit_title)
        sentence = self._first_sentence(first.text)
        trimmed = " ".join(sentence.split()[:6]).strip()
        if trimmed:
            return f"Module {index}: {trimmed}"
        return f"Module {index}: {profile.subject} Foundations"

    def _summary_from_group(self, group: list[ContentChunk]) -> str:
        sentences: list[str] = []
        for chunk in group:
            sentences.extend(self._SENTENCE_SPLIT.split(chunk.text))
        filtered = [sentence.strip() for sentence in sentences if sentence.strip()]
        if not filtered:
            return "Work through the core ideas and connect them to practical usage."
        return " ".join(filtered[:2])

    def _first_sentence(self, text: str) -> str:
        parts = self._SENTENCE_SPLIT.split(text.strip())
        return parts[0] if parts else text

    def _practice_prompt(self, profile: Profile, summary: str) -> str:
        return (
            f"Follow a guided example using this idea: {summary} "
            f"Then explain the result in one sentence for a {profile.pacing} pacing track."
        )

    def _challenge_prompt(self, profile: Profile, summary: str) -> str:
        return (
            f"Create a short solution that applies: {summary} "
            f"Match this style preference: {profile.teaching_style or 'hands-on'}."
        )

    def _checkpoint_questions(self, summary: str, profile: Profile) -> list[str]:
        return [
            f"What is the key takeaway from this module in your own words? ({summary})",
            f"How would you apply this concept to your goal: {profile.goals[0]}?",
            "What part still feels uncertain and why?",
        ]
