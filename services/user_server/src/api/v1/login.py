from typing import Annotated
import uuid as uuid_pkg
from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm

from src.database.models import User
from src.exceptions.http_exceptions import DocumentCustomException
from src.core.security import (
    authenticate_user,
    create_access_token,
    create_refresh_token
)
from src.core.schemas import (
    Token,
    Status,
    TokenData
)
from src.core.settings import tokenSettings, serverSettings

router: APIRouter = APIRouter(tags=["login"])


@router.get("/login",
            response_model=Token)
async def get_user(
        response: Response,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user: User = await authenticate_user(
        username_or_email=form_data.username,
        password=form_data.password
    )

    token_data: dict = {
        "user_id": user.uuid,
        "username": user.username
    }
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
        samesite='lax',
        max_age=int(max_age)
    )

    return Token(
        token=access_token,
        token_type="bearer"
    )

@router.post("/refresh")
async def refresh_access_token(
    request: Request,
) -> Dict[str, str]:
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise UnauthorizedException("Refresh token missing.")

    user_data = await verify_token(refresh_token, db)
    if not user_data:
        raise UnauthorizedException("Invalid refresh token.")

    new_access_token = await create_access_token(data={"sub": user_data.username_or_email})
    return {"access_token": new_access_token, "token_type": "bearer"}
