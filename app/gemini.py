from __future__ import annotations

import logging
import os
from typing import Any, Iterable


DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"
_PREFERRED_MODELS = (
    "gemini-2.5-flash-latest",
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
    "gemini-1.5-flash-latest",
)


def _normalize_model_name(name: str) -> str:
    return name.replace("models/", "", 1).strip()


def _dedupe(items: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        ordered.append(item)
    return ordered


def _supports_generate_content(model: Any) -> bool:
    methods = getattr(model, "supported_generation_methods", []) or []
    return "generateContent" in methods


def _discover_supported_models(genai: Any) -> list[str]:
    supported: list[str] = []
    for model in genai.list_models():
        if not _supports_generate_content(model):
            continue
        name = _normalize_model_name(getattr(model, "name", ""))
        if name:
            supported.append(name)
    return supported


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


def _model_exists(genai: Any, model_name: str) -> bool:
    get_model = getattr(genai, "get_model", None)
    if not callable(get_model):
        return True

    full_name = model_name if model_name.startswith("models/") else f"models/{model_name}"
    get_model(full_name)
    return True


def resolve_gemini_model_name(genai: Any, logger: logging.Logger, component: str) -> str:
    configured = _normalize_model_name(os.environ.get("GEMINI_MODEL", ""))
    discovered_supported: list[str] = []
    try:
        discovered_supported = _discover_supported_models(genai)
    except Exception as exc:
        logger.warning("[%s] Gemini model discovery failed (%s)", component, exc)

    preferred_from_discovery = None
    if discovered_supported:
        for preferred in _PREFERRED_MODELS:
            if preferred in discovered_supported:
                preferred_from_discovery = preferred
                break
        if not preferred_from_discovery:
            preferred_from_discovery = _pick_discovered_model(
                type("Model", (), {"name": name, "supported_generation_methods": ["generateContent"]})()
                for name in discovered_supported
            )

    candidates = _dedupe(
        [
            configured,
            preferred_from_discovery or "",
            *discovered_supported,
            *_PREFERRED_MODELS,
            DEFAULT_GEMINI_MODEL,
        ]
    )
    candidates = [name for name in candidates if name]

    if configured:
        logger.info("[%s] GEMINI_MODEL requested: %s", component, configured)

    for candidate in candidates:
        try:
            _model_exists(genai, candidate)
            logger.info("[%s] Gemini model selected: %s", component, candidate)
            return candidate
        except Exception as exc:
            logger.warning("[%s] Gemini model unavailable: %s (%s)", component, candidate, exc)

    logger.warning("[%s] Falling back to default Gemini model: %s", component, DEFAULT_GEMINI_MODEL)

    return DEFAULT_GEMINI_MODEL


def init_gemini_model(genai: Any, api_key: str, logger: logging.Logger, component: str):
    genai.configure(api_key=api_key)
    model_name = resolve_gemini_model_name(genai, logger, component)
    logger.info("[%s] Gemini initialized with model %s.", component, model_name)
    return genai.GenerativeModel(model_name), model_name
