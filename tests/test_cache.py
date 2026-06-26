"""Tests for nullix.cache — comprehensive coverage."""

import time

import pytest

from nullix.cache import LRUCache, TTLCache


class TestTTLCacheBasic:
    def test_set_and_get(self):
        c = TTLCache(default_ttl=60)
        c.set("a", 1)
        assert c.get("a") == 1

    def test_get_missing(self):
        c = TTLCache(default_ttl=60)
        assert c.get("nope") is None

    def test_invalid_ttl(self):
        with pytest.raises(ValueError):
            TTLCache(default_ttl=0)

    def test_custom_default(self):
        c = TTLCache(default_ttl=60)
        assert c.get("x", default="fallback") == "fallback"

    def test_set_invalid_ttl(self):
        c = TTLCache(default_ttl=60)
        with pytest.raises(ValueError, match="positive"):
            c.set("a", 1, ttl=-1)

    def test_delete_existing(self):
        c = TTLCache(default_ttl=60)
        c.set("key", "val")
        assert c.delete("key") is True
        assert c.get("key") is None

    def test_delete_missing(self):
        c = TTLCache(default_ttl=60)
        assert c.delete("nope") is False

    def test_clear(self):
        c = TTLCache(default_ttl=60)
        c.set("a", 1)
        c.set("b", 2)
        c.clear()
        assert c.get("a") is None
        assert c.get("b") is None

    def test_len(self):
        c = TTLCache(default_ttl=60)
        c.set("a", 1)
        c.set("b", 2)
        assert len(c) == 2

    def test_contains(self):
        c = TTLCache(default_ttl=60)
        c.set("a", 1)
        assert "a" in c
        assert "b" not in c

    def test_expiration(self):
        c = TTLCache(default_ttl=60)
        c.set("fast", "gone", ttl=0.05)
        time.sleep(0.1)
        assert c.get("fast") is None

    def test_len_evicts_expired(self):
        c = TTLCache(default_ttl=60)
        c.set("stay", "here", ttl=60)
        c.set("go", "away", ttl=0.05)
        time.sleep(0.1)
        assert len(c) == 1


class TestLRUCache:
    def test_set_and_get(self):
        c = LRUCache(capacity=3)
        c.set("a", 1)
        assert c.get("a") == 1

    def test_get_missing(self):
        c = LRUCache(capacity=3)
        assert c.get("nope") is None

    def test_get_custom_default(self):
        c = LRUCache(capacity=3)
        assert c.get("nope", default=42) == 42

    def test_eviction(self):
        c = LRUCache(capacity=2)
        c.set("a", 1)
        c.set("b", 2)
        c.set("c", 3)
        assert c.get("a") is None
        assert c.get("b") == 2
        assert c.get("c") == 3

    def test_access_refreshes_order(self):
        c = LRUCache(capacity=2)
        c.set("a", 1)
        c.set("b", 2)
        c.get("a")
        c.set("c", 3)
        assert c.get("a") == 1
        assert c.get("b") is None

    def test_overwrite_existing(self):
        c = LRUCache(capacity=2)
        c.set("a", 1)
        c.set("a", 99)
        assert c.get("a") == 99
        assert len(c) == 1

    def test_delete_existing(self):
        c = LRUCache(capacity=3)
        c.set("a", 1)
        assert c.delete("a") is True
        assert c.get("a") is None

    def test_delete_missing(self):
        c = LRUCache(capacity=3)
        assert c.delete("nope") is False

    def test_clear(self):
        c = LRUCache(capacity=3)
        c.set("a", 1)
        c.clear()
        assert len(c) == 0

    def test_len(self):
        c = LRUCache(capacity=5)
        c.set("a", 1)
        c.set("b", 2)
        assert len(c) == 2

    def test_contains(self):
        c = LRUCache(capacity=5)
        c.set("a", 1)
        assert "a" in c
        assert "b" not in c

    def test_invalid_capacity(self):
        with pytest.raises(ValueError, match="positive"):
            LRUCache(capacity=0)
