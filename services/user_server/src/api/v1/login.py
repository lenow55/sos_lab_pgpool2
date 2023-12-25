from typing import Annotated
from fastapi import APIRouter, Depends, Request, Response
from fastapi.security import OAuth2PasswordRequestForm

from src.database.models import User
from src.exceptions.http_exceptions import UnauthorizedException
from src.core.security import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    verify_token
)
from src.core.schemas import (
    Token,
    TokenData,
)
from src.core.settings import tokenSettings, serverSettings

router: APIRouter = APIRouter(tags=["auth"], prefix="/auth")


@router.post("/login",
             response_model=Token)
async def login(
        response: Response,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user: User = await authenticate_user(
        username_or_email=form_data.username,
        password=form_data.password
    )

    token_data: TokenData = TokenData(
            user_id=user.uuid,
            token_type=None,
            username=user.username, exp=None)
    access_token = await create_access_token(
        data=token_data)

    refresh_token = await create_refresh_token(
        data=token_data
    )

    max_age: float = tokenSettings.refresh_token_ttl.total_seconds()
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=serverSettings.secure,
        path=f"{serverSettings.root_path}v1/auth",
        samesite='lax',
        max_age=int(max_age)
    )

    return Token(
        access_token=access_token,
        token_type="bearer"
    )


@router.post("/refresh")
async def refresh_access_token(
    request: Request,
    response: Response
) -> Token:
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise UnauthorizedException(
            "Refresh token missing.")

    token_data: TokenData = await verify_token(refresh_token)

    new_access_token: str = await create_access_token(
        data=token_data)
    new_refresh_token: str = await create_refresh_token(
        data=token_data)

    max_age: float = tokenSettings.refresh_token_ttl.total_seconds()
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=serverSettings.secure,
        path=f"{serverSettings.root_path}v1/auth",
        samesite='lax',
        max_age=int(max_age)
    )
    return Token(
        access_token=new_access_token,
        token_type="bearer"
    )
