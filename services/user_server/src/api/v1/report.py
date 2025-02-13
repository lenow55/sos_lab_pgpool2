from typing import Annotated
from fastapi import APIRouter, Depends, Request, Response

from src.database.models import User
from src.exceptions.http_exceptions import UnauthorizedException
from src.core.security import (
    authenticate_user,
    verify_access_token
)
from src.core.schemas import (
    Token,
    TokenData,
)
from src.core.settings import tokenSettings, serverSettings

router: APIRouter = APIRouter(tags=["report"])


@router.post("/report",
             response_model=Token)
async def login(
        response: Response,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user: User = await authenticate_user(
        username_or_email=form_data.username,
        password=form_data.password
    )
    return Token(
        access_token=access_token,
        token_type="bearer"
    )
