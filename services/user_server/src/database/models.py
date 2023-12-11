from datetime import datetime
from tortoise import fields, models
from tortoise.fields import SET_NULL, Field, ForeignKeyRelation
from uuid import UUID


class Users(models.Model):
    id: Field[UUID] = fields.UUIDField(pk=True)
    username: Field[str] = fields.CharField(max_length=20, unique=True)
    full_name: Field[str] = fields.CharField(max_length=50, null=True)
    password: Field[bytes] = fields.BinaryField(null=False)
    create_date: Field[datetime] = fields.DatetimeField(auto_now_add=True)
    update_date: Field[datetime] = fields.DatetimeField(auto_now=True)

class BaseConfig(models.Model):
    id: Field[UUID] = fields.UUIDField(pk=True)
    count_connections: Field[int] = fields.IntField()
    read_write_percent: Field[int] = fields.IntField()
    query_complex: Field[int] = fields.IntField()
    base_in_cache: Field[bool] = fields.BooleanField()
    query_cache: Field[bool] = fields.BooleanField()
    pgpool_enabled: Field[bool] = fields.BooleanField()
    author: ForeignKeyRelation|None = fields.ForeignKeyField(
            "models.Users",
            related_name="config",
            null=True,
            on_delete=SET_NULL)
    create_date: Field[datetime] = fields.DatetimeField(auto_now_add=True)
    update_date: Field[datetime] = fields.DatetimeField(auto_now=True)

    class Meta:
        # Define the default ordering
        #  the pydantic serialiser will use this to order the results
        ordering = ["id"]

class ModelConfig(models.Model):
    id: Field[UUID] = fields.UUIDField(pk=True)
    model_id: Field[UUID] = fields.UUIDField(index=True)
    model_name: Field[str] = fields.CharField(max_length=50, null=True)
    version: Field[int] = fields.IntField()
    # прописать энкодер и декодер
    # надо это потому что параметры для модели нельзя будет в одну схему упаковать
    params_json = fields.JSONField()
    create_at: Field[datetime] = fields.DatetimeField(auto_now_add=True)
    modify_at: Field[datetime] = fields.DatetimeField(auto_now=True)

