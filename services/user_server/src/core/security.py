import bcrypt
from typing import Any
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from tortoise.exceptions import DoesNotExist
from src.exceptions.http_exceptions import NotFoundException, UnauthorizedException
from src.database.models import User
from src.core.schemas import TokenData, TokenType
from src.core.settings import tokenSettings, serverSettings

import logging
from src.core import logger as logger_mod
logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=serverSettings.root_path+"v1/auth/login")


async def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(
        plain_password.encode(),
        hashed_password)


def get_password_hash(password: str) -> bytes:
    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt())


async def authenticate_user(username_or_email: str, password: str) -> User:
    logger.debug(username_or_email)
    if "@" in username_or_email:
        try:
            db_user: User = await User.get(email=username_or_email, is_deleted=False)
        except DoesNotExist:
            raise NotFoundException(
                detail=f"User with email {username_or_email} not found")
    else:
        try:
            db_user: User = await User.get(username=username_or_email, is_deleted=False)
        except DoesNotExist:
            raise NotFoundException(
                detail=f"User with username {username_or_email} not found")

    if not await verify_password(password, db_user.hashed_password):
        raise UnauthorizedException(
            "Wrong username, email or password.")

    return db_user


async def create_access_token(data: TokenData, expires_delta: timedelta | None = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + tokenSettings.access_token_ttl
    logger.debug(datetime.utcnow())
    data.exp=expire
    data.token_type = TokenType.ACCESS
    logger.debug(data.model_dump_json())
    encoded_jwt: str = jwt.encode(
        data.model_dump(mode='json'),
        tokenSettings.jwt_secret.get_secret_value(),
        algorithm=tokenSettings.jwt_algorithm)
    return encoded_jwt


async def create_refresh_token(data: TokenData, expires_delta: timedelta | None = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + tokenSettings.refresh_token_ttl
    data.exp=expire
    data.token_type = TokenType.REFRESH
    encoded_jwt: str = jwt.encode(
        data.model_dump(mode='json'),
        tokenSettings.jwt_secret.get_secret_value(),
        algorithm=tokenSettings.jwt_algorithm)
    return encoded_jwt


async def verify_token(token: str) -> TokenData:
    """
    Verify a JWT token and return TokenData if valid.

    Parameters
    ----------
    token: str
        The JWT token to be verified.
    db: AsyncSession
        Database session for performing database operations.

    Returns
    -------
    TokenData
        TokenData instance if the token is valid

    Raises
    -------
    UnauthorizedException
        It token or payload not valid
    """
    # is_blacklisted = await crud_token_blacklist.exists(db, token=token)
    # if is_blacklisted:
    #    return None

    try:

        logger.debug(token)
        token_data: TokenData = TokenData(**jwt.decode(
            token,
            tokenSettings.jwt_secret.get_secret_value(),
            algorithms=[tokenSettings.jwt_algorithm]))
        return token_data

    except JWTError as e:
        logger.error(e)
        raise UnauthorizedException("Invalid token.")
    except ValidationError as e:
        raise UnauthorizedException(f"Invalid token payload {e.json()}")
