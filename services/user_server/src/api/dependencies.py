from typing import Annotated

from fastapi import (
    Depends,
)
from tortoise.exceptions import DoesNotExist

from src.core.sessions import refresh_session
from src.core.sessions.refresh_session import RefreshSession, refreshSessionManager
from src.core import redis
from src.core.redis import RedisBackend
from src.core.settings import redisSeggings, tokenSettings, serverSettings

from src.schemas.user import User
from src.core.security import oauth2_scheme
from src.core.security import verify_access_token

from src.exceptions.http_exceptions import (
    UnauthorizedException,
)
from src.core.schemas import AccessData
from src.crud.userService import userService

import logging
from src.core import logger as logger_mod
from src.core.schemas import Status
logger = logging.getLogger(__name__)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> User:
    logger.debug(token)
    token_data: AccessData | None = await verify_access_token(token)
    if token_data is None:
        raise UnauthorizedException(
            "User not authenticated.")

    try:
        return await userService.find_user(
            uuid=token_data.user_id,
            is_deleted=False)
    except DoesNotExist:
        raise UnauthorizedException(
            detail=f"User with username {token_data.username} not found")

def get_refresh_session_manager() -> RefreshSession:
    if isinstance(
            refresh_session.refreshSessionManager, RefreshSession):
        return refresh_session.refreshSessionManager

    if not isinstance(redis.redisBackend, RedisBackend):
        redis.redisBackend = RedisBackend.init(redisSeggings.redis_cache_url)
        logger.warn("Init redis from session")
    refresh_session.refreshSessionManager = RefreshSession(
        redisBackend=redis.redisBackend,
        model=AccessData,
        path=f"{serverSettings.root_path}v1/auth",
        token_ttl=tokenSettings.refresh_token_ttl
    )
    return refresh_session.refreshSessionManager
