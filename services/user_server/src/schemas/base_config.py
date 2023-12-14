from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated, ClassVar, Optional
from tortoise.contrib.pydantic.creator import pydantic_model_creator
from src.database import models

import logging
from src.core import logger as logger_mod
logger = logging.getLogger(__name__)


BaseConfig = pydantic_model_creator(
    cls=models.BaseConfig,
    name="BaseConfig",
    exclude=("author.hashed_password",
             "author.create_at",
             "author.update_at",
             "author.is_deleted",
             "author.deleted_at"),
    model_config=ConfigDict(
        extra='forbid',
    )
)

BaseConfigRead = pydantic_model_creator(
    cls=models.BaseConfig,
    name="BaseConfigRead",
    exclude=("create_at",
             "update_at",
             "author.hashed_password",
             "author.create_at",
             "author.update_at",
             "author.delete",
             "author.deleted_at",
             #"author.uuid",
             "author.is_deleted",
             "author.email",
             "author.full_name"),
    model_config=ConfigDict(
        extra='forbid',
    )
)

BaseConfigOnly = pydantic_model_creator(
    cls=models.BaseConfig,
    name="BaseConfigOnly",
    exclude=("author",),
    model_config=ConfigDict(
        extra='forbid',
    )
)


class BaseConfigBase(BaseModel):
    count_connections: Annotated[
        int,
        Field(
            ge=1, le=10000,
            examples=[80],
            description="Количество соединений к базе"
        )
    ]
    read_write_percent: Annotated[
        int,
        Field(
            ge=0, le=100,
            examples=[50],
            description="Процент записей на чтение к базе"
        )
    ]
    query_complex: Annotated[
        int,
        Field(
            ge=1, le=1000000,
            examples=[10000],
            description="Сложность запроса \
                    пока не понятно как будет выглядеть"
        )
    ]
    base_in_cache: Annotated[
        bool,
        Field(
            examples=[False],
            description="Помещается ли база данных в кэш"
        )
    ]
    query_cache: Annotated[
        bool,
        Field(
            examples=[False],
            description="Включён ли кэш запросов на pgpool"
        )
    ]


class BaseConfigCreate(BaseConfigBase):
    pgpool_enabled: Annotated[
        bool,
        Field(
            examples=[False],
            description="Включён ли PgPool2"
        )
    ]

    model_config: ClassVar[ConfigDict] = ConfigDict(
        extra='forbid')


class BaseConfigUpdate(BaseModel):
    count_connections: Annotated[
        Optional[int],
        Field(
            ge=1, le=10000,
            examples=[80],
            description="Количество соединений к базе"
        )
    ]
    read_write_percent: Annotated[
        Optional[int],
        Field(
            ge=0, le=100,
            examples=[50],
            description="Процент записей на чтение к базе"
        )
    ]
    query_complex: Annotated[
        Optional[int],
        Field(
            ge=1, le=1000000,
            examples=[10000],
            description="Сложность запроса \
                    пока не понятно как будет выглядеть"
        )
    ]
    base_in_cache: Annotated[
        Optional[bool],
        Field(
            examples=[False],
            description="Помещается ли база данных в кэш"
        )
    ]
    query_cache: Annotated[
        Optional[bool],
        Field(
            examples=[False],
            description="Включён ли кэш запросов на pgpool"
        )
    ]
