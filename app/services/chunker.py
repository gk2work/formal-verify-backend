"""
Chunker — document chunking utilities for RAG ingestion.

Provides the Chunk dataclass used throughout the RAG pipeline.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Chunk:
    """A single chunk of text with associated metadata for RAG ingestion."""
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)


def chunk_text(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 100,
    metadata: dict[str, Any] | None = None,
) -> list[Chunk]:
    """
    Split text into overlapping chunks of approximately chunk_size characters.

    Args:
        text: The source text to chunk.
        chunk_size: Target character count per chunk.
        chunk_overlap: Number of characters to overlap between consecutive chunks.
        metadata: Metadata dict attached to every chunk (e.g. source, doc_type).

    Returns:
        List of Chunk objects.
    """
    if not text.strip():
        return []

    base_meta = metadata or {}
    chunks: list[Chunk] = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        # Try to break at a sentence or paragraph boundary within the window
        if end < len(text):
            for sep in ("\n\n", "\n", ". ", " "):
                boundary = text.rfind(sep, start, end)
                if boundary != -1:
                    end = boundary + len(sep)
                    break

        chunk_text_content = text[start:end].strip()
        if chunk_text_content:
            chunk_meta = {**base_meta, "chunk_index": len(chunks)}
            chunks.append(Chunk(text=chunk_text_content, metadata=chunk_meta))

        start = end - chunk_overlap if end - chunk_overlap > start else end

    return chunks
