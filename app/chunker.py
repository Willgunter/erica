from __future__ import annotations

import uuid


def _smart_slice(text: str, start: int, max_len: int) -> tuple[str, int]:
    end = min(start + max_len, len(text))
    if end == len(text):
        return text[start:end], end

    cut = text.rfind(" ", start, end)
    if cut <= start:
        cut = end
    return text[start:cut], cut


def build_chunks(
    units: list[dict], *, target_chars: int = 240, overlap_chars: int = 40
) -> list[dict]:
    chunks: list[dict] = []
    idx = 0

    for unit in units:
        text = unit.get("text", "").strip()
        if not text:
            continue
        metadata = unit.get("metadata") or {}

        start = 0
        while start < len(text):
            piece, end = _smart_slice(text, start, target_chars)
            piece = piece.strip()
            if piece:
                chunks.append(
                    {
                        "id": str(uuid.uuid4()),
                        "chunk_index": idx,
                        "text": piece,
                        "metadata": {
                            **metadata,
                            "start_char": start,
                            "end_char": end,
                            "length": len(piece),
                        },
                    }
                )
                idx += 1
            if end >= len(text):
                break
            start = max(0, end - overlap_chars)

    return chunks
