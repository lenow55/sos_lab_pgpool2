from datetime import datetime, timedelta
from typing import Any, Type
from fastapi import Request, Response
from uuid import UUID, uuid4

from jose import jwt, JWTError
from jose.exceptions import ExpiredSignatureError
from pydantic import ValidationError
from exceptions.http_exceptions import UnauthorizedException

from src.core.redis import RedisBackend, redisBackend
from src.core.schemas import RefreshData, RefreshSessionData, AccessData, TokenType
from src.core.settings import tokenSettings, serverSettings

import logging
from src.core import logger as logger_mod
logger = logging.getLogger(__name__)

class RefreshSession:
    redisBackend: RedisBackend
    session_expire: int
    token_ttl: timedelta
    path: str
    key_name: str

    def __init__(
            self,
            redisBackend: RedisBackend,
            model: Type[AccessData],
            path: str,
            token_ttl: timedelta,
            key_name: str = "refresh_token"
    ) -> None:
        self.model = model
        self.path = path
        self.key_name = key_name
        self.token_ttl = token_ttl
        self.session_expire = int(token_ttl.total_seconds())
        if isinstance(redisBackend, RedisBackend):
            self.redisBackend = redisBackend
        else:
            raise AttributeError("RedisBackend not inited")

    def _create_refresh_token(
            self,
            refresh_id: UUID
    ) -> str:
        expire = datetime.utcnow() + self.token_ttl
        data: RefreshData = RefreshData(
            refresh_id=refresh_id,
            exp=expire,
            token_type=TokenType.REFRESH
        )
        encoded_jwt: str = jwt.encode(
            data.model_dump(mode='json'),
            tokenSettings.jwt_secret.get_secret_value(),
            algorithm=tokenSettings.jwt_algorithm)
        return encoded_jwt

    def _verify_refresh_token(
            self,
            refresh_token: str | None) -> RefreshData:
        if not refresh_token:
            raise UnauthorizedException(
                "Refresh token missing.")

        try:
            refresh_data: RefreshData = RefreshData(**jwt.decode(
                refresh_token,
                tokenSettings.jwt_secret.get_secret_value(),
                algorithms=[tokenSettings.jwt_algorithm]))
            return refresh_data

        except ExpiredSignatureError as e:
            raise UnauthorizedException(
                "Refresh token expired")
        except JWTError as e:
            raise UnauthorizedException(
                "Invalid refresh token.")
        except ValidationError as e:
            raise UnauthorizedException(
                f"Invalid refresh token payload {e.json()}")

    async def _create_refresh_session(
            self,
            refresh_token: str,
            data: RefreshSessionData,
            response: Response) -> Response:
        response.set_cookie(
            key=self.key_name,
            value=refresh_token,
            httponly=True,
            secure=serverSettings.secure,
            path=self.path,
            samesite='lax',
            max_age=self.session_expire
        )
        await self.redisBackend.set(
            key=data.refresh_id.bytes,
            value=data.model_dump_json(),
            expire=data.expires_at
        )
        return response

    async def create_refresh_session(
            self,
            data: AccessData,
            response: Response
    ) -> Response:
        refresh_id: UUID = uuid4()
        refresh_token: str = self._create_refresh_token(
            refresh_id=refresh_id)

        refresh_session_data: RefreshSessionData = RefreshSessionData(
            **data.model_dump(include={"user_id", "username"}),
            refresh_id=refresh_id, expires_at=self.session_expire,
            created_at=datetime.now()
        )

        response = await self._create_refresh_session(
            refresh_token=refresh_token,
            data=refresh_session_data,
            response=response)

        return response

    async def update_refresh_session(
            self,
            request: Request,
            response: Response
    ) -> AccessData:
        old_refresh_token: str | None = request.cookies.get(
            self.key_name)
        refresh_data: RefreshData = self._verify_refresh_token(
            refresh_token=old_refresh_token)
        store_result: Any = await self.redisBackend.get(
            refresh_data.refresh_id.bytes)
        if not isinstance(store_result, str):
            raise UnauthorizedException(
                f"Refresh session lost")
        try:
            refresh_session_data: RefreshSessionData = \
                RefreshSessionData.model_validate_json(json_data=store_result)
        except ValidationError as e:
            raise UnauthorizedException(
                f"Refresh session corrupted {e.json()}")

        refresh_session_data.refresh_id = uuid4()

        refresh_token: str = self._create_refresh_token(
            refresh_id=refresh_session_data.refresh_id)

        response = await self._create_refresh_session(
            refresh_token=refresh_token,
            data=refresh_session_data,
            response=response)

        return AccessData(
            user_id=refresh_session_data.user_id,
            username=refresh_session_data.username,
            token_type=None, exp=None)

    async def delete_refresh_session(
            self,
            request: Request,
            response: Response
    ) -> Response:
        old_refresh_token: str | None = request.cookies.get(
            self.key_name)
        refresh_data: RefreshData = self._verify_refresh_token(
            refresh_token=old_refresh_token)
        await self.redisBackend.delete(
            refresh_data.refresh_id.bytes)
        response.delete_cookie(self.key_name)
        return response


refreshSessionManager: RefreshSession | None = None
