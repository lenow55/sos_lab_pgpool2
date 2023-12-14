import uuid as uuid_pkg
from fastapi import APIRouter
from src.core.security import get_password_hash
from src.core.schemas import Status
from src.exceptions.http_exceptions import DocumentCustomException
from src.api.paginated import ListResponse, PaginatedListResponse, compute_offset
from src.schemas.user import User, UserCreate, UserCreateInternal, UserRead, UserUpdate
from src.crud.userService import userService

router: APIRouter = APIRouter(tags=["Users"])


@router.get("/user/{user_id}",
            response_model=UserRead)
async def get_user(
        user_id: uuid_pkg.UUID
) -> UserRead:
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
        has_more=(
            page * items_per_page) < users_data.total_count,
        page=page,
        items_per_page=items_per_page)


@router.post("/user",
             response_model=User)
async def write_user(
    user: UserCreate,
) -> User:
    user_internal_obj: UserCreateInternal = UserCreateInternal(
            **user.model_dump(exclude=set("password")),
            hashed_password=get_password_hash(user.password))
    return await userService.create_user(user_in_obj=user_internal_obj)


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
