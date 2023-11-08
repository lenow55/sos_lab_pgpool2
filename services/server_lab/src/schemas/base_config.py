from tortoise.contrib.pydantic.base import PydanticModel
from tortoise.contrib.pydantic.creator import pydantic_model_creator
from src.database.models import BaseConfig


BaseConfigIn: type[PydanticModel] = pydantic_model_creator(
    BaseConfig,
    name="BaseConfigIn",
    exclude=("author",),
    exclude_readonly=True
)

BaseConfigOut: type[PydanticModel] = pydantic_model_creator(
    BaseConfig,
    name="BaseConfigOut",
    #    exclude=(
    #        "author.full_name",
    #        "author.password",
    #        "author.create_date",
    #        "author.update_date",
    #        )
)
