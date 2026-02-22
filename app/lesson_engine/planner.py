from __future__ import annotations

import json
import logging
import os
import re
import uuid
from typing import Any

from ..gemini import init_gemini_model
from .models import ContentChunk, Profile


_logger = logging.getLogger(__name__)


def _mask_key(value: str | None) -> str:
    if not value:
        return "missing"
    if len(value) <= 8:
        return "***"
    return f"{value[:4]}...{value[-4:]}"


# ─── helpers ─────────────────────────────────────────────────────────────────

def _slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def _estimate_minutes(chunk_count: int, pacing: str) -> int:
    base = max(5, chunk_count * 3)
    factor = {"relaxed": 1.4, "moderate": 1.0, "intensive": 0.7}.get(pacing, 1.0)
    return max(5, round(base * factor))


def _init_gemini():
    try:
        import google.generativeai as genai
        api_key = os.environ.get("GEMINI_API_KEY", "")
        _logger.debug("[Planner] Initializing Gemini: has_api_key=%s key=%s", bool(api_key), _mask_key(api_key))
        if api_key:
            model, _ = init_gemini_model(genai, api_key, _logger, "Planner")
            return model
        _logger.warning("[Planner] GEMINI_API_KEY is missing; planner will use fallback modules.")
    except Exception as e:
        _logger.exception("[Planner] Gemini initialization failed: %s", e)
    return None


# ─── planner ─────────────────────────────────────────────────────────────────

