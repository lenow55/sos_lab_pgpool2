from typing import Set, Any

from aioredis import Redis
import aioredis

from src.core.cache import ABCCacheBackend


class RedisBackend(ABCCacheBackend):
    redis_connection: Redis

    @staticmethod
    async def init(url: str) -> "RedisBackend":
        redis = RedisBackend()
        redis.redis_connection = aioredis.from_url(url=url)
        return redis

    async def get(self, key: str | bytes):
        """Get Value from Key"""
        return await self.redis_connection.get(key)

    async def set(self, key: str|bytes, value, expire: int = 0, pexpire: int = 0, exists=False):
        """Set Key to Value"""
        return await self.redis_connection.set(key, value, ex=expire, px=pexpire, xx=exists)

    async def pttl(self, key: str) -> int:
        """Get PTTL from a Key"""
        return int(await self.redis_connection.pttl(key))

    async def ttl(self, key: str) -> int:
        """Get TTL from a Key"""
        return int(await self.redis_connection.ttl(key))

    async def pexpire(self, key: str, pexpire: int) -> bool:
        """Sets and PTTL for a Key"""
        return bool(await self.redis_connection.pexpire(key, pexpire))

    async def expire(self, key: str, expire: int) -> bool:
        """Sets and TTL for a Key"""
        return bool(await self.redis_connection.expire(key, expire))

    async def incr(self, key: str) -> int:
        """Increases an Int Key"""
        return int(await self.redis_connection.incr(key))

    async def decr(self, key: str) -> int:
        """Decreases an Int Key"""
        return int(await self.redis_connection.decr(key))

    async def delete(self, key: str | bytes):
        """Delete value of a Key"""
        return await self.redis_connection.delete(key)

    async def smembers(self, key: str) -> Set:
        """Gets Set Members"""
        return set(await self.redis_connection.smembers(key))

    async def sadd(self, key: str, value: Any) -> bool:
        """Adds a Member to a Dict"""
        return bool(await self.redis_connection.sadd(key, value))

    async def srem(self, key: str, member: Any) -> bool:
        """Removes a Member from a Set"""
        return bool(await self.redis_connection.srem(key, member))

    async def exists(self, key: str) -> bool:
        """Checks if a Key exists"""
        return bool(await self.redis_connection.exists(key))
    
redisBackend: RedisBackend | None = None

