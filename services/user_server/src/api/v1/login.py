from typing import Annotated
import uuid as uuid_pkg
from fastapi import APIRouter, Depends
from src.core.schemas import Status
from src.exceptions.http_exceptions import DocumentCustomException
from fastapi.security import OAuth2PasswordRequestForm
from src.core.schemas import (
        Token
        )

router: APIRouter = APIRouter(tags=["login"])


@router.get("/login",
            response_model=Token)
async def get_user(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    form_data.username
    return await userService.get_user(user_id=user_id)


@router.get("/users",
            response_model=PaginatedListResponse[User])
async def get_users(
        page: int = 1,
        items_per_page: int = 10
) -> PaginatedListResponse[User]:
    users_data: ListResponse = await userService.get_multi_users(
        offset=compute_offset(page, items_per_page),
        limit=items_per_page
    )
    return PaginatedListResponse[User](
        data=users_data.data,
        total_count=users_data.total_count,
        has_more=(page*items_per_page) < users_data.total_count,
        page=page,
        items_per_page=items_per_page)


@router.post("/user",
             response_model=User)
async def write_user(
    user: UserCreate,
) -> User:
    return await userService.create_user(user_in_obj=user)


@router.patch("/user/{user_id}",
              responses={404: {"model": DocumentCustomException}},
              response_model=User)
async def update_user(
    user_id: uuid_pkg.UUID,
    user_info: UserUpdate,
) -> User:
    return await userService.update_user(user_id=user_id, user_update_info=user_info)


@router.delete("/user/{user_id}",
               response_model=Status,
               responses={404: {"model": DocumentCustomException}})
async def delete_user(
    user_id: uuid_pkg.UUID
) -> Status:
    return await userService.delete_user(user_id=user_id)
