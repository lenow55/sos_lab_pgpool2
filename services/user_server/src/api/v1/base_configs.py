from typing import Annotated
import uuid as uuid_pkg
from fastapi import APIRouter, Depends
from src.api.dependencies import get_current_user
from src.schemas.base_config import BaseConfigOnly, BaseConfigRead
from src.core.schemas import Status
from src.exceptions.http_exceptions import DocumentCustomException
from src.api.paginated import ListResponse, PaginatedListResponse, compute_offset
from src.schemas.base_config import BaseConfig, BaseConfigCreate, BaseConfigUpdate
from src.schemas.user import User
from src.crud.base_config_service import baseConfigService

router: APIRouter = APIRouter(tags=["BaseConfigs"])


@router.get("/base_config/{id}",
            response_model=BaseConfigRead)
async def get_base_config(
        id: uuid_pkg.UUID,
) -> BaseConfigRead:
    return await baseConfigService.get_base_config(id=id)


@router.get("/base_configs",
            response_model=PaginatedListResponse
            [BaseConfigRead])
async def get_base_configs(
        page: int = 1,
        items_per_page: int = 10) -> PaginatedListResponse[BaseConfigRead]:
    base_configs_data: ListResponse = await baseConfigService.get_multi_base_configs(
        offset=compute_offset(page, items_per_page),
        limit=items_per_page
    )
    return PaginatedListResponse[BaseConfigRead](
        data=base_configs_data.data,
        total_count=base_configs_data.total_count,
        has_more=(page*items_per_page) < base_configs_data.total_count,
        page=page,
        items_per_page=items_per_page)


@router.post("/base_config",
             response_model=BaseConfig)
async def write_base_config(
        base_config: BaseConfigCreate,
        current_user: Annotated[User, Depends(get_current_user)]) -> BaseConfig:
    return await baseConfigService.create_base_config(
        obj=base_config,
        current_user_id=current_user.uuid)


@router.patch("/base_config/{id}",
              responses={404: {"model": DocumentCustomException}},
              response_model=BaseConfigOnly)
async def update_base_config(
        id: uuid_pkg.UUID,
        user_id: uuid_pkg.UUID,
        base_config_info: BaseConfigUpdate) -> BaseConfigOnly:
    return await baseConfigService.update_base_config(
        id=id, user_id=user_id, obj_update_info=base_config_info)


@router.delete(
    "/base_config/{id}", response_model=Status,
    responses={404: {"model": DocumentCustomException}})
async def delete_base_config(
    id: uuid_pkg.UUID,
    user_id: uuid_pkg.UUID) -> Status:
    return await baseConfigService.delete_base_config(id=id, user_id=user_id)
