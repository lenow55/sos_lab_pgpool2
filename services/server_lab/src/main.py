from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from fastapi.exceptions import HTTPException
from fastapi.responses import PlainTextResponse
import uuid

app = FastAPI(description="Effective PP2", version="0.0.1")


class BaseConfig(BaseModel):
    id: uuid.UUID = uuid.uuid4()
    count_connections: int = 0
    read_write_percent: int = 0
    query_complex: int = 0
    base_in_cache: bool = False
    query_cache: bool = False
    pgpool_enabled: bool = False
    create_date: datetime = datetime.now()
    updated_date: datetime = datetime.now()

class BaseConfigDTO(BaseModel):
    count_connections: int = 0
    read_write_percent: int = 0
    query_complex: int = 0
    base_in_cache: bool = False
    query_cache: bool = False
    pgpool_enabled: bool = False

@app.post(
    "/config",
    tags=["BaseConfigDTO"],
    description="Отправить конфигурацию на предсказание",
    response_model=BaseConfig,
    )
async def create_config(config: BaseConfigDTO) -> BaseConfig:
    return BaseConfig()


@app.get(
    "/config/{config_id}",
    tags=["BaseConfig"],
    description="Получить конфигурацию по id",
    response_model=BaseConfig,
    )
async def read_config(config_id: uuid.UUID) -> BaseConfig:
    return BaseConfig(id=config_id)

@app.patch(
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

@app.get(
    "/configs",
    tags=["BaseConfigList"],
    description="Получить список конфигураций",
    response_model=List[BaseConfig],
    )
async def read_configs() -> List[BaseConfig]:
    return [BaseConfig()]

@app.delete(
    "/config/{config_id}",
    response_class=PlainTextResponse,
)
async def delete_config(
    config_id: uuid.UUID
) -> PlainTextResponse:
    return PlainTextResponse(content=f"id {config_id}")

