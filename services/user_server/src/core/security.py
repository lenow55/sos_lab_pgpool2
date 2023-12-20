import bcrypt
from typing import Any
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from tortoise.exceptions import DoesNotExist
from exceptions.http_exceptions import NotFoundException
from src.database.models import User
from src.core.schemas import TokenData
from src.core.settings import tokenSettings
from src.schemas.user import UserRead

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/login")


async def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(
        plain_password.encode(),
        hashed_password)


def get_password_hash(password: str) -> bytes:
    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt())


async def authenticate_user(username_or_email: str, password: str) -> UserRead:
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
        return False

    return await UserRead.from_tortoise_orm(db_user)


async def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt: str = jwt.encode(
        to_encode,
        tokenSettings.jwt_secret.get_secret_value(),
        algorithm=tokenSettings.jwt_algorithm)
    return encoded_jwt


async def create_refresh_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + tokenSettings.refresh_token_ttl
    to_encode.update({"exp": expire})
    encoded_jwt: str = jwt.encode(
        to_encode, tokenSettings.jwt_secret.get_secret_value(),
        algorithm=tokenSettings.jwt_algorithm)
    return encoded_jwt


async def verify_token(token: str) -> TokenData | None:
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
    TokenData | None
        TokenData instance if the token is valid, None otherwise.
    """
    # is_blacklisted = await crud_token_blacklist.exists(db, token=token)
    # if is_blacklisted:
    #    return None

    try:
        payload = jwt.decode(
            token,
            tokenSettings.jwt_secret.get_secret_value(),
            algorithms=[tokenSettings.jwt_algorithm])
        token_dict = payload.get("data")
        if not isinstance(token_dict, dict):
            return None
        return TokenData(**token_dict)

    except JWTError:
        return None
    except ValidationError:
        return None
