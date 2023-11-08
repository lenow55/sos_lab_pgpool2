import uuid
from typing import List
from typing import List

from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.responses import PlainTextResponse

from src.schemas.base_config import BaseConfigIn, BaseConfigOut


router = APIRouter()


@router.post(
    "/config",
    tags=["BaseConfigDTO"],
    description="Отправить конфигурацию на предсказание",
    response_model=BaseConfig,
    )
async def create_config(config: BaseConfigDTO) -> BaseConfig:
    return ()


@router.get(
    "/config/{config_id}",
    tags=["BaseConfig"],
    description="Получить конфигурацию по id",
    response_model=BaseConfig,
    )
async def read_config(config_id: uuid.UUID) -> BaseConfig:
    return BaseConfig(id=config_id)

@router.patch(
    "/config/{config_id}",
    tags=["BaseConfigDTO"],
    description="Получить конфигурацию по id",
    response_model=BaseConfig,
    )
async def update_config(
        config_id: uuid.UUID,
        config: BaseConfigDTO
    ) -> BaseConfig:
    return BaseConfig(id=config_id)

@router.get(
    "/configs",
    tags=["BaseConfigList"],
    description="Получить список конфигураций",
    response_model=List[BaseConfig],
    )
async def read_configs() -> List[BaseConfig]:
    return [BaseConfig()]

@router.delete(
    "/config/{config_id}",
    response_class=PlainTextResponse,
)
async def delete_config(
    config_id: uuid.UUID
) -> PlainTextResponse:
    return PlainTextResponse(content=f"id {config_id}")