class LessonPlanner:
    def __init__(self):
        self.gemini_model = _init_gemini()

    def plan(
        self,
        profile: Profile,
        chunks: list[ContentChunk],
    ) -> tuple[list[dict], list[dict], int]:
        full_text = "\n\n".join(c.text for c in chunks)
        analyzed = self._analyze_with_gemini(full_text, profile)

        modules: list[dict] = []
        checkpoints: list[dict] = []

        for index, concept in enumerate(analyzed, start=1):
            module = self._build_module_from_concept(index, concept, profile, chunks)
            modules.append(module)
            checkpoints.append(module["checkpoint"])

        estimated_duration = sum(m["estimated_minutes"] for m in modules)
        return modules, checkpoints, estimated_duration

    # ── gemini analysis ───────────────────────────────────────────────────────

    def _analyze_with_gemini(self, full_text: str, profile: Profile) -> list[dict]:
        """Use Gemini to extract structured learning modules from raw content."""
        _logger.info(
            "[Planner] Gemini analysis invoked | subject=%s | chars=%d | model_ready=%s",
            profile.subject,
            len(full_text),
            bool(self.gemini_model),
        )
        if not self.gemini_model:
            _logger.debug("[Planner] Gemini unavailable; using fallback analysis for subject=%s", profile.subject)
            return self._fallback_analysis(full_text, profile)

        try:
            text_sample = full_text[:20000]
            _logger.info(
                "[Planner] Sending Gemini request with sample_chars=%d (total=%d) goals=%d",
                len(text_sample),
                len(full_text),
                len(profile.goals),
            )
            prompt = f"""You are an expert educational AI analyzing study material for a student.

Subject: {profile.subject}
Student Goals: {', '.join(profile.goals[:2]) if profile.goals else 'master the subject'}

Here is the raw content from their study material (practice exam/notes):
---
{text_sample}
---

Analyze this content and extract 3-5 distinct learning modules based on the CONCEPTS being tested.
Do NOT just copy exam questions — identify the underlying concepts and TEACH them.

For each module provide:
1. A clear concept title (4-7 words)
2. concept_explanation: A thorough, clear explanation teaching this concept (4-5 sentences, written as if tutoring the student)
3. key_insight: The single most important sentence to remember
4. flashcards: Create 5-7 HIGH-QUALITY flashcards that test understanding of THIS SPECIFIC CONTENT. Each flashcard should:
   - Front: A specific term, definition prompt, or concept question from the material
   - Back: A clear, complete answer with relevant details from the content
   - Cover key facts, definitions, processes, and relationships from the actual material
5. exam_questions: Create 2-3 challenging questions that TEST understanding of this concept:
   - Use actual questions from the material if available
   - Otherwise, create questions that test application and understanding (not just memorization)
   - Include detailed answers with explanations
   - Provide 2-3 helpful hints that guide thinking without giving away the answer

CRITICAL: The flashcards MUST be based on the ACTUAL content provided, not generic questions. Extract specific facts, terms, processes, and concepts from the text.

Return ONLY valid JSON with NO markdown fences, NO extra text:
{{"modules": [{{"title": "...", "concept_explanation": "...", "key_insight": "...", "flashcards": [{{"front": "...", "back": "..."}}], "exam_questions": [{{"question": "...", "answer": "...", "hints": ["...", "..."]}}]}}]}}"""

            response = self.gemini_model.generate_content(prompt)
            text = response.text.strip()
            _logger.debug(
                "[Planner] Gemini response raw_length=%d prefix=%r",
                len(text),
                text[:120].replace("\n", " "),
            )

            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()

            parsed = json.loads(text)
            modules = parsed.get("modules", [])
            if modules:
                _logger.info("[Planner] Gemini returned %d modules for subject=%s", len(modules), profile.subject)
                for i, mod in enumerate(modules, 1):
                    fc_count = len(mod.get("flashcards", []))
                    eq_count = len(mod.get("exam_questions", []))
                    _logger.debug(
                        "[Planner] Module %d: title=%s flashcards=%d exam_questions=%d",
                        i,
                        mod.get("title", "Untitled"),
                        fc_count,
                        eq_count,
                    )
                return modules
        except Exception as e:
            _logger.exception("[Planner] Gemini analysis failed: %s", e)
            if "not found" in str(e).lower():
                self.gemini_model = None
                _logger.warning("[Planner] Disabled Gemini model after NotFound; set GEMINI_MODEL to a valid value.")
            _logger.warning("[Planner] Falling back to heuristic analysis for subject=%s", profile.subject)

        return self._fallback_analysis(full_text, profile)

    def _fallback_analysis(self, full_text: str, profile: Profile) -> list[dict]:
        """Simple fallback when Gemini is unavailable."""
        _logger.warning("[Planner] Fallback analysis running for subject=%s", profile.subject)
        words = full_text.split()
        chunk_size = max(200, len(words) // 4)
        segments = []
        for i in range(0, len(words), chunk_size):
            seg = " ".join(words[i:i + chunk_size])
            if seg.strip():
                segments.append(seg)
        segments = segments[:4]

        modules = []
        for i, seg in enumerate(segments):
            title_words = [w for w in seg.split() if len(w) > 4][:4]
            title = " ".join(title_words).title() or f"Module {i+1}"
            
            sentences = [s.strip() for s in seg.split('.') if len(s.strip()) > 20][:7]
            flashcards = []
            for j, sentence in enumerate(sentences[:7]):
                words = sentence.split()
                if len(words) > 5:
                    key_term = ' '.join(words[:3])
                    flashcards.append({
                        "front": f"What is {key_term}?",
                        "back": sentence
                    })
            
            if len(flashcards) < 5:
                flashcards.extend([
                    {"front": f"What is {title}?", "back": seg[:120]},
                    {"front": f"Why is {title} important?", "back": f"It helps achieve: {profile.goals[0] if profile.goals else 'your goals'}"},
                ])
            
            modules.append({
                "title": title,
                "concept_explanation": seg[:500],
                "key_insight": f"Focus on understanding {title.lower()} thoroughly.",
                "flashcards": flashcards[:7],
                "exam_questions": [
                    {"question": f"Explain the concept of {title} in your own words.", "answer": seg[:200], "hints": ["Think about the definition", "Consider real examples"]},
                    {"question": f"How does {title} relate to {profile.subject}?", "answer": "Connect the concept to its application in the subject.", "hints": ["Think about practical uses"]},
                ],
            })
        return modules

    # ── module builder ────────────────────────────────────────────────────────

    def _build_module_from_concept(
        self,
        index: int,
        concept: dict[str, Any],
        profile: Profile,
        chunks: list[ContentChunk],
    ) -> dict:
        title = concept.get("title", f"Module {index}")
        concept_explanation = concept.get("concept_explanation", "")
        key_insight = concept.get("key_insight", "")
        flashcards = concept.get("flashcards", [])
        exam_questions = concept.get("exam_questions", [])

        steps = self._build_steps(concept_explanation, profile, title)
        checkpoint = self._build_checkpoint(index, title, exam_questions, profile)

        chunks_per_module = max(1, len(chunks) // max(1, index))
        start = (index - 1) * chunks_per_module
        end = start + chunks_per_module
        chunk_ids = [c.id for c in chunks[start:end]]

        return {
            "module_id": f"module-{index}",
            "title": title,
            "objective": f"Understand and apply {title.lower()}",
            "teaching_style": profile.teaching_style,
            "pacing": profile.pacing,
            "chunk_ids": chunk_ids,
            "concept_explanation": concept_explanation,
            "key_insight": key_insight,
            "flashcards": flashcards,
            "exam_questions": exam_questions,
            "steps": steps,
            "checkpoint": checkpoint,
            "estimated_minutes": _estimate_minutes(max(3, len(flashcards)), profile.pacing),
        }

    # ── steps ─────────────────────────────────────────────────────────────────

    def _build_steps(
        self, concept_explanation: str, profile: Profile, title: str
    ) -> list[dict]:
        return [
            {
                "step_id": str(uuid.uuid4()),
                "kind": "learn",
                "title": "Concept Walkthrough",
                "instruction": concept_explanation,
                "media_ref": None,
            },
            {
                "step_id": str(uuid.uuid4()),
                "kind": "practice",
                "title": "Guided Practice",
                "instruction": (
                    f"Review the flashcards for {title}. "
                    f"Try to explain each concept back in your own words before flipping."
                ),
                "media_ref": None,
            },
            {
                "step_id": str(uuid.uuid4()),
                "kind": "challenge",
                "title": "AI Spar",
                "instruction": (
                    "Test your understanding with Erica. "
                    "She will ask you questions from the practice exam and guide you to the right answers."
                ),
                "media_ref": None,
            },
        ]

    # ── checkpoint ────────────────────────────────────────────────────────────

    def _build_checkpoint(
        self,
        index: int,
        title: str,
        exam_questions: list[dict],
        profile: Profile,
    ) -> dict:
        question_texts = (
            [q["question"] for q in exam_questions[:3]]
            if exam_questions
            else [
                f"Explain {title} in your own words.",
                f"How does {title} connect to {profile.goals[0] if profile.goals else 'your goals'}?",
                "What's still unclear about this concept?",
            ]
        )
        return {
            "checkpoint_id": f"checkpoint-{index}",
            "module_id": f"module-{index}",
            "marker": "knowledge_check",
            "questions": question_texts,
        }
