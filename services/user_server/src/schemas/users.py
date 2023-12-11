from tortoise.contrib.pydantic.base import PydanticModel
from tortoise.contrib.pydantic.creator import pydantic_model_creator

from src.database.models import Users


UserInSchema: type[PydanticModel] = pydantic_model_creator(
    Users,
    name="UserIn",
    exclude_readonly=True
)
UserOutSchema: type[PydanticModel] = pydantic_model_creator(
    Users,
    name="UserOut",
    exclude=(
        "password",
        "created_at",
        "modified_at"
        )
)
UserDatabaseSchema: type[PydanticModel] = pydantic_model_creator(
    Users,
    name="User",
    exclude=(
        "created_at",
        "modified_at"
        )
)
