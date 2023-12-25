from typing import Annotated

from fastapi import (
    Depends,
)
from tortoise.exceptions import DoesNotExist

from src.schemas.user import User
from src.core.security import oauth2_scheme
from src.core.security import verify_token

from src.exceptions.http_exceptions import (
    UnauthorizedException,
)
from src.core.schemas import TokenData
from src.crud.userService import userService

import logging
from src.core import logger as logger_mod
from src.core.schemas import Status
logger = logging.getLogger(__name__)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> User:
    logger.debug(token)
    token_data: TokenData | None = await verify_token(token)
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
