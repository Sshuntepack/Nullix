"""Simple in-memory caching utilities."""

from __future__ import annotations

import time
from collections import OrderedDict
from typing import Any, Hashable


class TTLCache:
    """A cache with per-item time-to-live expiration."""

    def __init__(self, default_ttl: float = 60.0) -> None:
        if default_ttl <= 0:
            raise ValueError("default_ttl must be positive")
        self._default_ttl = default_ttl
        self._store: dict[Hashable, tuple[Any, float]] = {}

    def set(self, key: Hashable, value: Any, ttl: float | None = None) -> None:
        """Store a value with an optional custom TTL (seconds)."""
        ttl = ttl if ttl is not None else self._default_ttl
        if ttl <= 0:
            raise ValueError("ttl must be positive")
        self._store[key] = (value, time.monotonic() + ttl)

    def get(self, key: Hashable, default: Any = None) -> Any:
        """Retrieve a value if it exists and has not expired."""
        if key not in self._store:
            return default
        value, expiry = self._store[key]
        if time.monotonic() > expiry:
            del self._store[key]
            return default
        return value

    def delete(self, key: Hashable) -> bool:
        """Remove an item. Return True if it existed."""
        return self._store.pop(key, None) is not None

    def clear(self) -> None:
        """Remove all items from the cache."""
        self._store.clear()

    def __len__(self) -> int:
        self._evict_expired()
        return len(self._store)

    def _evict_expired(self) -> None:
        """Remove all expired entries."""
        now = time.monotonic()
        expired = [k for k, (_, exp) in self._store.items() if now > exp]
        for k in expired:
            del self._store[k]

    def __contains__(self, key: Hashable) -> bool:
        return self.get(key) is not None


class LRUCache:
    """A least-recently-used cache with a fixed capacity."""

    def __init__(self, capacity: int = 128) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self._capacity = capacity
        self._store: OrderedDict[Hashable, Any] = OrderedDict()

    def get(self, key: Hashable, default: Any = None) -> Any:
        """Retrieve a value and mark it as recently used."""
        if key not in self._store:
            return default
        self._store.move_to_end(key)
        return self._store[key]

    def set(self, key: Hashable, value: Any) -> None:
        """Store a value, evicting the least-recently-used item if at capacity."""
        if key in self._store:
            self._store.move_to_end(key)
        self._store[key] = value
        if len(self._store) > self._capacity:
            self._store.popitem(last=False)

    def delete(self, key: Hashable) -> bool:
        """Remove an item. Return True if it existed."""
        try:
            del self._store[key]
            return True
        except KeyError:
            return False

    def clear(self) -> None:
        """Remove all items from the cache."""
        self._store.clear()

    def __len__(self) -> int:
        return len(self._store)

    def __contains__(self, key: Hashable) -> bool:
        return key in self._store
