"""
progress_store.py — Disk-free progress tracking.
Disk .txt fayllar o'rniga RAM dict ishlatiladi.
"""
from __future__ import annotations

_store: dict[str, str] = {}  # key: f"{msg_id}_down" | f"{msg_id}_up"


def write_progress(key: str, current: int, total: int) -> None:
    """Progress foizini RAMga yozadi."""
    if total > 0:
        _store[key] = f"{current * 100 / total:.1f}%"


def read_progress(key: str) -> str:
    """Hozirgi progress qiymatini qaytaradi."""
    return _store.get(key, "0.0%")


def clear_progress(key: str) -> None:
    """Key ni o'chiradi (download/upload tugagandan keyin)."""
    _store.pop(key, None)
