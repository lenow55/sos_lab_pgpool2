from tortoise.contrib.pydantic.base import PydanticModel
from tortoise.contrib.pydantic.creator import pydantic_model_creator

from src.database.models import ModelConfig


ModelConfigInSchema:type[PydanticModel] = pydantic_model_creator(
    ModelConfig,
    name="ModelConfigIn",
    exclude=(
        "id",
        "create_at",
        "modify_at"
        ),
    exclude_readonly=True
)
ModelConfigOutSchema:type[PydanticModel] = pydantic_model_creator(
    ModelConfig,
    name="ModelConfigOut",
)
