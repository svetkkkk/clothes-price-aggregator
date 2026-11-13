"""Кэш рейтинга: Redis, а если он недоступен, то память процесса."""
import json
import os
import time


class MemoryCache:
    def __init__(self):
        self._data = {}

    def get(self, key):
        item = self._data.get(key)
        if not item:
            return None
        expires, value = item
        if expires < time.time():
            del self._data[key]
            return None
        return value

    def set(self, key, value, ttl=300):
        self._data[key] = (time.time() + ttl, value)


class RedisCache:
    def __init__(self, client):
        self.client = client

    def get(self, key):
        raw = self.client.get(key)
        return json.loads(raw) if raw else None

    def set(self, key, value, ttl=300):
        self.client.set(key, json.dumps(value, ensure_ascii=False), ex=ttl)


def build_cache():
    url = os.getenv("REDIS_URL")
    if url:
        try:
            import redis
            client = redis.Redis.from_url(url)
            client.ping()
            return RedisCache(client)
        except Exception:
            pass  # Redis недоступен: работаем без него, но не падаем
    return MemoryCache()
