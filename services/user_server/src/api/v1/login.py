from typing import Annotated
from fastapi import APIRouter, Depends, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from src.api.dependencies import get_refresh_session_manager
from src.core.sessions.refresh_session import RefreshSession

from src.database.models import User
from src.exceptions.http_exceptions import UnauthorizedException
from src.core.security import (
    authenticate_user,
    create_access_token,
)
from src.core.schemas import (
    AccessData,
    Token,
)

router: APIRouter = APIRouter(tags=["auth"], prefix="/auth")


@router.post("/login",
             response_model=Token)
async def login(
        response: Response,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        refresh_session: Annotated[RefreshSession, Depends(get_refresh_session_manager)]
) -> Token:
    user: User = await authenticate_user(
        username_or_email=form_data.username,
        password=form_data.password
    )

    token_data: AccessData = AccessData(
        user_id=user.uuid,
        token_type=None,
        username=user.username, exp=None)
    access_token = await create_access_token(
        data=token_data)

    await refresh_session.create_refresh_session(
        data=token_data, response=response)

    return Token(
        access_token=access_token,
        token_type="bearer"
    )


@router.post("/refresh")
async def refresh_access_token(
    request: Request,
    response: Response,
    refresh_session: Annotated[RefreshSession, Depends(get_refresh_session_manager)]
) -> Token:

    token_data: AccessData = await refresh_session.update_refresh_session(
        request=request,
        response=response)

    user_exist: bool = await User.exists(uuid=token_data.user_id, is_deleted=False)
    if user_exist == False:
        response = await refresh_session.delete_refresh_session(
            request=request,
            response=response)
        headers = {"set-cookie": response.headers["set-cookie"]}
        raise UnauthorizedException("User not found", headers=headers)

    new_access_token: str = await create_access_token(
        data=token_data)

    return Token(
        access_token=new_access_token,
        token_type="bearer"
    )
