from fastapi import FastAPI
from src.core import redis
from src.core.settings import redisSeggings

def register_redis(
    app: FastAPI
    ) -> None:
    @app.on_event("startup")
    async def create_redis_cache_pool() -> None:
       redis.redisBackend = redis.RedisBackend.init(redisSeggings.redis_cache_url)

    @app.on_event("shutdown")
    async def close_redis_cache_pool() -> None:
        await redis.redisBackend.redis_connection.close() # type: ignore
