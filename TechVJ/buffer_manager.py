"""
buffer_manager.py — Global RAM buffer manager.
Bir vaqtda bir nechta foydalanuvchi yuklab olayotganda
jami RAM ishlatilishini 500MB da cheklaydi.
"""
from __future__ import annotations
import asyncio

BUFFER_THRESHOLD = 300 * 1024 * 1024   # 300 MB
GLOBAL_RAM_LIMIT  = 500 * 1024 * 1024  # 500 MB


class BufferManager:
    """
    RAM bufer allokatsiyasini boshqaradi.
    should_buffer() → True bo'lsa RAM ishlatiladi, False bo'lsa disk.
    Lock ichida check+increment atomik — race condition yo'q.
    """

    def __init__(self) -> None:
        self._used: int = 0
        self._lock: asyncio.Lock = asyncio.Lock()

    async def should_buffer(self, file_size: int) -> bool:
        """
        RAMga olish kerakmi? Atomik tekshiruv va rezerv.
        True qaytarsa → file_size qiymat _used ga qo'shilgan.
        False qaytarsa → hech narsa o'zgarmagan.
        """
        async with self._lock:
            if file_size > BUFFER_THRESHOLD:
                return False
            if self._used + file_size > GLOBAL_RAM_LIMIT:
                return False
            self._used += file_size
            return True

    async def release(self, file_size: int) -> None:
        """Upload/download tugagandan keyin RAM ni bo'shatadi."""
        async with self._lock:
            self._used = max(0, self._used - file_size)

    @property
    def used_bytes(self) -> int:
        """Hozir RAMda necha bayt band (monitoring uchun)."""
        return self._used


# Modul darajasida singleton
buffer_mgr = BufferManager()
