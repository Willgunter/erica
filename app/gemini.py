from __future__ import annotations

import logging
import os
from typing import Any, Iterable


DEFAULT_GEMINI_MODEL = "gemini-2.0-flash"
_PREFERRED_MODELS = (
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
    "gemini-1.5-flash-latest",
)


def _normalize_model_name(name: str) -> str:
    return name.replace("models/", "", 1).strip()


def _supports_generate_content(model: Any) -> bool:
    methods = getattr(model, "supported_generation_methods", []) or []
    return "generateContent" in methods


def _pick_discovered_model(models: Iterable[Any]) -> str | None:
    supported: list[str] = []
    for model in models:
        if not _supports_generate_content(model):
            continue
        name = _normalize_model_name(getattr(model, "name", ""))
        if name:
            supported.append(name)

    if not supported:
        return None

    for preferred in _PREFERRED_MODELS:
        if preferred in supported:
            return preferred

    for name in supported:
        if name.startswith("gemini") and "flash" in name:
            return name

    for name in supported:
        if name.startswith("gemini"):
            return name

    return supported[0]


def resolve_gemini_model_name(genai: Any, logger: logging.Logger, component: str) -> str:
    configured = _normalize_model_name(os.environ.get("GEMINI_MODEL", ""))
    if configured:
        logger.info("[%s] Gemini model from GEMINI_MODEL=%s", component, configured)
        return configured

    try:
        discovered = _pick_discovered_model(genai.list_models())
        if discovered:
            logger.info("[%s] Gemini model auto-selected: %s", component, discovered)
            return discovered
        logger.warning(
            "[%s] No generateContent Gemini model discovered; defaulting to %s",
            component,
            DEFAULT_GEMINI_MODEL,
        )
    except Exception as exc:
        logger.warning(
            "[%s] Gemini model discovery failed; defaulting to %s (%s)",
            component,
            DEFAULT_GEMINI_MODEL,
            exc,
        )

    return DEFAULT_GEMINI_MODEL


def init_gemini_model(genai: Any, api_key: str, logger: logging.Logger, component: str):
    genai.configure(api_key=api_key)
    model_name = resolve_gemini_model_name(genai, logger, component)
    logger.info("[%s] Gemini initialized with model %s.", component, model_name)
    return genai.GenerativeModel(model_name), model_name
