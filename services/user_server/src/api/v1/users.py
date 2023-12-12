import uuid as uuid_pkg
from fastapi import APIRouter
from fastapi.params import Query
from src.exceptions.http_exceptions import DocumentCustomException
from src.api.paginated import ListResponse, PaginatedListResponse, compute_offset
from src.schemas.user import User, UserCreate, UserRead, UserUpdate
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
        has_more=(page*items_per_page) < users_data.total_count,
        page=page,
        items_per_page=items_per_page)


@router.post("/user",
             response_model=User)
async def write_user(
    user: UserCreate,
) -> User:
    return await userService.create_user(user_in_obj=user)


@router.patch("/user",
              response_model=User)
async def update_user(
    user: UserUpdate,
) -> User:
    return await userService.update_user(user_in_obj=user)


@router.delete("/user/{user_id}",
               response_model=User,
               responses={404: {"model": DocumentCustomException}},
               status_code=201)
async def delete_user(
    user_id: uuid_pkg.UUID
) -> User:
    return await userService.delete_user(user_id=user_id)
